from flask import Flask, render_template, request, redirect, url_for, flash
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
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard', username=username))
        else:
            flash('Invalid credentials, please try again.', 'danger')
    return render_template('login.html')

@app.route('/create', methods=['GET', 'POST'])
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
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        gender_preference = request.form['gender_preference']
        location = request.form['location']
        selected_interests = request.form.getlist('interests')

        # Validation
        if len(user_id) < 1 or len(user_id) > 16:
            flash('User ID must be between 1 and 16 characters.', 'danger')
            return render_template('create.html', interests=predefined_interests)

        conn = get_db_connection()
        existing_user = conn.execute('SELECT * FROM user_profiles WHERE user_id = ?', (user_id,)).fetchone()
        if existing_user:
            flash('User ID already exists. Please choose another.', 'danger')
            conn.close()
            return render_template('create.html', interests=predefined_interests)

        # Convert selected interests to a comma-separated string
        interests_str = ','.join(selected_interests)

        conn.execute('INSERT INTO user_profiles (user_id, name, age, gender, gender_preference, location, interests) VALUES (?, ?, ?, ?, ?, ?, ?)',
                     (user_id, name, age, gender, gender_preference, location, interests_str))
        conn.commit()
        conn.close()

        flash('Profile created successfully!', 'success')
        return redirect(url_for('login'))

    return render_template('create.html', interests=predefined_interests)


    return render_template('create.html', interests=predefined_interests)

@app.route('/dashboard/<username>')
def dashboard(username):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM user_profiles WHERE user_id = ?', (username,)).fetchone()
    conn.close()
    if user:
        profile = {
            "Name": user["name"],
            "Age": user["age"],
            "Gender": user["gender"],
            "Location": user["location"],
            "Interests": user["interests"].split(',')
        }
        return render_template('dashboard.html', username=username, profile=profile)
    else:
        flash('Please log in to access the dashboard.', 'danger')
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
