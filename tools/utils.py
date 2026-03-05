import requests
from django.conf import settings

def calculate_water_need(land_size, crop_type):
    """
    Standardizes crop water requirements (units in MCM per Acre).
    Reference: CGWB Hydrology Standards.
    """
    intensity = {
        'paddy': 1200, 
        'wheat': 800, 
        'maize': 600, 
        'millets': 400, 
        'vegetables': 550
    }
    base_need = intensity.get(crop_type.lower(), 500)
    return round(land_size * base_need, 2)

def get_geo_coords(district, state):
    """
    Helper to fetch coordinates for the Map app and User Profile.
    Uses Nominatim API with a safety timeout.
    """
    try:
        query = f"{district}, {state}, India"
        url = "https://nominatim.openstreetmap.org/search"
        params = {"q": query, "format": "json", "limit": 1}
        headers = {"User-Agent": "INGRES-AI-Project"}
        
        response = requests.get(url, params=params, headers=headers, timeout=5)
        data = response.json()
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"])
    except Exception:
        pass
    return None, None