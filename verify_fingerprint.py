import serial
import base64
from pymongo import MongoClient

# MongoDB connection
client = MongoClient("mongodb+srv://dharshan:saymyname@cluster0.hh0vx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.get_database('fingerprint')  
users_collection = db.login  

# Serial Communication with Galileo
SERIAL_PORT = "COM5"  # Change as needed
BAUD_RATE = 115200
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=5)

print(f"Listening on {SERIAL_PORT} for fingerprint verification...")

while True:
    input("Press Enter to scan fingerprint...")

    ser.write(b"BEGIN_VERIFY\n")
    data = ""

    while True:
        line = ser.readline().decode('utf-8').strip()
        if line == "END_VERIFY":
            break
        data += line

    # Check if the fingerprint exists in MongoDB
    stored_fingerprints = users_collection.find({})
    match_found = False

    for user in stored_fingerprints:
        if user['fingerprint_template'] == data:
            print(f"✅ ACCESS GRANTED! User ID: {user['user_id']}")
            match_found = True
            break

    if not match_found:
        print("❌ ACCESS DENIED! No matching fingerprint found.")
