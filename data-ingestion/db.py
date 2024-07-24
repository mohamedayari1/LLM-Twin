from pymongo import MongoClient
from pymongo import ConnectionFailure

from config import settings

class MongoDatabaseConnector:
    "Singleton class to connect to MongoDB database."
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            try:
                cls._instance = MongoClient(settings.MONGO_DATABASE_HOST)
            except ConnectionFailure as e:
                print(f"Couldn't connect to the database:   {str(e)}")
                raise 
        print(f"Connection to database with uri:  {settings.MONGO_DATABASE_HOST}")
        return cls._instance    
    
    def get_database(self):
        return self._instance[settings.MONGO_DATABASE_NAME]
    
    def close(self):
        if self._instance:
            self._instance.close()
            print("Connection to database has been closed")
            
connection = MongoDatabaseConnector()