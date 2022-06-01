from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

conn_str = "mongodb+srv://ASHOK:ASHOK@cluster0.lgtry.mongodb.net/?retryWrites=true&w=majority"
conn = MongoClient(conn_str, server_api=ServerApi('1'),serverSelectionTimeoutMS=5000)

database = conn.files_database
file_collection = database.get_collection("files")

try:
    print('database connected successfully')
except Exception:
    print("Unable to connect to the server.")
