# -*- coding: utf-8 -*-
import re
import time
import urllib, urllib2
import urlparse

import lxml.html

from lib.core import Input

class Thumbnail:
    """pixiv thumbnails and some information"""
    
    def __init__(self, id_, title_, author_, pageURL_, imgURL_):
        self.id      = id_
        self.title   = title_
        self.author  = author_
        self.imgURL  = imgURL_
        self.pageURL = pageURL_

def getPage(url):
    req = urllib2.Request(url)
    req.add_header('Referer', 'http://www.pixiv.net')
    req.add_header('Accept-Language', 'ja')
    return unicode(urllib2.urlopen(req).read(), "utf-8")

def getLargeImage(id_):
    url = "http://www.pixiv.net/member_illust.php?mode=medium&illust_id="+str(id_)
    root = lxml.html.fromstring(getPage(url)).xpath('//img[@border="0"]')[0]
    return [root.attrib['src']]

def searchTag(word, full=True):    
    def makeImageData(tags):
        a   = tags.xpath(".//a")
        h2  = tags.xpath(".//h1")[0].text
        img = tags.xpath(".//img[1]/@src")[0]
        p   = re.compile('.*/member_illust\.php\?mode=medium&illust_id=(\d+)')

        pageURL= urlparse.urljoin("http://www.pixiv.net/", a[0].attrib['href'])
        id_ = int(p.match(pageURL).group(1))
        title = h2
        author = a[1].text
        imgURL = img
        
        return Thumbnail(id_, title, author, pageURL, imgURL)
    
    #部分一致
    qword = urllib.quote_plus(word.encode('utf-8'))
    if full:
        url = "http://www.pixiv.net/search.php?s_mode=s_tag_full&word="+qword
    else:
        url = "http://www.pixiv.net/search.php?s_mode=s_tag&word="+qword
    dom = lxml.html.fromstring(getPage(url))
    return map(makeImageData, dom.xpath('//li[@class="image-item"]'))

class PixivCrawler(Input):
    def init(self):
        self.latest_id_file = open("pixivcrawler.txt", "r+")
        self.latest_id_dict = eval(self.latest_id_file.read() or "{}") # dict
    
    def get_latest_id(self, key):
        return self.latest_id_dict.get(key, 0)
    
    def set_latest_id(self, key, id_):
        self.latest_id_dict[key] = id_
        self.latest_id_file.seek(0)
        self.latest_id_file.write(str(self.latest_id_dict))
    
    def fetch(self):
        for key in self.search_tags:
            latest_id = self.get_latest_id(key)
            image_list = searchTag(key.decode("utf-8"))
            image_list = filter(lambda a:a.id > latest_id, sorted(image_list, lambda a, b:a.id > b.id))
            if image_list == []:
                continue
            self.set_latest_id(key, image_list[0].id)
            for image in image_list:
                page_url = image.pageURL
                image_url = getLargeImage(image.id)[0]
                caption =  '<a href=\"%s\">%s / %s</a>' % (image_url, image.title, image.author)
                params = {'type':'photo', 'link':page_url, 'caption':caption, 'source':image_url}
                self.send(params)
        time.sleep(3600)
    
    def cleanup(self):
        self.latest_id_file.close()