from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import DatabaseManager
import numpy as np
import pandas as pd



app = Flask(__name__)
app.secret_key = 'flask'

# Create an instance of the DatabaseManager class
db_manager = DatabaseManager(db_name='dating_app_test2')

@app.route('/')
def home():
    """
    Redirects users to the login page.

    Returns:
        flask.Response: A redirection to the login page.
    """
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles user authentication. Users provide their `username` and `password`,
    which are checked against the `User` table in the database.

    Methods:
        GET: Renders the login form.
        POST: Authenticates the user and redirects to the dashboard.

    Returns:
        flask.Response: The rendered login page (GET) or a redirection to the dashboard (POST).
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        query = "SELECT * FROM user WHERE UserId = ? AND password = ?"
        params=(username,password)
        user = db_manager.fetch_one(query=query,params=params)
        print("User is: ",user)
        if user:
            print("Login successfull!")
            session['user_id'] = user[4]
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            print("Login unsuccessfull :(")
            flash('Invalid credentials, please try again.', 'danger')
    return render_template('login.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    """
    Allows new users to create a profile by submitting their details. The user's 
    profile data is stored in the `User` table in the database.

    Methods:
        GET: Renders the user creation form.
        POST: Processes the form submission and stores the new user in the database.
    """
    predefined_interests = [
        'Art', 'Badminton', 'Baking', 'Baseball', 'Basketball', 'Boxing', 'Chess',
        'Coding', 'Cooking', 'Crafting', 'Cycling', 'Dancing', 'Drawing', 'Exercising',
        'Fitness', 'Gaming', 'Gardening', 'Guitar', 'Hiking', 'Meditation', 'Music',
        'Painting', 'Photography', 'Playing computer games', 'Playing the piano',
        'Reading', 'Running', 'Singing', 'Skateboarding', 'Skating', 'Soccer',
        'Surfing', 'Swimming', 'Traveling', 'Videography', 'Watching movies', 'Writing', 'Yoga'
    ]

    message = None
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        gender_preference = request.form['gender_preference']
        province = request.form['province']
        city = request.form['city']
        smoking = request.form['smoking'] == 'true'
        drinking = request.form['drinking'] == 'true'
        languages = request.form.getlist('languages')
        selected_interests = request.form.getlist('interests')
        if smoking:
            selected_interests.append('smoking')
        if drinking:
            selected_interests.append('drinking')
        interests_str = ','.join(selected_interests)
        languages_str = ','.join(languages)

        # Check if the user ID already exists
        query = "SELECT * FROM User WHERE UserID = ?"
        params = (user_id,)
        existing_user = db_manager.fetch_one(query=query, params=params)
        
        if existing_user:
            message = 'User ID already exists. Please choose a different User ID.'
            return render_template('create.html', interests=predefined_interests, message=message)
        
        # If user ID does not exist, proceed to create the profile
        query = "INSERT INTO User (UserID, password, name, age, gender, gender_preference, location, interests, languages) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        location = f"{province}, {city}"
        params = (user_id, password, name, age, gender, gender_preference, location, interests_str, languages_str)
        db_manager.execute_query(query=query, params=params)
        
        message = 'Profile created successfully!'
        return render_template('create.html', interests=predefined_interests, message=message)

    return render_template('create.html', interests=predefined_interests)


@app.route('/dashboard')
def dashboard():
    """
    Displays the logged-in user's profile information and lists the users 
    they have liked and matched with. Retrieves the relevant data from the `User`
    and `Records` tables.

    Returns:
        flask.Response: The rendered dashboard page with the user's profile information and interactions.
    """
    if 'user_id' not in session:
        flash('Please log in to access your dashboard.', 'danger')
        return redirect(url_for('login'))

    query = "SELECT * FROM User WHERE UserID = ?"
    params = (session['user_id'],)
    user = db_manager.fetch_one(query=query,params=params)

    if user:
        profile = {
            "User ID": user[4],
            "Name": user[3],
            "Age": user[0],
            "Gender": user[1],
            "Gender_Preference": user[7],
            "Location": user[2],
            "Languages": user[8].split(','),
            "Interests": user[5].split(',')
        }

        query = "SELECT UserID, Name FROM User WHERE UserID IN (SELECT UserA FROM Records WHERE UserB = ? AND Liked = 1)"
        params = (session['user_id'],)
        liked_users = db_manager.fetch_all(query=query,params=params)
        
        query = "SELECT UserID, Name, Age, Gender, Gender_Preference, Location, Languages, Interests FROM User WHERE UserID IN (SELECT UserB FROM Records WHERE UserA = ? AND Match = 1)"
        params = (session['user_id'],)
        matched_users = db_manager.fetch_all(query=query,params=params)
        
        # Count the number of likes
        likes_count = len(liked_users)

        return render_template('dashboard.html', profile=profile, likes_count=likes_count, matched_users=matched_users)
    else:
        print("User not found")
        flash('User not found.', 'danger')
        return redirect(url_for('login'))


    
@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    """
    Allows the logged-in user to update their profile information, including name, age, 
    gender, preferences, and interests. The updated data is saved in the `User` table.

    Methods:
        GET: Renders the profile edit form.
        POST: Processes the form submission and updates the user's profile in the database.

    Returns:
        flask.Response: The rendered profile edit page (GET) or a redirection to the dashboard (POST).
    """

    predefined_interests = [
    'Art', 'Badminton', 'Baking', 'Baseball', 'Basketball', 'Boxing', 'Chess',
    'Coding', 'Cooking', 'Crafting', 'Cycling', 'Dancing', 'Drawing', 'Exercising',
    'Fitness', 'Gaming', 'Gardening', 'Guitar', 'Hiking', 'Meditation', 'Music',
    'Painting', 'Photography', 'Playing computer games', 'Playing the piano',
    'Reading', 'Running', 'Singing', 'Skateboarding', 'Skating', 'Soccer',
    'Surfing', 'Swimming', 'Traveling', 'Videography', 'Watching movies', 'Writing', 'Yoga'
]
    if 'user_id' not in session:
        flash('Please log in to access your profile.', 'danger')
        return redirect(url_for('login'))
    
    query = "SELECT * FROM User WHERE userID = ?"
    params = (session['user_id'],)
    user = db_manager.fetch_one(query=query,params=params)
    print(user)

    if request.method == 'POST':
        # Process the form data and update the user's profile in the database
        new_name = request.form['name']
        new_age = request.form['age']
        new_gender = request.form['gender']
        new_gender_preference = request.form['gender_preference']
        new_city = request.form['city']
        new_smoking = request.form['smoking']
        new_drinking = request.form['drinking']
        new_languages = ','.join(request.form.getlist('languages'))
        
        if new_smoking == True:
            new_interests.append('smoking')
        if new_drinking == True:
            new_interests.append('drinking')
        new_interests = ','.join(request.form.getlist('interests'))
        query = "UPDATE User SET name = ?, age = ?, gender = ?, gender_preference = ?, location = ?, languages = ?, interests = ? WHERE UserID = ?"
        params = (new_name, new_age, new_gender, new_gender_preference,new_city,new_languages, new_interests, session['user_id'])
        db_manager.execute_query(query=query,params=params)
        print("Profile updated successfully!")
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('edit_profile.html', profile=user, interests=predefined_interests)

def custom_age_score(age_differences):
    """
    Calculates a score based on the age difference between users. The smaller the age difference,
    the higher the score.

    Parameters:
        age_difference (int): The difference in age between two users.

    Returns:
        float: The calculated score for the given age difference.
    """
    age_scores = np.zeros_like(age_differences, dtype=float)
    
    age_scores[(age_differences >= 0) & (age_differences <= 3)] = 1.0
    age_scores[(age_differences > 3)] = 1.0 - (age_differences[(age_differences > 3)] * 0.1)  
    
    age_scores[age_scores < 0] = 0

    return age_scores

def compute_score(current_user_id, users,liked_users,disliked_users):
    """
    Computes the matching score between a user and a potential match by considering various
    factors such as interests, location, language preferences, and age difference.

    Parameters:
        user (pandas.Series): The current user's data.
        potential_match (pandas.Series): The potential match's data.

    Returns:
        float: The calculated matching score.
    """
    # Convert the 'Age' column to integers
    users['Age'] = users['Age'].astype(int)
    current_user = users[users['UserID'] == current_user_id].iloc[0]
    potential_matches = users[users['UserID'] != current_user_id].copy()
    gender_scores = (current_user['Gender_Preference'] == potential_matches['Gender']).astype(int)
    location_scores = (current_user['Location'] == potential_matches['Location']).astype(int)
    interest_scores = potential_matches['Interests'].apply(
        lambda x: len(set(current_user['Interests']) & set(x)) / len(set(current_user['Interests']) | set(x))
        if len(set(current_user['Interests']) | set(x)) > 0 else 0
    )
    language_scores = potential_matches['Languages'].apply(
        lambda x: len(set(current_user['Languages']) & set(x)) / len(set(current_user['Languages']) | set(x))
        if len(set(current_user['Languages']) | set(x)) > 0 else 0
    )
    age_differences = np.abs(potential_matches['Age'] - current_user['Age'])
    age_scores = custom_age_score(age_differences)
    like_adjustment = 0.05 * len(liked_users)
    dislike_adjustment = -0.05 * len(disliked_users)
    total_scores = (0.4 * interest_scores + 0.2 * age_scores + 
                    0.1 * location_scores + 0.1 * language_scores + 
                    like_adjustment + dislike_adjustment)
    total_scores = np.where(gender_scores == 0, 0, total_scores)
    scores = list(zip(potential_matches['UserID'], np.round(total_scores, 2)))
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)

    return sorted_scores

@app.route('/matching', methods=['GET'])
def matching():
    """
    Displays a potential match for the logged-in user by filtering out users they've already 
    interacted with and ranking the remaining users using the scoring algorithm.

    Returns:
        flask.Response: The rendered matching page with the top potential match.
    """
    if 'user_id' not in session:
        flash('Please log in to access the matching page.', 'danger')
        return redirect(url_for('login'))

    current_user_id = session['user_id']
    print("Current User ID:", current_user_id)

    conn = db_manager.get_db_connection()
    users = pd.read_sql('SELECT * FROM User', conn)

    # Fetch list of other_user_ids that have already been interacted with by the current user (UserA)
    interacted_users_query = " SELECT UserB FROM Records WHERE UserA = '{}'".format(current_user_id)
    interacted_users = pd.read_sql(interacted_users_query, conn)
    interacted_user_ids_list=interacted_users['UserB'].tolist()
    
    # Convert the list of interacted user IDs to a set for easy lookup
    interacted_user_ids = set(interacted_user_ids_list)
    
    # Filter out users who have already been interacted with
    users = users[~users['UserID'].isin(interacted_user_ids)]
    conn.close()

    query = "SELECT UserID, Name FROM User WHERE UserID IN (SELECT UserB FROM Records WHERE UserA = ? AND Liked = 1)"
    params = (current_user_id,)
    liked_users = db_manager.fetch_all(query=query,params=params)
    
    query = "SELECT UserID, Name FROM User WHERE UserID IN (SELECT UserB FROM Records WHERE UserA = ? AND Disliked = 1)"
    params = (current_user_id,)
    disliked_users = db_manager.fetch_all(query=query,params=params)

    sorted_matches = compute_score(current_user_id, users,liked_users, disliked_users)
    print("Sorted Matches:", sorted_matches)

    if sorted_matches:
        top_match_id = sorted_matches[0][0]
        match_profile = users[users['UserID'] == top_match_id].iloc[0].to_dict()
        match_profile['Languages'] = match_profile['Languages'].split(',')
        match_profile['Interests'] = match_profile['Interests'].split(',')
        print("Match Profile:", match_profile)
    else:
        match_profile = None
        print("No matches found.")

    return render_template('matching.html', match_profile=match_profile)


@app.route('/like', methods=['POST'])
def like():
    """
    Handles the "like" interaction between the logged-in user and a potential match. 
    If the other user has also liked the current user, the match is recorded in the `Records` table.

    Parameters:
        match_user_id (str): The UserID of the user being liked.

    Returns:
        flask.Response: A redirection to the matching page.
    """
    user_id = session['user_id']
    liked_user_id = request.form['liked_user_id']
    
    query = "SELECT * FROM Records WHERE Match = 0 AND Liked = 1 AND Disliked = 0 AND UserA = ? AND UserB = ?"
    params =  (liked_user_id, user_id)
    existing_record = db_manager.fetch_one(query=query,params=params)

    if existing_record:
        query = "UPDATE Records SET Match = 1 WHERE Match = 0 AND Liked = 1 AND Disliked = 0 AND UserA = ? AND UserB = ?"
        params = (liked_user_id, user_id)
        db_manager.execute_query(query=query,params=params)
        
        query = "INSERT INTO Records (Match, Liked, Disliked, UserA, UserB) VALUES (1, 1, 0, ?, ?)"
        params = (user_id, liked_user_id)
        db_manager.execute_query(query=query,params=params)
    else:
        query = "INSERT INTO Records (Match, Liked, Disliked, UserA, UserB) VALUES (0, 1, 0, ?, ?)"
        params = (user_id, liked_user_id)
        db_manager.execute_query(query=query,params=params)

    return redirect(url_for('matching'))

@app.route('/dislike', methods=['POST'])
def dislike():
    """
    Handles the "dislike" interaction between the logged-in user and a potential match by 
    recording the interaction in the `Records` table.

    Parameters:
        match_user_id (str): The UserID of the user being disliked.

    Returns:
        flask.Response: A redirection to the matching page.
    """
    user_id = session['user_id']
    disliked_user_id = request.form['liked_user_id']
    
    query = "INSERT INTO Records (Match, Liked, Disliked,UserA, UserB)VALUES (0, 0, 1, ?, ?)"
    params = (user_id, disliked_user_id)
    db_manager.execute_query(query=query,params=params)
    

    return redirect(url_for('matching'))

@app.route('/delete', methods=['POST'])
def delete():
    """
    Deletes the logged-in user's profile and all related interactions from the `User` 
    and `Records` tables. The user is also logged out by clearing the session.

    Returns:
        flask.Response: A redirection to the login page after deletion.
    """
    userID = session['user_id']
    session.clear()
    
    query = "DELETE FROM records WHERE userA = ? OR userB = ?"
    params = (userID,userID)
    db_manager.execute_query(query=query,params=params)
    
    query = "DELETE FROM User WHERE UserID = ?"
    params = (userID,)
    db_manager.execute_query(query=query,params=params)

    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    """
    Logs the user out by clearing the session and redirects to the login page.
    """
    session.clear()  # Clear all session data
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)