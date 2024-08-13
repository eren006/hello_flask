import numpy as np
import pandas as pd

# Sample DataFrame of users
users = pd.DataFrame({
   'user_id': [1, 2, 3, 4, 5],
   'gender': ['M', 'F', 'M', 'F', 'M'],
   'gender_preference':['F','M','M','F', 'Non-binary'],
   'city': ['NY', 'LA', 'NY', 'NY', 'LA'],
   'age': [25, 30, 25, 25, 35],
   'interests': [['music', 'sports'], ['reading', 'music'], ['sports', 'music'], ['music', 'art'], ['sports', 'art']],
   'smoking_preference': ['No', 'Yes', 'No', 'Yes', 'No'],  # Added for example
   'drinking_preference': ['No', 'Yes', 'No', 'No', 'Yes'],  # Added for example
   'language': [['English'], ['Spanish', 'English'], ['English'], ['French', 'English'], ['Spanish']]  # Added for example
})

def custom_age_score(age_difference):
    if 0 <= age_difference <= 3:
        return 1  # Age difference 1-3 years, full score
    else:
        # Age difference 4 years or more, decreasing score
        max_age_diff = 10  # Adjust this value as needed
        return max(0, 1 - (age_difference - 3) / (max_age_diff - 3))

def compute_score(current_user_id, users):
    current_user = users[users['user_id'] == current_user_id].iloc[0]

    # Prepare scoring results
    scores = []

    # Iterate through other users to compute scores
    for _, potential_match in users[users['user_id'] != current_user_id].iterrows():
        # Gender Preference
        gender_score = 1 if current_user['gender_preference'] == potential_match['gender'] else 0

        # Smoking Preference
        smoking_score = 1 if current_user['smoking_preference'] == potential_match['smoking_preference'] else -1

        # Drinking Preference
        drinking_score = 1 if current_user['drinking_preference'] == potential_match['drinking_preference'] else -1

        # Location
        location_score = 1 if current_user['city'] == potential_match['city'] else 0

        # Interests (Jaccard similarity)
        intersection = len(set(current_user['interests']) & set(potential_match['interests']))
        union = len(set(current_user['interests']) | set(potential_match['interests']))
        interest_score = intersection / union if union != 0 else 0

        # Language Preference (Jaccard similarity)
        language_intersection = len(set(current_user['language']) & set(potential_match['language']))
        language_union = len(set(current_user['language']) | set(potential_match['language']))
        language_score = language_intersection / language_union if language_union != 0 else 0

        # Age
        age_difference = abs(current_user['age'] - potential_match['age'])
        age_score = custom_age_score(age_difference)
        
        # Like/Dislike Adjustments
        like_adjustment = 0.05 * len(potential_match_obj.liked_users)
        dislike_adjustment = -0.05 * len(potential_match_obj.disliked_users)
        
        # Weighted Score
        if gender_score == 0:
            total_score = 0
        else:
            total_score = float(round(0.4 * interest_score + 0.2 * age_score + 
                                      0.1 * location_score + 0.1 * language_score + 
                                      0.1 * smoking_score + 0.1 * drinking_score +
                                      like_adjustment + dislike_adjustment,2))

        scores.append((potential_match['user_id'], total_score))

    # Sort users by score in descending order
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    return sorted_scores

# Example usage for user 1
user_id = 1
sorted_matches = compute_score(user_id, users)
print(f"Match scores for user {user_id}:", sorted_matches)