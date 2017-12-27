# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import requests
from bs4 import BeautifulSoup

class Entry(models.Model):
    crawl = models.ForeignKey('Crawl', related_name='entries')
    title = models.CharField(max_length=256)
    order = models.IntegerField()
    comments = models.IntegerField()
    points = models.IntegerField()

class Crawl(models.Model):
    date = models.DateTimeField(auto_now_add=True)

    def perform_crawl(self, max_items):
        url = 'https://news.ycombinator.com/'
        source = requests.get(url)
        text = source.text
        soup = BeautifulSoup(text, 'html.parser')
        count = 0

        # for element in soup.findAll('a', {'class': 'storylink'}):
        for element in soup.findAll('tr', {'class': 'athing'}):
            order = element.find('span', {'class': 'rank'}).string.replace('.', '')
            id = element.get('id')
            title = element.find('a', {'class': 'storylink'}).string
            points = element.next_sibling.find('span', {'class': 'score'}).string.replace(' points', '')
            comments = element.next_sibling.find_all('a', {'href': 'item?id='+id})[1].string.replace(' comments', '').replace(' comment', '')
            try:
                comments = int(comments)
            except:
                comments = 0
            
            entry = Entry.objects.create(crawl=self, title=title, order=order, comments=comments, points=points)
            
            count += 1
            if count > max_items:
                break


