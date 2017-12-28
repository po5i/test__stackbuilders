# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from crawler.models import Crawl, Entry

class CrawlerTestCase(TestCase):

    def test_01_first30(self):
        """
        Get the first 30 entries
        """
        crawl = Crawl.objects.create()
        output = crawl.perform_crawl(30)
        self.assertTrue(output)

    def test_02_filter5words_greater_order_by_comments(self):
        """
        Filter all previous entries with more than five words in the title ordered by amount of comments first.
        """
        crawl = Crawl.objects.create()
        crawl.perform_crawl(30)
        filtered = crawl.filter(words_greater=5, order='comments')
        comments = 0

        for f in filtered:
            self.assertTrue(len(f.title.split()) > 5)
            if comments != 0:
                self.assertTrue(f.comments <= comments)
            comments = f.comments

    def test_03_filter5words_less_order_by_points(self):
        """
        Filter all previous entries with less than or equal to five words in the title ordered by points.
        """
        crawl = Crawl.objects.create()
        crawl.perform_crawl(30)
        filtered = crawl.filter(words_less=5, order='points')
        points = 0

        for f in filtered:
            self.assertTrue(len(f.title.split()) <= 5)
            if points != 0:
                self.assertTrue(f.points <= points)
            points = f.points

