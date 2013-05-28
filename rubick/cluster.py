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
    def __init__(self, name_server, ports=range(0, 100)):
        self.name_server = name_server
        self.server = {}
        for port in ports:
            cache = CacheServer(port)
            self.server[port] = cache

    def select_port(self, key, *args, **kwargs):
        return self.name_server.get_port(self, key, *args, **kwargs)

    def get_cache(self, ports):
        caches = []
        for port in ports:
            if port in self.server:
                caches.append(self.server[port])
        return caches

    def get(self, key, *args, **kwargs):
        ports = self.select_port(key, *args, **kwargs)
        caches = self.get_cache(ports)
        value = None
        for cache in caches:
            value = cache.get(key, *args, **kwargs)
            if value:
                break
        return value

    def set(self, key, value, *args, **kwargs):
        ports = self.select_port(key, *args, **kwargs)
        caches = self.get_cache(ports)
        for cache in caches:
            cache.set(key, value, *args, **kwargs)

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
    def __init__(self, strategy="", redundancy=3):
        self.redundancy = redundancy
        self.hash_strategy = getattr(self, strategy, self.random_hash)

    def get_port(self, cluster, input, *args, **kwargs):
        return self.hash_strategy(cluster, input, *args, **kwargs)

    def random_hash(self, cluster, *args, **kwargs):
        cluster.check_caches()
        return random.choice(cluster.current_caches().keys())

    def consistent_hash(self, cluster, value, *args, **kwargs):
        cluster.check_caches()
        ports = cluster.current_caches().keys()
        values = map(lambda x: md5(str(x)), ports)
        port_values = zip(ports, values)
        sorted_port_values = sorted(port_values, key=lambda item: item[1])
        selected_ports, _ = zip(*sorted_port_values)
        if not selected_ports:
            raise Exception("No ports, Cluster Down")
        return selected_ports[:self.redundancy]
