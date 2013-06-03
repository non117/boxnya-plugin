# -*- coding: utf-8 -*-
import cPickle as pickle
import datetime
import time
import urllib, urllib2
import lxml.html

from collections import deque

from lib.core import Input

def serialize(filename, obj):
    with open(filename, "wb") as f:
        pickle.dump(obj, f)

def deserialize(filename):
    with open(filename, "rb") as f:
        return pickle.load(f)

class PxImage:
    def __init__(self, node):
        self.node = node
        self.image_url = node.xpath('div/a/img')[0].attrib["src"].replace("3.jpg", "4.jpg")
        self.id = int(self.image_url.split("/")[3])
        self.title = node.xpath('div/div/div/a')[1].text
        self.author = node.xpath('div/div/div/a')[0].text
        self.page_url = "http://500px.com/photo/%d" % self.id
    def to_tumblr_param(self):
        caption = '<a href=\"%s\">%s / %s</a>' % (self.image_url, self.title, self.author)
        params = {'type':'photo', 'link':self.page_url, 'caption':caption, 'source':self.image_url}
        return params

class PxCrawler(Input):
    def init(self):
        self.n = 1 # A number of page crawling.
        try:
            self.q = deserialize("500px.dump")
        except IOError:
            self.q = deque(maxlen=self.n*10*20)

    def fetch_pximages(self):
        baseurl = "http://500px.com/popular?page=%d"
        images = []
        for i in range(self.n):
            s = urllib.urlopen(baseurl % (i + 1)).read()
            image_node = lxml.html.fromstring(s).xpath('//div[contains(concat(" ",normalize-space(@class)," "), "photo_thumb")]')
            for node in image_node:
                images.append(PxImage(node))
        return images

    def check_dup(self, images):
        ids = map(lambda img:img.id, images)
        d = dict(zip(ids, images))
        old_ids = set(self.q)
        new_ids = list(set(ids) - old_ids)
        map(self.q.append, new_ids)
        serialize("500px.dump", self.q)
        return [d[id_] for id_ in new_ids]

    def fetch(self):
        images = self.check_dup(self.fetch_pximages())
        print len(images) #debug
        for image in images:
            self.send(image.to_tumblr_param())
        time.sleep(10800)

    def cleanup(self):
        serialize("500px.dump", self.q)