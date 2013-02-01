# -*- coding: utf-8 -*-
import re
import time
import urllib, urllib2

from BeautifulSoup import BeautifulSoup

from lib.core import Input

class PixivImage(object):
    """pixiv image and medium sized images"""
    def __init__(self, tag):
        a   = tag.findAll("a")
        h1  = tag.findAll("h1")[0].string
        img = tag.findAll("img")[0]['src']
        p   = re.compile('/member_illust\.php\?mode=medium&illust_id=(\d+)')
        
        self.id = int(p.match(a[0]['href']).group(1))
        self.title = u"「%s」 / %s" % (h1.string, a[1].string)
        self.url = img[0:-5]+"m."+img[-3:]

def search_pixiv(word):
    def get_page(url):
        return urllib2.urlopen(url).read()
    
    def make_image_data(tags):
        return PixivImage(tags)
    
    dom = BeautifulSoup(get_page("http://www.pixiv.net/search.php?s_mode=s_tag_full&word="+ urllib.quote_plus(word)))
    try:
#        lis = dom.findAll(attrs={'class' : "column-search-result"})[0].findAll(attrs = {'class' : "image-item"})
        lis = dom.findAll(attrs = {'class' : "image-item"})
    except IndexError:
        lis = []
    return map(make_image_data, lis)

class PixivCrawler(Input):
    def init(self):
        self.latest_id_file = open("pixivcrawler.txt", "r+")
        self.latest_id_dict = eval(self.latest_id_file.read() or "{}") # dict
    
    def get_latest_id(self, key):
        return self.latest_id_dict.get(key, 0)
    
    def set_latest_id(self, key, id):
        self.latest_id_dict[key] = id
        self.latest_id_file.seek(0)
        self.latest_id_file.write(str(self.latest_id_dict))
    
    def fetch(self):
        for key in self.search_tags:
            latest_id = self.get_latest_id(key)
            image_list = search_pixiv(key)
            image_list = filter(lambda a:a.id > latest_id, sorted(image_list, lambda a, b:a.id > b.id))
            if image_list == []:
                continue
            self.set_latest_id(key, image_list[0].id)
            for image in image_list:
                page_url = "http://www.pixiv.net/member_illust.php?mode=medium&illust_id=%d" % image.id
                caption =  '<a href=\"%s\">%s</a>' % (image.url, image.title)
                params = {'type':'photo', 'link':page_url, 'caption':caption, 'source':image.url}
                self.send(params)
        time.sleep(3600)
    
    def cleanup(self):
        self.latest_id_file.close()