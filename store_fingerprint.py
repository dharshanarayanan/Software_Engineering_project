import serial
import base64
import os
from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongodb+srv://dharshan:saymyname@cluster0.hh0vx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.get_database('fingerprint')  
users_collection = db.login  

# Serial Communication with Galileo
SERIAL_PORT = "COM5"  # Change as needed
BAUD_RATE = 115200
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=5)

print(f"Listening on {SERIAL_PORT} for fingerprint data...")

while True:
    line = ser.readline().decode('utf-8').strip()

    if line == "BEGIN_TEMPLATE":
        print("Receiving fingerprint template...")
        data = ""

        while True:
            line = ser.readline().decode('utf-8').strip()
            if line == "END_TEMPLATE":
                break
            data += line

        # Save to MongoDB
        user_id = input("Enter User ID: ")  # Assign an ID
        user_data = {
            "user_id": user_id,
            "fingerprint_template": data
        }
        users_collection.insert_one(user_data)

        print(f"✅ Fingerprint stored for User ID: {user_id}")
