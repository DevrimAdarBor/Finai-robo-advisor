def calculate_risk_profile(age, investment_horizon, risk_tolerance, investment_knowledge):
    """
    Calculates a risk score and category based on user inputs.
    
    Args:
        age (int): User's age.
        investment_horizon (str): 'Short Term (0-3 years)', 'Medium Term (3-7 years)', 'Long Term (7+ years)'.
        risk_tolerance (str): 'Low', 'Moderate', 'High'.
        investment_knowledge (str): 'None', 'Some', 'Extensive'.
        
    Returns:
        dict: {'score': int, 'risk_level': str, 'description': str}
    """
    score = 0
    
    # Age Score (Younger = Higher Risk Capacity)
    if age < 30:
        score += 10
    elif age < 45:
        score += 7
    elif age < 60:
        score += 4
    else:
        score += 1
        
    # Horizon Score
    if "Long" in investment_horizon:
        score += 10
    elif "Medium" in investment_horizon:
        score += 6
    else:
        score += 2
        
    # Tolerance Score
    if risk_tolerance == "High":
        score += 10
    elif risk_tolerance == "Moderate":
        score += 6
    else:
        score += 2
        
    # Knowledge Score
    if investment_knowledge == "Extensive":
        score += 5
    elif investment_knowledge == "Some":
        score += 3
    else:
        score += 1
        
    # Determine Risk Level
    # Total max score = 10 + 10 + 10 + 5 = 35
    # Total min score = 1 + 2 + 2 + 1 = 6
    
    if score >= 28:
        risk_level = "Aggressive"
        description = "High growth potential with higher volatility. primarily equities and crypto."
    elif score >= 18:
        risk_level = "Moderate"
        description = "Balanced growth and stability. Mix of equities and fixed income."
    else:
        risk_level = "Conservative"
        description = "Focus on capital preservation. Primarily bonds and stable assets."
        
    return {
        "score": score,
        "risk_level": risk_level,
        "description": description
    }
