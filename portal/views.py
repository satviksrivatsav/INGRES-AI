import os
import joblib
import numpy as np

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.db.models import Count
from django.urls import reverse

from .models import GroundwaterData, SafetyCheck, WaterPlan
from chatbot.models import ChatConversation
from schemes.models import WaterScheme
from accounts.models import UserProfile


User = get_user_model()

# ============================================================
# LOAD ML MODELS
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.path.join(BASE_DIR, "portal/ml_models")

RESOURCE_MODEL = joblib.load(os.path.join(MODEL_DIR, "resource_planner_model.pkl"))
RESOURCE_ENCODERS = joblib.load(os.path.join(MODEL_DIR, "resource_planner_encoders.pkl"))
RESOURCE_TARGET = joblib.load(os.path.join(MODEL_DIR, "resource_planner_target.pkl"))

SAFETY_MODEL = joblib.load(os.path.join(MODEL_DIR, "safety_checker_model.pkl"))
SAFETY_ENCODERS = joblib.load(os.path.join(MODEL_DIR, "safety_checker_encoders.pkl"))
SAFETY_TARGET = joblib.load(os.path.join(MODEL_DIR, "safety_checker_target.pkl"))

# ============================================================
# PUBLIC PAGES
# ============================================================

def landing_view(request):
    return render(request, "landing.html")


# ============================================================
# PUBLIC DASHBOARD
# ============================================================

@login_required
def public_dashboard_view(request):

    user_profile = getattr(request.user, "profile", None)

    ap_data = GroundwaterData.objects.filter(
        state="Andhra Pradesh"
    ).order_by("district")

    local_data = None

    if user_profile and user_profile.state and user_profile.district:
        local_data = GroundwaterData.objects.filter(
            state=user_profile.state,
            district=user_profile.district
        ).first()

    active_alerts = []

    if user_profile and user_profile.state:
        active_alerts = GroundwaterData.objects.filter(
            state=user_profile.state,
            is_active_alert=True
        ).order_by("-created_at")[:3]

    recent_chats = ChatConversation.objects.filter(
        user=request.user,
        bot_type="public"
    ).order_by("-timestamp")[:5]

    points = GroundwaterData.objects.exclude(
        latitude__isnull=True
    ).exclude(
        longitude__isnull=True
    )

    region_display = "Location Not Set"

    if user_profile and user_profile.district:
        region_display = f"{user_profile.district}, {user_profile.state}"

    context = {
        "status": local_data,
        "alerts": active_alerts,
        "recent_chats": recent_chats,
        "points": points,
        "region": region_display,
        "ap_data": ap_data,
        "is_critical": local_data.status_category in ["Critical","Over-Exploited"] if local_data else False
    }

    return render(request,"dashboards/public_dashboard.html",context)


# ============================================================
# OFFICIAL DASHBOARD
# ============================================================

@user_passes_test(lambda u: u.role == "official" or u.is_superuser)
@login_required
def official_dashboard_view(request):

    active_alerts = GroundwaterData.objects.filter(is_active_alert=True)

    stats = GroundwaterData.objects.values(
        "status_category"
    ).annotate(
        count=Count("id")
    )

    user_stats = User.objects.filter(
        role="official"
    ).values(
        "role"
    ).annotate(
        total=Count("id")
    )

    context = {
        "alerts": active_alerts,
        "stats": stats,
        "user_stats": user_stats,
        "page_title": "Official Policy Node"
    }

    return render(request,"dashboards/official_dashboard.html",context)


# ============================================================
# LOCATION UPDATE
# ============================================================

@login_required
def update_location_view(request):

    if request.method == "POST":

        state = request.POST.get("state")
        district = request.POST.get("district")

        profile, created = UserProfile.objects.get_or_create(user=request.user)

        profile.state = state
        profile.district = district
        profile.save()

        return JsonResponse({
            "success": True,
            "district": district,
            "state": state
        })

    return JsonResponse({"success": False}, status=400)


# ============================================================
# PROFILE SETTINGS
# ============================================================

@login_required
def profile_settings_view(request):

    user = request.user
    profile = getattr(user, "profile", None)

    if request.method == "POST":

        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")

        if profile:
            profile.state = request.POST.get("state")
            profile.district = request.POST.get("district")
            profile.phone = request.POST.get("phone")
            profile.save()

        user.save()

    return render(request,"dashboards/profile.html",{
        "user":user,
        "profile":profile
    })


