# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function

class CacheDownException(Exception):
    def __init__(self, *args, **kwargs):
        super(Exception, self).__init__("CacheDown", *args, **kwargs)