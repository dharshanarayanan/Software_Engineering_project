from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, emit
import os
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key')

# Set up Flask-SocketIO
socketio = SocketIO(app)

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html')
    return redirect(url_for('show_login'))

if __name__ == '__main__':
    socketio.run(app, debug=True)