from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key')

# Set up Flask-SocketIO
socketio = SocketIO(app)

@app.route('/')
def index():
    # Serve the index.html template with a link to the login page
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login logic here if needed
        username = request.form.get('username')
        password = request.form.get('password')
        print(f"Username: {username}, Password: {password}")  # For debugging
        return "Login successful!"  # Replace with appropriate logic
    return render_template('login.html')

@app.route('/welcome')
def welcome():
    # Serve a welcome message
    return "Welcome to the Website!"

if __name__ == '__main__':
    socketio.run(app, debug=True)
