from pymongo import MongoClient
from pymongo.ssl_support import SSLContextOptions

import logging
logging.basicConfig(level=logging.DEBUG)

from pymongo import MongoClient

uri = "mongodb+srv://dharshan:whatsmyname@cluster0.hh0vx.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri)
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print("Error:", e)

