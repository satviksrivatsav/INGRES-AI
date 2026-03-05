from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.conf import settings

class ResearchDomainWhitelist(models.Model):
    domain = models.CharField(max_length=255, unique=True, help_text="e.g., institution.edu, org.name.org")

    def __str__(self):
        return self.domain

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    ROLE_CHOICES = (
        ('public', 'Public User (Citizen/Farmer)'),
        ('researcher', 'Research / Academic User'),
        ('official', 'Official Government User'),
    )

    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='official')

    is_verified = models.BooleanField(default=False)
    login_count = models.PositiveIntegerField(default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    
class UserProfile(models.Model):
    """
    Acts as the Regional Identity Node. Stores location data 
    critical for FR-2.3 (Hierarchical Retrieval).
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    state = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    
    # Stores the role here too for quick access in templates
    role = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"Profile for {self.user.email} ({self.user.role})"

class EmailOTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        # 10 Minute expiry as per security standards
        return timezone.now() > self.created_at + timedelta(minutes=10)

class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    title = models.CharField(max_length=100)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.email}: {self.title}"