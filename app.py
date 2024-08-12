from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db_connection():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
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
        user = conn.execute('SELECT * FROM user_profiles WHERE user_id = ?', (username,)).fetchone()
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
        'Traveling', 'Playing the piano', 'Photography', 'Cooking', 'Watching movies',
        'Dancing', 'Swimming', 'Music', 'Singing', 'Drawing', 'Playing computer games',
        'Hiking', 'Cycling', 'Reading', 'Yoga', 'Painting', 'Gaming', 'Skateboarding',
        'Fitness', 'Basketball', 'Baking', 'Coding', 'Running', 'Writing', 'Chess',
        'Surfing', 'Videography', 'Soccer', 'Gardening', 'Art', 'Boxing', 'Exercising',
        'Crafting', 'Skating', 'Meditation', 'Baseball', 'Badminton', 'Guitar'
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
        conn.execute('INSERT INTO user_profiles (user_id, password, name, age, gender, gender_preference, province, city, interests) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
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

@app.route('/matching')
def matching():
    if 'user_id' not in session:
        flash('Please log in to perform matching.', 'danger')
        return redirect(url_for('login'))

    # Logic for matching would go here (e.g., fetching potential matches based on preferences)
    # For now, we just render a placeholder page
    return render_template('matching.html')

if __name__ == '__main__':
    app.run(debug=True)
