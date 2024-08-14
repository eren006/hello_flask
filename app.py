from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlitecloud
import numpy as np
import pandas as pd


app = Flask(__name__)
app.secret_key = 'flask'


def get_db_connection():
    db_name = 'dating_app_test2'
    # Open the connection to SQLite Cloud
    conn = sqlitecloud.connect("sqlitecloud://cbgnacvcik.sqlite.cloud:8860?apikey=Mx2cK8ScRiNgZl31SFhJCezNWBXAtRBbtsdvvBVA5xw")
    conn.execute(f"USE DATABASE {db_name}")
    print("DB connection has been established ")

    return conn

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM user WHERE UserId = ? AND password = ?", (username, password)).fetchone()
        conn.close()
        print(user)
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
    predefined_interests = [
    'Art', 'Badminton', 'Baking', 'Baseball', 'Basketball', 'Boxing', 'Chess',
    'Coding', 'Cooking', 'Crafting', 'Cycling', 'Dancing', 'Drawing', 'Exercising',
    'Fitness', 'Gaming', 'Gardening', 'Guitar', 'Hiking', 'Meditation', 'Music',
    'Painting', 'Photography', 'Playing computer games', 'Playing the piano',
    'Reading', 'Running', 'Singing', 'Skateboarding', 'Skating', 'Soccer',
    'Surfing', 'Swimming', 'Traveling', 'Videography', 'Watching movies', 'Writing', 'Yoga'
]


    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        gender_preference = request.form['gender_preference']
        province = request.form['province']
        city = request.form['city']
        smoking = request.form['smoking']== 'true' 
        drinking = request.form['drinking']== 'true' 
        languages = request.form.getlist('languages')
        selected_interests = request.form.getlist('interests')
        if smoking == True:
            selected_interests.append('smoking')
        if drinking == True:
            selected_interests.append('drinking')
        interests_str = ','.join(selected_interests)
        languages_str= ','.join(languages)
        conn = get_db_connection()
        conn.execute('''INSERT INTO User 
               (UserID, password, name, age, gender, gender_preference, location, interests,languages) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
               (user_id, password, name, age, gender, gender_preference, city, interests_str,languages_str))
        conn.commit()
        conn.close()
        print("Profile created successfully!!")
        flash('Profile created successfully!', 'success')
        return redirect(url_for('login'))

    return render_template('create.html', interests=predefined_interests)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access your dashboard.', 'danger')
        return redirect(url_for('login'))

    conn = get_db_connection()
    
    # Fetch the user's profile
    user = conn.execute('SELECT * FROM User WHERE UserID = ?', (session['user_id'],)).fetchone()

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

        # Fetch the list of liked users
        liked_users = conn.execute('''SELECT UserID, Name FROM User
                                      WHERE UserID IN (SELECT UserB FROM Records WHERE UserA = ? AND Liked = 1)''',
                                      (session['user_id'],)).fetchall()

        # Fetch the list of disliked users
        disliked_users = conn.execute('''SELECT UserID, Name FROM User
                                         WHERE UserID IN (SELECT UserB FROM Records WHERE UserA = ? AND Disliked = 1)''',
                                         (session['user_id'],)).fetchall()
        
        # Fetch the list of matched users
        matched_users = conn.execute('''SELECT UserID, Name, Age, Gender, Gender_Preference, Location, Languages, Interests FROM User
                                        WHERE UserID IN (SELECT UserB FROM Records WHERE UserA = ? AND Match = 1)''',
                                        (session['user_id'],)).fetchall()
        

        conn.close()

        # Count the number of likes, dislikes, and matches
        likes_count = len(liked_users)
        dislikes_count = len(disliked_users)

        return render_template('dashboard.html', profile=profile, likes_count=likes_count, dislikes_count=dislikes_count, matched_users=matched_users)
    else:
        conn.close()
        flash('User not found.', 'danger')
        return redirect(url_for('login'))


    
@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
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
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM User WHERE userID = ?', (session['user_id'],)).fetchone()

    if request.method == 'POST':
        # Process the form data and update the user's profile in the database
        new_name = request.form['name']
        new_age = request.form['age']
        new_gender = request.form['gender']
        new_gender_preference = request.form['gender_preference']
        new_province = request.form['province']
        new_city = request.form['city']
        new_smoking = request.form['smoking']
        new_drinking = request.form['drinking']
        new_languages = ','.join(request.form.getlist('languages'))
        
        if new_smoking == True:
            new_interests.append('smoking')
        if new_drinking == True:
            new_interests.append('drinking')
        new_interests = ','.join(request.form.getlist('interests'))
        conn.execute('''UPDATE User SET name = ?, age = ?, gender = ?, gender_preference = ?, location = ?, languages = ?, interests = ? WHERE UserID = ?''',
                     (new_name, new_age, new_gender, new_gender_preference,new_city,new_languages, new_interests, session['user_id']))
        conn.commit()
        conn.close()
        print("Profile updated successfully!")
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('dashboard'))

    conn.close()
    return render_template('edit_profile.html', profile=user, interests=predefined_interests)

def custom_age_score(age_difference):
    if 0 <= age_difference <= 3:
        return 1
    else:
        max_age_diff = 10
        return max(0, 1 - (age_difference - 3) / (max_age_diff - 3))

def compute_score(current_user_id, users):
    # Convert the 'Age' column to integers
    users['Age'] = users['Age'].astype(int)
    current_user = users[users['UserID'] == current_user_id].iloc[0]

    scores = []
    for _, potential_match in users[users['UserID'] != current_user_id].iterrows():
        gender_score = 1 if current_user['Gender_Preference'] == potential_match['Gender'] else 0
        # smoking_score = 1 if current_user['smoking_preference'] == potential_match['smoking_preference'] else -1
        # drinking_score = 1 if current_user['drinking_preference'] == potential_match['drinking_preference'] else -1
        location_score = 1 if current_user['Location'] == potential_match['Location'] else 0

        intersection = len(set(current_user['Interests']) & set(potential_match['Interests']))
        union = len(set(current_user['Interests']) | set(potential_match['Interests']))
        interest_score = intersection / union if union != 0 else 0

        language_intersection = len(set(current_user['Languages']) & set(potential_match['Languages']))
        language_union = len(set(current_user['Languages']) | set(potential_match['Languages']))
        language_score = language_intersection / language_union if language_union != 0 else 0

        age_difference = abs(current_user['Age'] - potential_match['Age'])
        age_score = custom_age_score(age_difference)
        
        like_adjustment = 0.05 * len(potential_match.liked_users)
        dislike_adjustment = -0.05 * len(potential_match.disliked_users)

        if gender_score == 0:
            total_score = 0
        else:
            total_score = float(round(0.4 * interest_score + 0.2 * age_score + 
                                      0.1 * location_score + 0.1 * language_score + 
                                      #0.1 * smoking_score + 0.1 * drinking_score +
                                      + like_adjustment + dislike_adjustment, 2))

        scores.append((potential_match['UserID'], total_score))

    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
    return sorted_scores

@app.route('/matching', methods=['GET'])
def matching():
    if 'user_id' not in session:
        flash('Please log in to access the matching page.', 'danger')
        return redirect(url_for('login'))

    current_user_id = session['user_id']
    print("Current User ID:", current_user_id)

    conn = get_db_connection()
    users = pd.read_sql('SELECT * FROM User', conn)
    # print(users)
    # Fetch list of other_user_ids that have already been interacted with by the current user (UserA)
    interacted_users_query = " SELECT UserB FROM Records WHERE UserA = '{}'".format(current_user_id)
    interacted_users = pd.read_sql(interacted_users_query, conn)
    interacted_user_ids_list=interacted_users['UserB'].tolist()
    # Convert the list of interacted user IDs to a set for easy lookup
    interacted_user_ids = set(interacted_user_ids_list)
    # Filter out users who have already been interacted with
    users = users[~users['UserID'].isin(interacted_user_ids)]
    conn.close()

    sorted_matches = compute_score(current_user_id, users)
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
    user_id = session['user_id']
    liked_user_id = request.form['liked_user_id']

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if there is a record (0, 1, 0, liked_user_id, user_id) in the Records table
    cursor.execute('''SELECT * FROM Records WHERE Match = 0 AND Liked = 1 AND Disliked = 0 AND UserA = ? AND UserB = ?''', 
                   (liked_user_id, user_id))
    existing_record = cursor.fetchone()

    if existing_record:
        # If there is a matching record, insert with Match = 1
        cursor.execute('''UPDATE Records 
                          SET Match = 1
                          WHERE Match = 0 AND Liked = 1 AND Disliked = 0 AND UserA = ? AND UserB = ?''', 
                       (liked_user_id, user_id))
        cursor.execute('''INSERT INTO Records (Match, Liked, Disliked, UserA, UserB)
                          VALUES (1, 1, 0, ?, ?)''', 
                       (user_id, liked_user_id))
    else:
        # Otherwise, insert with Match = 0
        cursor.execute('''INSERT INTO Records (Match, Liked, Disliked, UserA, UserB)
                          VALUES (0, 1, 0, ?, ?)''', 
                       (user_id, liked_user_id))

    conn.commit()
    conn.close()

    return redirect(url_for('matching'))

@app.route('/dislike', methods=['POST'])
def dislike():
    user_id = session['user_id']
    disliked_user_id = request.form['liked_user_id']

    conn = get_db_connection()
    conn.execute('''INSERT INTO Records (Match, Liked, Disliked,UserA, UserB)
                    VALUES (0, 0, 1, ?, ?)''', (user_id, disliked_user_id))
    conn.commit()
    conn.close()

    return redirect(url_for('matching'))


def delete(userID):
    conn = get_db_connection()
    conn.execute(''' DELETE FROM records WHERE userA = ? OR userB = ? ''',(userID,userID))
    conn.execute(''' DELETE FROM User WHERE UserID = ? ''',(userID))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    app.run(debug=True)