import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from portal.models import GroundwaterData

def seed_data():
    # List of major Indian districts with approximate coordinates
    # Rationale: Provides a diverse range of Safe to Over-Exploited zones
    districts_data = [
        # Andhra Pradesh
        {"district": "Guntur", "state": "Andhra Pradesh", "lat": 16.3067, "lon": 80.4365, "status": "Critical", "extract": 92.5, "recharge": 450.0},
        {"district": "Nellore", "state": "Andhra Pradesh", "lat": 14.4426, "lon": 79.9865, "status": "Safe", "extract": 45.0, "recharge": 620.0},
        {"district": "Kurnool", "state": "Andhra Pradesh", "lat": 15.8281, "lon": 78.0373, "status": "Semi-Critical", "extract": 78.2, "recharge": 310.0},
        
        # Karnataka
        {"district": "Bangalore", "state": "Karnataka", "lat": 12.9716, "lon": 77.5946, "status": "Over-Exploited", "extract": 142.0, "recharge": 120.0},
        {"district": "Mysore", "state": "Karnataka", "lat": 12.2958, "lon": 76.6394, "status": "Safe", "extract": 38.5, "recharge": 580.0},
        {"district": "Bagalkot", "state": "Karnataka", "lat": 16.1817, "lon": 75.6958, "status": "Critical", "extract": 98.0, "recharge": 200.0},

        # Maharashtra
        {"district": "Mumbai", "state": "Maharashtra", "lat": 19.0760, "lon": 72.8777, "status": "Safe", "extract": 20.0, "recharge": 900.0},
        {"district": "Pune", "state": "Maharashtra", "lat": 18.5204, "lon": 73.8567, "status": "Semi-Critical", "extract": 81.0, "recharge": 450.0},
        {"district": "Ahmednagar", "state": "Maharashtra", "lat": 19.0948, "lon": 74.7480, "status": "Over-Exploited", "extract": 115.0, "recharge": 300.0},

        # Delhi
        {"district": "New Delhi", "state": "Delhi", "lat": 28.6139, "lon": 77.2090, "status": "Over-Exploited", "extract": 170.0, "recharge": 50.0},

        # Punjab (High extraction area)
        {"district": "Ludhiana", "state": "Punjab", "lat": 30.9010, "lon": 75.8573, "status": "Over-Exploited", "extract": 165.0, "recharge": 210.0},
        {"district": "Amritsar", "state": "Punjab", "lat": 31.6340, "lon": 74.8723, "status": "Critical", "extract": 99.5, "recharge": 180.0},

        # Rajasthan
        {"district": "Jaipur", "state": "Rajasthan", "lat": 26.9124, "lon": 75.7873, "status": "Over-Exploited", "extract": 185.0, "recharge": 90.0},
        {"district": "Jodhpur", "state": "Rajasthan", "lat": 26.2389, "lon": 73.0243, "status": "Critical", "extract": 105.0, "recharge": 110.0}
    ]

    print("--- Starting Database Seeding ---")
    count = 0
    for item in districts_data:
        obj, created = GroundwaterData.objects.update_or_create(
            district=item['district'],
            state=item['state'],
            defaults={
                'status_category': item['status'],
                'latitude': item['lat'],
                'longitude': item['lon'],
                'extraction_percentage': item['extract'],
                'recharge_value': item['recharge'],
                'description': f"Current groundwater assessment for {item['district']}. Status: {item['status']}.",
                'is_active_alert': True if item['status'] in ['Critical', 'Over-Exploited'] else False
            }
        )
        if created:
            count += 1
            print(f"Added: {item['district']}")
    
    print(f"--- Seeding Complete. {count} new entries added. ---")

if __name__ == '__main__':
    seed_data()