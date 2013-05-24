# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from cache import CacheServer
from util.utils import md5
import random

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
            raise Exception("Port not in pools")
        return self.server[port]

    def get(self, port, key, *args, **kwargs):
        cache = self.get_cache(port)
        return cache.get(key, *args, **kwargs)

    def set(self, port, key, value, *args, **kwargs):
        cache = self.get_cache(port)
        return cache.set(key, value, *args, **kwargs)

    def check_caches(self):
        """
        每次check之后，可以保证当前状态下cache是能work的
        """
        delete_port = []
        for port in self.server:
            try:
                worked = self.server[port].ping()
            except:
                delete_port.append(port)
            else:
                if not worked:
                    delete_port.append(port)

        for port in delete_port:
            del self.server[port]

    def current_caches(self):
        return self.server

class NameServer(object):
    """
    NameServer负责维护数据冗余，以及如何去读取数据
    """
    def __init__(self, cluster, strategy="", redundancy=3):
        self.redundancy = redundancy
        self.cluster = cluster
        self.hash_strategy = getattr(self, strategy, self.random_hash)

    def get_port(self, input):
        return self.hash_strategy(input)


    def random_hash(self, *args, **kwargs):
        self.cluster.check_caches()
        return random.choice(self.cluster.current_caches().keys())

    def consistent_hash(self, value, *args, **kwargs):
        self.cluster.check_caches()
        ports = self.cluster.current_caches().keys()
        select_port = None
        current_value = ""
        for port in ports:
            md5_value = md5(str(port) + str(value))
            if md5_value > current_value:
                select_port = port
        if select_port is None:
            raise Exception("No ports, Cluster Down")
        return select_port

    def get(self, key):
        port = self.get_port(key)
        self.cluster.get(port, key)

    def set(self, key, value):
        port = self.get_port(key)
        self.cluster.set(port, key, value)

