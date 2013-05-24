# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from cache import CacheServer

class Cluster(object):
    """
    认为集群是不会挂的。
    """
    def __init__(self, ports=range(0, 100)):
        self.server = {}
        for port in ports:
            cache = CacheServer(port)
            self.server[port] = cache

    def get_cache(self, port):
        if not port in self.server:
            raise Exception()
        return self.server[port]


    def get(self, port, key, *args, **kwargs):
        cache = self.get_cache(port)
        return cache.get(key, *args, **kwargs)

    def set(self, port, key, value, *args, **kwargs):
        cache = self.get_cache(port)
        return cache.set(key, value, *args, **kwargs)