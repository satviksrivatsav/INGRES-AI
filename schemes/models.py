from django.db import models

class WaterScheme(models.Model):
    CATEGORY_CHOICES = [
        ('irrigation', 'Irrigation Support'),
        ('financial', 'Financial Subsidy'),
        ('technical', 'Technical Assistance'),
        ('infrastructure', 'Rainwater Harvesting'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    benefits = models.TextField(help_text="Bulleted list of benefits")
    eligibility = models.TextField()
    application_link = models.URLField(blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    state_specific = models.CharField(max_length=100, blank=True, help_text="Leave blank for National schemes")

    def __str__(self):
        return self.name