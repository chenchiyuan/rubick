# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function

from rubick.cluster import Cluster, NameServer
key = "test"
value = ""

def test():
    cluster = Cluster()
    global value
    server = NameServer(cluster, "consistent_hash")
    for i in range(1000):
        value = i
        server.set(key, value)
        cache_value = server.get(key)
        if not cache_value:
            print("Cache Value Miss")
            exit()
        if not value == cache_value:
            print("Cache Value wrong")
            exit()
    print("Success!")

if __name__ == "__main__":
    test()