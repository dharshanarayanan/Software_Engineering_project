from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_socketio import SocketIO
from pymongo import MongoClient
import os
import bcrypt

# Initialize Flask app and secret key
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key')

# Set up Flask-SocketIO
socketio = SocketIO(app)

# MongoDB connection setup
MONGO_URI = "mongodb+srv://dharshan:saymyname@cluster0.hh0vx.mongodb.net/?retryWrites=true&w=majority&authSource=admin&tls=true"
client = MongoClient(MONGO_URI)
db = client['voting_system']
users_collection = db['login']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        # Retrieve user from database
        user = users_collection.find_one({"username": username})

        if user and bcrypt.checkpw(password, user['password']):
            session['username'] = username  # Store in session
            flash("Login successful!", "success")
            return redirect(url_for('voter'))
        else:
            flash("Invalid username or password.", "error")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/voter')
def voter():
    if 'username' in session:
        return render_template('voter.html', username=session['username'])
    else:
        flash("Please log in first.", "error")
        return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        # Check if the username already exists
        existing_user = users_collection.find_one({"username": username})
        if existing_user:
            flash("Username already exists. Please choose another.", "error")
            return redirect(url_for('register'))

        # Hash password before storing
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

        # Insert new user into MongoDB collection
        users_collection.insert_one({"username": username, "password": hashed_password})
        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for('login'))

    return render_template('Registration.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("Logged out successfully!", "info")
    return redirect(url_for('login'))

if __name__ == '__main__':
    socketio.run(app, debug=True)
