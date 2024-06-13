import pandas as pd
import numpy as np

def calculate_nutrient_profile_score(nutritional_content):

    nutritional_content = {
        'energy': nutritional_content.get('energy-kcal_100g'),
        'saturated_fat': nutritional_content.get('saturated-fat_100g'),
        'sugar': nutritional_content.get('sugars_100g'),
        'sodium': nutritional_content.get('salt_100g'),
        'fruit_veg_nuts': nutritional_content.get('fruits-vegetables-nuts-estimate-from-ingredients_100g'),
        'fibre': nutritional_content.get('fiber_100g'),
        'protein': nutritional_content.get('proteins_100g')
    }

    # Define the nutrient thresholds and points for 'A' and 'C' points
    a_points = {
        'energy': [(335, 1), (670, 2), (1005, 3), (1340, 4), (1675, 5), (2010, 6), (2345, 7), (2680, 8), (3015, 9), (3350, 10)],
        'saturated_fat': [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)],
        'sugar': [(4.5, 1), (9, 2), (13.5, 3), (18, 4), (22.5, 5), (27, 6), (31, 7), (36, 8), (40, 9), (45, 10)],
        'sodium': [(90, 1), (180, 2), (270, 3), (360, 4), (450, 5), (540, 6), (630, 7), (720, 8), (810, 9), (900, 10)]
    }
    
    c_points = {
        'fruit_veg_nuts': [(40, 1), (60, 2), (80, 5)],
        'fibre': [(0.7, 1), (1.4, 2), (2.1, 3), (2.8, 4), (3.5, 5)],
        'protein': [(1.6, 1), (3.2, 2), (4.8, 3), (6.4, 4), (8.0, 5)]
    }
    
    # Calculate 'A' points
    total_a_points = 0
    for nutrient, thresholds in a_points.items():
        value = nutritional_content.get(nutrient, 0)
        for threshold, points in thresholds:
            if value > threshold:
                total_a_points = max(total_a_points, points)
    
    # Calculate 'C' points
    total_c_points = 0
    for nutrient, thresholds in c_points.items():
        value = nutritional_content.get(nutrient, 0)
        for threshold, points in thresholds:
            if value > threshold:
                total_c_points = max(total_c_points, points)
    
    # Calculate overall score
    if total_a_points < 11:
        overall_score = total_a_points - total_c_points
    else:
        if nutritional_content.get('fruit_veg_nuts', 0) >= 5:
            overall_score = total_a_points - total_c_points
        else:
            overall_score = total_a_points - (total_c_points - c_points['protein'])
    
    return overall_score