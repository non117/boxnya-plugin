# -*- coding: utf-8 -*-
import json
import urllib, urllib2
import time
from datetime import datetime

from lib.core import Input

class Teiden(Input):
    def get_info(self):
        source = {1:u"月間予定",2:u"翌日予定",3:u"当日予定"}
        params = {
                "data":datetime.today().strftime("%Y%m%d"),
                "group":""
                }
        url = "http://kteiden.chibiegg.net/api/kteiden.json"
        req = urllib2.Request(url+"?"+urllib.urlencode(params))
        res = urllib2.urlopen(req).read()
        if res == '[]': return None
        data = json.loads(res)[0]
        if data["is_implemented"] is True:
            return u"%s %s-%sに停電予定. 順番 : %d, 情報源 : %s, 電気予報 : %d%%" % (
                                                                     data["date"] ,
                                                                     data["start"],
                                                                     data["end"],
                                                                     data["order"],
                                                                     source[data["source"]],
                                                                     data["forecast"]["rate"],
                                                                     )

    def fetch(self):
        today = datetime.today()
        if today.hour in (0,8,10,12,14,16,18):
            text = self.get_info()
            if text:
                self.send(text)
        time.sleep(1800)