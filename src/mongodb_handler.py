import pymongo
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class MongoDBHandler:
    def __init__(self, database: str):
        """
        Initialize the MongoDB connection.
        :param uri: MongoDB connection URI.
        :param database: Database name.
        """
        uri = os.getenv("MONGODB_URI")
        if not uri:
            raise ValueError("Environment variable MONGODB_URI not set.")
        self.client = pymongo.MongoClient(uri)
        self.db = self.client[database]

    def insert_data(self, collection: str, data: dict):
        """
        Insert a document into a specific collection.
        :param collection: The name of the collection (sensor token).
        :param data: The document to insert.
        """
        # Add a timestamp to the data
        data['timestamp'] = datetime.utcnow()
        self.db[collection].insert_one(data)

    def close(self):
        """
        Close the MongoDB connection.
        """
        self.client.close()

