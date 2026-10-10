import os
from urllib.parse import quote_plus
from pymongo import MongoClient

username = quote_plus(os.environ["MONGO_USERNAME"])
password = quote_plus(os.environ["MONGO_PASSWORD"])

uri = (
    f"mongodb+srv://{username}:{password}"
    "@cluster0.lyjxwkq.mongodb.net/"
    "?retryWrites=true&w=majority&appName=Cluster0"
)

client = MongoClient(uri, serverSelectionTimeoutMS=15000)

try:
    client.admin.command("ping")
    print("MongoDB connected successfully!")

except Exception as e:
    print("MongoDB connection failed:", e)

finally:
    client.close()
