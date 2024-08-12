from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necessary for flashing messages

# A simple in-memory user database
users = {
    "admin": "password123"
}

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials, please try again.', 'danger')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return "Welcome to the dashboard!"

if __name__ == '__main__':
    app.run(debug=True)
