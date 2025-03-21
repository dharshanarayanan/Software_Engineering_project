import pymongo
from pymongo import MongoClient

uri = "mongodb+srv://dharshan:saymyname@cluster0.hh0vx.mongodb.net/voting_system?retryWrites=true&w=majority&authSource=admin&tls=true"

client = MongoClient(uri)
client.admin.command('ping')
print("✅ Connected!")
