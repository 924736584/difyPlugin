import logging
from typing import Optional
from pymongo import MongoClient
from pymongo.collection import Collection
from bson import ObjectId
import datetime


class MongoDbUtil:

    def __init__(self, db_type: str,
                 username: str, password: str,
                 host: str, port: Optional[int] = None,
                 database: Optional[str] = None,
                 properties: Optional[str] = None) -> None:
        self.db_type = db_type
        self.username = username
        self.password = password
        self.host = host
        self.port = port if port else 27017  # Default MongoDB port is 27017
        self.database = database
        self.properties = properties
        self.client = self.connect_mongo()

    def connect_mongo(self):
        '''
        Create a connection to MongoDB.
        '''
        connection_str = f"mongodb://{self.username}:{self.password}@{self.host}:{self.port}/"
        logging.info(f"MongoDB connect str: {connection_str}")
        client = MongoClient(connection_str)
        return client

    def get_database(self) -> Optional['Database']:
        '''
        Get the MongoDB database instance.
        '''
        if self.database:
            return self.client[self.database]
        else:
            logging.error("No database name provided")
            return None

    def get_collection(self, collection_name: str) -> Collection:
        '''
        Get the MongoDB collection instance.
        '''
        db = self.get_database()
        if db is not None:
            return db[collection_name]
        else:
            raise ValueError("No valid database connection found")

    def run_query(self, collection_name: str, query: dict, projection: Optional[dict] = None) -> list[dict]:
        '''
        Run a MongoDB query and return results as a list of dictionaries.
        '''
        collection = self.get_collection(collection_name)
        if collection is not None:
            cursor = collection.find(query).limit(5)
            records = []
            for document in cursor:
                print(document)
                document = self.convert_bson_types(document)
                records.append(document)
            print(records)
            return records
        else:
            return []

    def convert_bson_types(self, document: dict) -> dict:
        '''
        Convert BSON types like ObjectId to string, datetime to formatted string etc.
        '''
        for key, value in document.items():
            if isinstance(value, ObjectId):
                document[key] = str(value)
            elif isinstance(value, datetime.datetime):
                document[key] = value.strftime('%Y-%m-%d %H:%M:%S')
        return document

    def test_connection(self) -> bool:
        '''
        Test MongoDB connection.
        '''
        try:
            db = self.get_database()
            if db:
                return True
        except Exception as e:
            logging.error(f"Error while connecting to MongoDB: {str(e)}")
        return False

    @staticmethod
    def is_not_empty(s: str) -> bool:
        '''
        Check if a string is not empty.
        '''
        return s is not None and s.strip() != ""
