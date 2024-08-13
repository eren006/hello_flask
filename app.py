from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlitecloud


app = Flask(__name__)


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
        user = conn.execute('SELECT * FROM User WHERE UserID = ?', (username,)).fetchone()
        conn.close()
        if user and user['name'] == password:
            session['user_id'] = user['user_id']  # Store user_id in session
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
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
        selected_interests = request.form.getlist('interests')

        interests_str = ','.join(selected_interests)

        conn = get_db_connection()
        # Insert user records here (Different Format as to what's in the database, will discuss tomorrow)
        conn.execute('INSERT INTO user_profiles (user_id, password, name, age, gender, gender_preference, location, interests) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                     (user_id, password, name, age, gender, gender_preference, province, city, interests_str))
        conn.commit()
        conn.close()

        flash('Profile created successfully!', 'success')
        return redirect(url_for('login'))

    return render_template('create.html', interests=predefined_interests)

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access your dashboard.', 'danger')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM user_profiles WHERE user_id = ?', (session['user_id'],)).fetchone()
    conn.close()
    
    if user:
        profile = {
            "User ID": user["user_id"],
            "Name": user["name"],
            "Age": user["age"],
            "Gender": user["gender"],
            "Gender Preference": user["gender_preference"],
            "Location": user["location"],
            "Interests": user["interests"].split(',')
        }
        return render_template('dashboard.html', profile=profile)
    else:
        flash('User not found.', 'danger')
        return redirect(url_for('login'))
    
@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:
        flash('Please log in to access your profile.', 'danger')
        return redirect(url_for('login'))
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM user_profiles WHERE user_id = ?', (session['user_id'],)).fetchone()

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
        new_interests = ','.join(request.form.getlist('interests'))

        conn.execute('''UPDATE user_profiles SET name = ?, age = ?, gender = ?, gender_preference = ?, province = ?, city = ?, smoking = ?, drinking = ?, languages = ?, interests = ? WHERE user_id = ?''',
                     (new_name, new_age, new_gender, new_gender_preference, new_province, new_city, new_smoking, new_drinking, new_languages, new_interests, session['user_id']))
        conn.commit()
        conn.close()

        flash('Profile updated successfully!', 'success')
        return redirect(url_for('dashboard'))

    conn.close()
    return render_template('edit_profile.html', profile=user)

@app.route('/matching')
def matching():
    if 'user_id' not in session:
        flash('Please log in to perform matching.', 'danger')
        return redirect(url_for('login'))

    # Logic for matching would go here (e.g., fetching potential matches based on preferences)
    # For now, we just render a placeholder page
    return render_template('matching.html')

    return render_template('dashboard.html', profile=profile)


if __name__ == '__main__':
    app.run(debug=True)