# ============================================================
# WATER RESOURCE PLANNER (ML MODEL)
# ============================================================

@login_required
def water_planner_view(request):

    if request.method == "POST":

        try:

            land = float(request.POST.get("land_size"))
            crop = request.POST.get("crop_type")
            season = request.POST.get("season")

            rainfall = "moderate"
            soil = "loamy"

            crop_encoded = RESOURCE_ENCODERS["crop"].transform([crop])[0]
            season_encoded = RESOURCE_ENCODERS["season"].transform([season])[0]
            rainfall_encoded = RESOURCE_ENCODERS["rainfall"].transform([rainfall])[0]
            soil_encoded = RESOURCE_ENCODERS["soil_type"].transform([soil])[0]

            features = np.array([[crop_encoded,season_encoded,rainfall_encoded,soil_encoded,land]])

            prediction = RESOURCE_MODEL.predict(features)

            risk = RESOURCE_TARGET.inverse_transform(prediction)[0]

            estimated_need = int(land * 800)

            WaterPlan.objects.create(
                user=request.user,
                land_size=land,
                crop_type=crop.capitalize(),
                season=season.capitalize(),
                estimated_need=estimated_need,
                risk_level=risk
            )

            return redirect(reverse("portal:water_planner"))

        except Exception as e:
            print(e)

    plans = WaterPlan.objects.filter(user=request.user).order_by("-created_at")

    return render(request,"dashboards/planner.html",{
        "plans":plans
    })


# ============================================================
# WATER SAFETY CHECKER (ML MODEL)
# ============================================================

@login_required
def safety_checker_view(request):

    if request.method == "POST":

        area = request.POST.get("location_area","Unknown")
        source = request.POST.get("source_type")

        tds = 500
        bacteria = 20
        turbidity = 5

        source_encoded = SAFETY_ENCODERS["water_source"].transform([source])[0]
        area_encoded = SAFETY_ENCODERS["area_type"].transform(["rural"])[0]

        features = np.array([[source_encoded,area_encoded,tds,bacteria,turbidity]])

        prediction = SAFETY_MODEL.predict(features)

        safety_score = SAFETY_TARGET.inverse_transform(prediction)[0]

        advice_map = {
            "Safe":"Water quality acceptable. Periodic testing recommended.",
            "Warning":"Potential contamination risk. Use filtration or boiling.",
            "Unsafe":"Water unsafe for direct consumption. Use RO + boiling."
        }

        SafetyCheck.objects.create(
            user=request.user,
            location_area=area,
            source_type=source.capitalize(),
            safety_score=safety_score,
            advice=advice_map[safety_score]
        )

        return redirect("portal:safety_checker")

    checks = SafetyCheck.objects.filter(
        user=request.user
    ).order_by("-checked_at")

    return render(request,"dashboards/safety_checker.html",{
        "checks":checks
    })


# ============================================================
# INTERACTIVE MAP
# ============================================================

@login_required
def map_view(request):

    geo_data = GroundwaterData.objects.all()

    return render(request,"dashboards/maps.html",{
        "points":geo_data,
        "page_title":"Interactive Groundwater Intelligence Map"
    })


# ============================================================
# CONSERVATION ADVISOR
# ============================================================

@login_required
def conservation_advisor_view(request):

    user_profile = getattr(request.user,"profile",None)

    local_status = None

    if user_profile and user_profile.district:
        local_status = GroundwaterData.objects.filter(
            district=user_profile.district
        ).first()

    is_critical = local_status.status_category in ["Critical","Over-Exploited"] if local_status else False

    protocols = [

        {
            "title":"Drip Irrigation",
            "impact":"Reduces water use by 40-70%",
            "icon":"fa-faucet-drip",
            "is_priority":is_critical
        },

        {
            "title":"Rainwater Harvesting",
            "impact":"Recharges 100k+ Litres/Year",
            "icon":"fa-cloud-showers-water",
            "is_priority":True
        },

        {
            "title":"Mulching Techniques",
            "impact":"Prevents 30% soil moisture loss",
            "icon":"fa-seedling",
            "is_priority":False
        }
    ]

    return render(request,"dashboards/advisor.html",{
        "protocols":protocols,
        "is_critical":is_critical
    })