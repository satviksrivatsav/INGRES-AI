from django.db import models
from portal.models import GroundwaterData

class MapMarker(models.Model):
    # FR-6.4: Display key parameters when a unit is selected
    data_point = models.OneToOneField(GroundwaterData, on_delete=models.CASCADE, related_name='marker')
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    # We use this to cache coordinates so Leaflet doesn't have to geocode on every load
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Marker: {self.data_point.district} ({self.data_point.state})"