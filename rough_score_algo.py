import pandas as pd
import numpy as np

# Sample DataFrame of users
users = pd.DataFrame({
    'user_id': [1, 2, 3, 4, 5],
    'gender': ['M', 'F', 'M', 'F', 'M'],
    'city': ['NY', 'LA', 'NY', 'NY', 'LA'],
    'age': [25, 30, 22, 28, 35],
    'interests': [['music', 'sports'], ['reading', 'music'], ['sports', 'music'], ['music', 'art'], ['sports', 'art']]
})

# Define user preferences
def compute_score(current_user_id, users):
    current_user = users[users['user_id'] == current_user_id].iloc[0]
    
    # Prepare scoring results
    scores = []

    # Iterate through other users to compute scores
    for _, potential_match in users[users['user_id'] != current_user_id].iterrows():
        # Gender Preference
        gender_score = 1 if current_user['gender'] != potential_match['gender'] else 0
        
        # Location
        location_score = 1 if current_user['city'] == potential_match['city'] else 0
        
        # Interests (Jaccard similarity)
        intersection = len(set(current_user['interests']) & set(potential_match['interests']))
        union = len(set(current_user['interests']) | set(potential_match['interests']))
        interest_score = intersection / union
        
        # Age
        age_difference = abs(current_user['age'] - potential_match['age'])
        age_score = 1 / (1 + age_difference)
        
        # Weighted Score
        total_score = (0.4 * gender_score + 0.3 * location_score + 0.2 * interest_score + 0.1 * age_score)
        
        scores.append((potential_match['user_id'], total_score))

    # Sort users by score in descending order
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    return sorted_scores

# Example usage for user 1
user_id = 1
sorted_matches = compute_score(user_id, users)
print(f"Match scores for user {user_id}:", sorted_matches)
