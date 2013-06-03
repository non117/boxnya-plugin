# -*- coding: utf-8 -*-
import random
import urllib2

from lib.core import Output
from lib.tumblr.api import Api

class Tumblr2(Output):
    def init(self):
        api1 = Api(self.atoken, self.atokensecret, self.ckey, self.csecret, self.hostname)
        api2 = Api(self.atoken2, self.atokensecret2, self.ckey, self.csecret, self.hostname)
        self.apis = [api1, api2]
    
    def throw(self, packet):
        params = packet["data"]
        if params["type"] == "photo":
            source = params["source"]
            link = params.get("link")
            caption = params.get("caption")
            request = urllib2.Request(source)
            image_obj = urllib2.urlopen(request).read()
            n = random.randint(0,1)
            self.apis[n].post_photo("", caption, link, image_obj, source)
    