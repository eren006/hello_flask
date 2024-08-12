from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necessary for flashing messages

# A simple in-memory user database
users = {}

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard', username=username))
        else:
            flash('Invalid credentials, please try again.', 'danger')
    return render_template('login.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        profile = request.form['profile']
        
        if username in users:
            flash('Username already exists, please choose another.', 'danger')
        else:
            users[username] = {'password': password, 'profile': profile}
            flash('Profile created successfully!', 'success')
            return redirect(url_for('login'))
    
    return render_template('create.html')

@app.route('/dashboard/<username>')
def dashboard(username):
    if username in users:
        profile = users[username]['profile']
        return f"Welcome {username}! <br> Your profile: {profile}"
    else:
        flash('Please log in to access the dashboard.', 'danger')
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
