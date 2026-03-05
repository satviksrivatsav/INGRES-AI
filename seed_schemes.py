import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from schemes.models import WaterScheme

def seed_schemes():
    schemes_data = [
        # National Schemes
        {
            "name": "Jal Jeevan Mission (JJM)",
            "desc": "A flagship central government initiative to provide functional household tap connections to all rural households in India by 2024.",
            "benefits": "1. Assured tap water supply.\n2. Improved health through clean water.\n3. Community participation in water management.",
            "eligibility": "All rural households in India.",
            "link": "https://jaljeevanmission.gov.in/",
            "cat": "infrastructure",
            "state": ""
        },
        {
            "name": "Atal Bhujal Yojana (ATAL JAL)",
            "desc": "A world-bank funded scheme focused on sustainable groundwater management through community participation.",
            "benefits": "1. Funding for water conservation.\n2. Technical support for local water budgeting.\n3. Incentives for high-performing panchayats.",
            "eligibility": "Gram Panchayats in water-stressed identified states.",
            "link": "https://ataljal.mowr.gov.in/",
            "cat": "technical",
            "state": ""
        },
        {
            "name": "Pradhan Mantri Krishi Sinchayee Yojana (PMKSY)",
            "desc": "Focuses on 'Har Khet Ko Pani' (Water to every field) and improving on-farm water use efficiency to reduce wastage.",
            "benefits": "1. Subsidy for drip and sprinkler irrigation.\n2. Construction of water harvesting structures.\n3. Field-level water application support.",
            "eligibility": "Small and marginal farmers.",
            "link": "https://pmksy.gov.in/",
            "cat": "irrigation",
            "state": ""
        },
        # State Specific (Andhra Pradesh & Telangana)
        {
            "name": "YSR Jala Kala",
            "desc": "A welfare scheme providing free borewells to needy and eligible farmers in all 13 districts of Andhra Pradesh.",
            "benefits": "1. Free drilling of borewells.\n2. Installation of free submersible pump sets.\n3. Direct support to small/marginal farmers.",
            "eligibility": "Farmers with a minimum landholding of 2.5 acres.",
            "link": "https://ysrjalakala.ap.gov.in/",
            "cat": "financial",
            "state": "Andhra Pradesh"
        },
        {
            "name": "Mission Kakatiya",
            "desc": "A massive program for restoring all the minor irrigation tanks and lakes in Telangana state.",
            "benefits": "1. Increased groundwater recharge.\n2. Improved agricultural productivity.\n3. Restoration of rural ecosystem.",
            "eligibility": "Local communities and ayacut farmers.",
            "link": "https://missionkakatiya.cgg.gov.in/",
            "cat": "infrastructure",
            "state": "Telangana"
        },
        {
            "name": "Mission Bhagiratha",
            "desc": "Providing safe drinking water to every household in the state through an extensive grid of pipelines.",
            "benefits": "1. 100 liters of water per person in villages.\n2. Treated surface water for health safety.\n3. Sustainable water grid management.",
            "eligibility": "All households in Telangana.",
            "link": "https://missionbhagiratha.telangana.gov.in/",
            "cat": "infrastructure",
            "state": "Telangana"
        }
    ]

    print("--- Starting Schemes Seeding ---")
    for s in schemes_data:
        scheme, created = WaterScheme.objects.update_or_create(
            name=s['name'],
            defaults={
                'description': s['desc'],
                'benefits': s['benefits'],
                'eligibility': s['eligibility'],
                'application_link': s['link'],
                'category': s['cat'],
                'state_specific': s['state']
            }
        )
        if created:
            print(f"Created Scheme: {s['name']}")
    print("--- Seeding Complete ---")

if __name__ == "__main__":
    seed_schemes()