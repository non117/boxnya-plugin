# -*- coding: utf-8 -*-
from pymongo import Connection

from lib.core import Filter

class Deleted(Filter):
    def init(self):
        self.watch = [] # 監視対象のスクリーンネームを入れる. 空なら全部通知
        self.exclude = []

        addr = "localhost"
        port = 27017
        db_name = "twitter"
        self.connection = Connection(addr, port)
        self.col = self.connection[db_name].tweet
    
    def filter(self, packet):
        data = packet["data"]
        if not isinstance(data, dict):
            return None
        if data.get("event") == "delete":
            try:
                tweet = self.col.find({u"id":data["id"]})[0]
            except IndexError:
                return None
            detail = {"user":tweet[u"user"][u"screen_name"],
                      "post":tweet[u"text"]}
            if str(detail["user"]) in self.exclude or (self.watch != [] and str(detail["user"]) not in self.watch):
                return None
            self.send(u"%(user)s deleted: %(post)s" % detail, exclude = ["favbot"])

    def cleanup(self):
        self.connection.close()