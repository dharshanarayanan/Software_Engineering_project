from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_socketio import SocketIO
from pymongo import MongoClient
import os

# Initialize Flask app and secret key
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key')

# Set up Flask-SocketIO
socketio = SocketIO(app)

# MongoDB connection setup
client = MongoClient("mongodb+srv://dharshan:whatsmyname@cluster0.hh0vx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.get_database('voting_system')  # Replace 'user_db' with your database name
users_collection = db.login  # Replace 'users' with your collection name

@app.route('/')
def index():
    # Serve the index.html template with a link to the login page
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Find the user in the MongoDB collection
        user = users_collection.find_one({"username": username})
        if user and user['password'] == password:
            session['username'] = username
            return redirect(url_for('welcome'))
        else:
            flash("Invalid username or password", "error")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Check if the username already exists in the database
        existing_user = users_collection.find_one({"username": username})
        if existing_user:
            flash("Username already exists. Please choose another.", "error")
            return redirect(url_for('register'))

        # Insert new user into MongoDB collection
        users_collection.insert_one({"username": username, "password": password})
        flash("Registration successful! You can now log in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/welcome')
def welcome():
    # Serve a welcome message after successful login
    if 'username' in session:
        return f"Welcome to the Website, {session['username']}!"
    return redirect(url_for('login'))

if __name__ == '__main__':
    socketio.run(app, debug=True)
