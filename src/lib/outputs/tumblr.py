# -*- coding: utf-8 -*-
import urllib2

from lib.core import Output
from lib.tumblr.api import Api

class Tumblr(Output):
    def init(self):
        self.api = Api(self.atoken, self.atokensecret, self.ckey, self.csecret, self.hostname)
    
    def throw(self, packet):
        params = packet["data"]
        if params["type"] == "photo":
            source = params["source"]
            link = params.get("link")
            caption = params.get("caption")
            if "pixiv" in source:
                request = urllib2.Request(source)
                request.add_header('Referer', 'http://www.pixiv.net')
                image_obj = urllib2.urlopen(request).read()
                self.api.post_photo("", caption, link, image_obj, source)
            else:
                self.api.post_photo(source, caption, link)