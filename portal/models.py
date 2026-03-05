from django.db import models
from django.conf import settings
import requests


# ============================================================
# WATER RESOURCE PLANNER MODEL
# ============================================================

class WaterPlan(models.Model):

    CROP_CHOICES = [
        ('paddy', 'Paddy / Rice'),
        ('wheat', 'Wheat'),
        ('maize', 'Maize / Corn'),
        ('millets', 'Millets'),
        ('vegetables', 'Vegetables'),
    ]

    SEASON_CHOICES = [
        ('kharif', 'Kharif'),
        ('rabi', 'Rabi'),
        ('summer', 'Summer'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    land_size = models.FloatField(help_text="Size of land in Acres")

    crop_type = models.CharField(
        max_length=50,
        choices=CROP_CHOICES
    )

    season = models.CharField(
        max_length=20,
        choices=SEASON_CHOICES
    )

    estimated_need = models.FloatField(
        null=True,
        blank=True
    )

    risk_level = models.CharField(
        max_length=20,
        default="Low"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.crop_type} ({self.season})"


# ============================================================
# WATER QUALITY SAFETY CHECK MODEL
# ============================================================

class SafetyCheck(models.Model):

    SOURCE_CHOICES = [
        ('borewell', 'Borewell'),
        ('well', 'Open Well'),
        ('tap', 'Public Supply / Tap'),
        ('tanker', 'Private Tanker'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    location_area = models.CharField(
        max_length=100,
        help_text="Area or Landmark"
    )

    source_type = models.CharField(
        max_length=20,
        choices=SOURCE_CHOICES
    )

    safety_score = models.CharField(
        max_length=20
    )  # Safe, Warning, Unsafe

    advice = models.TextField()

    checked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.source_type} ({self.safety_score})"


# ============================================================
# CORE GROUNDWATER DATA MODEL
# ============================================================

class GroundwaterData(models.Model):

    STATUS_CHOICES = [
        ('Safe', 'Safe'),
        ('Semi-Critical', 'Semi-Critical'),
        ('Critical', 'Critical'),
        ('Over-Exploited', 'Over-Exploited'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    state = models.CharField(max_length=100)

    district = models.CharField(max_length=100)

    status_category = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Safe'
    )

    extraction_percentage = models.FloatField(
        default=0.0
    )

    recharge_value = models.FloatField(
        default=0.0
    )

    description = models.TextField(
        help_text="Details about groundwater conditions"
    )

    is_active_alert = models.BooleanField(
        default=False
    )

    latitude = models.FloatField(
        null=True,
        blank=True
    )

    longitude = models.FloatField(
        null=True,
        blank=True
    )

    assessment_year = models.IntegerField(
        default=2023
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    # --------------------------------------------------------

    def save(self, *args, **kwargs):
        if not self.latitude or not self.longitude:
            self._geocode_location()
        super().save(*args, **kwargs)

    # --------------------------------------------------------

    def _geocode_location(self):
        """
        Auto-fetch latitude and longitude using OpenStreetMap
        """
        try:
            query = f"{self.district}, {self.state}, India"

            url = "https://nominatim.openstreetmap.org/search"

            params = {
                "q": query,
                "format": "json",
                "limit": 1
            }

            headers = {
                "User-Agent": "INGRES-AI-System"
            }

            response = requests.get(
                url,
                params=params,
                headers=headers,
                timeout=10
            )

            data = response.json()

            if data:
                self.latitude = float(data[0]["lat"])
                self.longitude = float(data[0]["lon"])

        except Exception:
            pass

    # --------------------------------------------------------

    def __str__(self):
        return f"{self.district}, {self.state} - {self.status_category}"

    class Meta:
        verbose_name = "Groundwater Data"
        verbose_name_plural = "Groundwater Data Entries"