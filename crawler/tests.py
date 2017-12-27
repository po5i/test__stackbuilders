# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from crawler.models import Crawl, Entry

class CrawlerTestCase(TestCase):

    # def setUp(self):
    #     """ 
    #     Setup the initial data
    #     """
    #     crawl = Crawl.objects.create()
    #     self.__class__.crawl = crawl

    def test_01_first30(self):
        """
        Get the first 30 entries
        """
        crawl = Crawl.objects.create()
        crawl.perform_crawl(30)
        self.assertEqual(crawl.entries.all().count(),30)


    # Filter all previous entries with more than five words in the title ordered by amount of comments first.
    # Filter all previous entries with less than or equal to five words in the title ordered by points.
    
