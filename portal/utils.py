import base64

def calculate_water_requirement(land_size, crop_type, season):
    """
    Calculates estimated water requirement for the Water Resource Planner[cite: 104, 111].
    Rule-based logic suitable for B.Tech level.
    """
    # Base requirements (in liters per acre per day - dummy estimates)
    crop_weights = {
        'rice': 5000, 'wheat': 2500, 'maize': 3000, 
        'sugarcane': 6000, 'vegetables': 2000
    }
    
    season_multipliers = {
        'summer': 1.5, 'monsoon': 0.5, 'winter': 1.0
    }
    
    base = crop_weights.get(crop_type.lower(), 2500)
    multiplier = season_multipliers.get(season.lower(), 1.0)
    
    total_daily = land_size * base * multiplier
    
    # Shortage Risk Assessment [cite: 112]
    risk_level = 'Low'
    if multiplier > 1.2: risk_level = 'High'
    elif multiplier > 0.8: risk_level = 'Medium'
    
    return total_daily, risk_level

def classify_groundwater_status(extraction_percentage):
    """
    Classifies groundwater condition based on extraction levels[cite: 85, 90].
    Categories: Safe, Semi-Critical, Critical, Over-Exploited.
    """
    if extraction_percentage > 100:
        return 'Over-Exploited', 'CRITICAL_RED_GLOW', 'Strict extraction limits required.'
    elif extraction_percentage > 90:
        return 'Critical', 'ORANGE_ALERT', 'High extraction detected. Monitor usage.'
    elif extraction_percentage > 70:
        return 'Semi-Critical', 'YELLOW_CAUTION', 'Moderate extraction. Resource under stress.'
    
    return 'Safe', 'GREEN_NORMAL', 'Water levels are within safe limits.'

def check_water_safety(source_type, location_hazard_level='Low'):
    """
    Checks if groundwater is safe for drinking[cite: 116, 121].
    Inputs: Location data and water source type[cite: 118, 119].
    """
    # Simple logic-based safety check [cite: 115]
    if source_type.lower() == 'open well' or location_hazard_level == 'High':
        return 'Unsafe', 'Possible contamination. Boiling or filtration mandatory.' [cite: 122, 123]
    
    return 'Safe', 'Generally safe for drinking, but regular testing is recommended.' [cite: 99]