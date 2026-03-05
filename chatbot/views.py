import json
import re
from google import genai
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render
from .models import ChatConversation
from portal.models import GroundwaterData


# Initialize Gemini Client (New SDK)
try:
    client = genai.Client(api_key=settings.AI_API_KEY) if getattr(settings, 'AI_API_KEY', None) else None
except Exception as e:
    client = None
    print(f"Warning: Gemini Client initialization failed: {e}")

def clean_markdown(text):
    """Removes markdown for a clean professional UI."""
    if not text:
        return ""
    text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
    text = re.sub(r'\*(.*?)\*', r'\1', text)
    text = re.sub(r'#+\s*', '', text)
    return text.strip()


def get_groundwater_context(query_text):
    """
    Enhanced RAG Logic:
    - Detect district
    - Detect year (if mentioned)
    - Return exact dataset record
    """

    district_match = None
    year_match = None

    # Detect year (4-digit number)
    year_search = re.search(r'(20\d{2})', query_text)
    if year_search:
        year_match = int(year_search.group(1))

    # Try to match district
    for data in GroundwaterData.objects.all():
        if data.district.lower() in query_text.lower():
            district_match = data.district
            break

    if not district_match:
        return None

    queryset = GroundwaterData.objects.filter(district=district_match)

    if year_match:
        queryset = queryset.filter(assessment_year=year_match)

    record = queryset.first()

    if not record:
        return None

    return {
        "district": record.district,
        "year": record.assessment_year,
        "status": record.status_category,
        "extraction": record.extraction_percentage,
        "recharge": record.recharge_value,
        "description": record.description
    }


def full_chat_view(request):
    """Renders the Water Buddy AI interface."""
    if request.user.is_authenticated:
        history = ChatConversation.objects.filter(
            user=request.user,
            bot_type='public'
        ).order_by('-timestamp')[:10]
    else:
        history = []

    return render(request, 'chatbot/chatbot.html', {'history': history})


def chatbot_query(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Unauthorized'}, status=400)

    try:
        data = json.loads(request.body)
        user_msg = data.get('msg', '').strip()

        if not user_msg:
            return JsonResponse({'reply': 'Please enter a valid query.'}, status=400)

        # 1. RETRIEVAL STEP (Structured RAG)
        retrieved_data = get_groundwater_context(user_msg)

        if retrieved_data:
            # Direct structured answer (NO hallucination possible)
            bot_reply = (
                f"Groundwater Assessment Report:\n"
                f"1. District: {retrieved_data['district']}\n"
                f"2. Assessment Year: {retrieved_data['year']}\n"
                f"3. Status Category: {retrieved_data['status']}\n"
                f"4. Extraction Stage: {retrieved_data['extraction']}%\n"
                f"5. Annual Recharge: {retrieved_data['recharge']} MCM\n\n"
                f"Interpretation:\n"
            )

            # AI only generates explanation — NOT numbers
            explanation_prompt = (
                "Explain the groundwater status category in simple professional terms. "
                f"Status Category: {retrieved_data['status']}. "
                "Do not generate any numbers. No markdown. Professional tone."
            )

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=explanation_prompt
            )

            explanation = clean_markdown(response.text)

            bot_reply += explanation

        else:
            # General explanatory query (no numeric retrieval)
            general_prompt = (
                "You are an official groundwater assistant. "
                "Answer clearly and professionally. "
                "No markdown. No fabricated statistics."
                f"\nUser Query: {user_msg}"
            )

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=general_prompt
            )

            bot_reply = clean_markdown(response.text)

        # Save conversation
        ChatConversation.objects.create(
            user=request.user if request.user.is_authenticated else None,
            message=user_msg,
            response=bot_reply,
            bot_type='public'
        )

        return JsonResponse({"reply": bot_reply})

    except Exception as e:
        print(f"Chatbot Error: {e}")
        return JsonResponse(
            {'reply': 'Water Intelligence Node offline. Try again.'},
            status=500
        )
