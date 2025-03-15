import serial
import base64
import os

# Set your COM port (Windows) or /dev/ttyUSBx (Linux/Mac)
SERIAL_PORT = "COM5"  # Change as needed
BAUD_RATE = 115200

ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=5)

# Ensure the directory exists
save_dir = r"D:\amrita\software\Software_Engineering_project\fingerprint"
os.makedirs(save_dir, exist_ok=True)  # Creates the folder if it doesn't exist

fingerprint_count = 1  # Keep track of stored fingerprints

print(f"Listening on {SERIAL_PORT}...")

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
        
        # Decode Base64 and save as a unique file
        fingerprint_bytes = base64.b64decode(data)
        
        file_path = os.path.join(save_dir, f"fingerprint_{fingerprint_count}.bin")
        
        with open(file_path, "wb") as f:
            f.write(fingerprint_bytes)

        print(f"✅ Fingerprint template saved to {file_path}")
        
        fingerprint_count += 1  # Increment for the next fingerprint
