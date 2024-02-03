from pymongo import MongoClient

uri = "mongodb+srv://mongo1:g6BHrVNzjVRQznr@linkshortener.88yutcr.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri)

db = client.linkshortener_db

collection = db.collection


# from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi
# uri = "mongodb+srv://mongo1:<password>@linkshortener.88yutcr.mongodb.net/?retryWrites=true&w=majority"
# # Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'))
# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)