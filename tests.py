# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function

from rubick.cluster import Cluster, NameServer
from rubick.client import Client
key = "test"
value = ""

def test():
    client = Client()
    name_server = NameServer(strategy="consistent_hash")
    cluster = Cluster(name_server)
    items = range(1, 100)
    for i in items:
        client.set(cluster, key, value=i)
        value = i
        check_value = client.get(cluster, key)
        if check_value == value:
            pass
        else:
            print("Not Match")
            print("Value Is %s, but in cache is %s" %(value, check_value))

if __name__ == "__main__":
    test()