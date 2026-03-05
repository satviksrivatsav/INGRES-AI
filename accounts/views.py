import random
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import EmailOTP, UserProfile

User = get_user_model()

def login_view(request):
    """
    Handles secure authentication and routes users to their specific 
    Intelligence Hub based on their designated Role.
    """
    if request.method == 'POST':
        email = request.POST.get('username')  # Usually named 'username' in standard forms
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user:
            # 1. Verification Check: Ensure OTP process was completed
            if not user.is_active:
                messages.error(request, 'Verification Pending: Please verify your email via OTP.')
                return render(request, 'accounts/login.html')

            login(request, user)

            # 2. Analytics: Increment login counter
            if hasattr(user, 'login_count'):
                user.login_count += 1
                user.save()

            # 3. 3-Way Role Routing: Redirect to specific workspace
            if user.role == 'official':
                return redirect('portal:official_dashboard')
            elif user.role == 'researcher':
                return redirect('portal:researcher_dashboard')
            else: 
                # Default for Public users (Citizens/Farmers)
                return redirect('portal:public_dashboard')

        messages.error(request, 'Invalid credentials. Please verify your email and password.')

    return render(request, 'accounts/login.html')


def signup_view(request):
    """
    Captures user details and the chosen INGRES-AI Role, 
    then triggers the SMTP verification sequence.
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        # FR-1.1: Capture the dynamic role selected by the user
        role = request.POST.get('role', 'public') 

        # 1. Existence Check: Prevent duplicate accounts
        if User.objects.filter(email=email).exists():
            messages.info(request, 'This account already exists. Please sign in.')
            return redirect('accounts:login')

        # 2. Secure User Creation
        # Note: is_active=False ensures they can't login until OTP is verified
        user = User.objects.create_user(
            email=email,
            password=password,
            role=role,
            is_active=False
        )

        # 3. Role Sync with Profile
        # The profile is auto-created by your signal; we just update the role field
        user.profile.role = role
        user.profile.save()

        # 4. Automated OTP Generation
        otp = str(random.randint(100000, 999999))
        EmailOTP.objects.update_or_create(user=user, defaults={'otp': otp})

        # 5. SMTP Trigger: Send verification code
        try:
            send_mail(
                subject='[INGRES-AI] Security Verification Code',
                message=f'Welcome to the INGRES-AI Node.\n\nYour verification code is: {otp}\n\nThis code expires in 10 minutes.',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception as e:
            # Fallback for local development or SMTP misconfiguration
            print(f"SMTP Error: {e}")
            messages.warning(request, 'Email service unavailable. If you are a developer, check the console for your OTP.')

        # 6. Session Hand-off: Pass the user ID to the next step
        request.session['verify_user'] = user.id
        return redirect('accounts:verify_otp')

    return render(request, 'accounts/signup.html')


def verify_otp_view(request):
    user_id = request.session.get('verify_user')

    if not user_id:
        return redirect('accounts:signup')

    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        otp_obj = EmailOTP.objects.filter(user=user).first()

        if otp_obj and not otp_obj.is_expired() and entered_otp == otp_obj.otp:
            user.is_active = True
            user.is_verified = True
            user.save()

            otp_obj.delete()
            del request.session['verify_user']

            return render(request, 'accounts/verify_success.html')

        messages.error(request, 'Invalid or expired OTP.')

    return render(request, 'accounts/verify_otp.html')


def logout_view(request):
    logout(request)
    return redirect('landing')

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)
    # This ensures the profile is saved whenever the user is saved
    if hasattr(instance, 'profile'):
        instance.profile.save()