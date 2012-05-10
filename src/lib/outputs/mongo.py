# -*- coding: utf-8 -*-

from pymongo import Connection
from lib.core import Output

class Mongo(Output):
    def init(self):
        addr = "localhost"
        port = 27017
        db_name = "twitter"
        self.connection = Connection(addr, port)
        self.db = self.connection[db_name]
        
    def throw(self, packet):
        data = packet["data"]
        if data.get("event") is None:
            self.db.tweet.insert(data)
        elif "favorite" in data["event"]:
            self.db.favorite.insert(data)
        elif "list" in data["event"]:
            self.db.list.insert(data)
        elif "retweet" == data["event"]:
            self.db.retweet.insert(data)
        elif "follow" == data["event"]:
            self.db.follow.insert(data)
        elif "dm" == data["event"]:
            self.db.dm.insert(data)
        elif "delete" == data["event"]:
            self.db.delete.insert(data)
        
    def cleanup(self):
        self.connection.close()