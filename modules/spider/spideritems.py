# -*- coding: utf-8 -*-
__author__ = 'ayonel'
import itertools
import json
import os
from scrapy import Item
from scrapy import Field
from scrapy.settings import Settings
from scrapy.crawler import Crawler

class SpiderItems(Item):
    domain = Field()
    title = Field()
    url = Field()
    tag = Field()