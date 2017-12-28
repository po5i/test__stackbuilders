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

    def as_dict(self):
        return {
            "title": self.title,
            "order": self.order,
            "comments": self.comments,
            "points": self.points,
        }

class Crawl(models.Model):
    date = models.DateTimeField(auto_now_add=True)

    def perform_crawl(self, max_items):
        url = 'https://news.ycombinator.com/'
        source = requests.get(url)
        text = source.text
        soup = BeautifulSoup(text, 'html.parser')
        error = False

        def elementAnalysis(element):
            order = element.find('span', {'class': 'rank'}).string.replace('.', '')
            id = element.get('id')
            title = element.find('a', {'class': 'storylink'}).string
            try:
                points = element.next_sibling.find('span', {'class': 'score'}).string.replace(' points', '')
            except:
                return False
            try:
                comments = element.next_sibling.find_all('a', {'href': 'item?id='+id})[1].string.replace(' comments', '').replace(' comment', '')
                comments = int(comments)
            except:
                return False
            
            return {
                "title": title, 
                "order": order, 
                "comments": comments, 
                "points": points
            }
            
        # parsedList = []
        # for element in soup.findAll('tr', {'class': 'athing'}):
        #     parsed = elementAnalysis(element)
        #     if not parsed:
        #         continue
        #     parsedList.append(parsed)

        parsedList = list(map(elementAnalysis, soup.findAll('tr', {'class': 'athing'})))

        # filter Falses:
        parsedListFiltered = list(filter(lambda x: x != False, parsedList))

        for p in parsedListFiltered:
            Entry.objects.create(crawl=self, title=p["title"], order=p["order"], comments=p["comments"], points=p["points"])


            # order = element.find('span', {'class': 'rank'}).string.replace('.', '')
            # id = element.get('id')
            # title = element.find('a', {'class': 'storylink'}).string
            # try:
            #     points = element.next_sibling.find('span', {'class': 'score'}).string.replace(' points', '')
            # except:
            #     # points = 0
            #     continue
            # try:
            #     comments = element.next_sibling.find_all('a', {'href': 'item?id='+id})[1].string.replace(' comments', '').replace(' comment', '')
            #     comments = int(comments)
            # except:
            #     # comments = 0
            #     continue
            
            # entry = Entry.objects.create(crawl=self, title=title, order=order, comments=comments, points=points)
            
            # count += 1
            # if count > max_items:
            #     break

        return True

    def filter(self, **kwargs):
        num_words_greater = kwargs.get('words_greater')
        num_words_less = kwargs.get('words_less')
        arg_order = kwargs.get('order')
        
        objects = Entry.objects.filter(crawl=self)
        output = []
        
        if arg_order:
            objects = objects.order_by('-' + arg_order)

        def criteria_greater(obj):
            return len(obj.title.split()) > num_words_greater

        def criteria_less(obj):
            return len(obj.title.split()) <= num_words_less

        if num_words_greater:
            output = list(filter(criteria_greater, objects))
        elif num_words_less:
            output = list(filter(criteria_less, objects))

        # for obj in objects:
        #     words = len(obj.title.split())
        #     if num_words_greater:
        #         if words > num_words_greater:
        #             output.append(obj)
        #     elif num_words_less:
        #         if words <= num_words_less:
        #             output.append(obj)

        return output
