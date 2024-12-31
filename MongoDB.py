from pymongo import MongoClient

# Replace <username>, <password>, and <cluster> with your details
client = MongoClient("mongodb+srv://NirmalVignesh:Nirmal@cluster0.o1af3.mongodb.net/")
db = client["myDatabase"]  # Replace with your database name
collection = db["myCollection"]  # Replace with your collection name

# Insert a document to create the database
collection.insert_one({"key": "value"})
print("Database and collection created!")
