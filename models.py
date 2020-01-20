from pymongo import MongoClient
from decouple import config


class Message:

    def __init__(self, db_url, port):
        self.db_url = db_url
        self.port = port

    def client(self):
        client = MongoClient(self.db_url, self.port)
        return client

    def save_message(self, msg):
        db = self.client.message
        db.insert_one(msg)











