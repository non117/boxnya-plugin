# -*- coding: utf-8 -*-
import urllib, urllib2

from lib.tumblr.oauth import OAuth

class Api():
    def __init__(self,  atoken="", atokensecret="", ckey="", csecret="", hostname=""):
        self.oauth = OAuth(ckey, csecret, atoken, atokensecret)
        self.site = "http://api.tumblr.com/v2/blog/%s/" % (hostname)
    
    def initializer(self):
        ''' アクセストークン, シークレットを作る '''
        request_url = "http://www.tumblr.com/oauth/request_token"
        auth_url = "http://www.tumblr.com/oauth/authorize"
        accesstoken_url = "http://www.tumblr.com/oauth/access_token"
        return self.oauth.oauth_initializer(request_url, auth_url, accesstoken_url)
    
    def execute(self, url, method, params={}, file_param=()):
        ''' リクエスト処理の実行 '''
        # パラメータを成形して辞書に
        for key, val in params.items():
            if isinstance(val, unicode): val = val.encode("utf-8")
            params[key] = urllib.quote(str(val), "")
        if file_param:
            request = self.oauth.make_request_raw(url, method, params, file_param)
        else:
            request = self.oauth.make_request(url, method, params)
        try:
            response = urllib2.urlopen(request)
            data = response.read()
            return data
        except urllib2.URLError, e:
            return e.read()

    def post_text(self, body, title=""):
        url = self.site + "post"
        return self.execute(url,"POST", {"type":"text",
                                         "title":title,
                                         "body":body})
    
    def post_photo(self, source="", caption="", link="", image_obj=None, file_name=""):
        url = self.site + "post"
        if image_obj:
            data = ("data", image_obj, file_name)
        else:
            data = ()
        return self.execute(url, "POST", {"type":"photo",
                                          "caption":caption,
                                          "link":link,
                                          "source":source,
                                          },
                            data
                            )
