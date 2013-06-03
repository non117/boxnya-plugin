from lib.core import Input
import mechanize
import urllib
import json

class TumblrNotify(Input):
    def init(self):
        br = mechanize.Browser()
        br.set_handle_robots(False)
        
        self.cj = mechanize.LWPCookieJar()
        br.set_cookiejar(self.cj)
        
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(),
                              max_time=1)
        
        br.open("https://www.tumblr.com/login")
        br.select_form(nr=0)
        
        br['user[email]'] = ""
        br['user[password]'] = ""
        
        url, data, hdrs = br.form.click_request_data()
        br.open("https://www.tumblr.com/login", data)

        self.nf = 0

        opener = mechanize.build_opener(
            mechanize.HTTPCookieProcessor(self.cj))
        mechanize.install_opener(opener)
        self._fetch()

    def _fetch(self):
        req = {
            'notifications_next': 50000,
            'magick': self.nf,
            'notifications': 'true',
            'from': self.nf,
            }
        
        res = mechanize.urlopen("http://www.tumblr.com/svc/poll?%s" 
                                % urllib.urlencode(req))
        data = json.loads(res.read())
        self.nf = data['next_from']
        return data["notifications"]

    def fetch(self):
        for post in self._fetch():
            text = post["from_tumblelog_name"] + u" " + post["type"] +  u"ed " + post["summary"] + u"\n" + post["target_post_url"]
            self.send(text)
