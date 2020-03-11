from pymongo import MongoClient


class Message:

    def __init__(self, db_url, port, message):
        self.db_url = db_url
        self.port = port
        self.message = message

    def client(self):
        client = MongoClient(self.db_url, self.port)
        return client

    def save_message(self):
        client = self.client()
        db = client.dbbot
        db.message.insert_one(self.message)


class Chat:

    def __init__(self, db_url, port, chat):
        self.db_url = db_url
        self.port = port
        self.chat = chat

    def client(self):
        client = MongoClient(self.db_url, self.port)
        return client

    def update_chat(self):
        _client = self.client()
        db = _client.dbbot
        db.chat.update(self.chat, upset=True)
