# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from rubick.metas import DelayMetaClass

class Client(object):
    __metaclass__ = DelayMetaClass

    def get(self, cluster, key, *args, **kwargs):
        return cluster.get(key, *args, **kwargs)

    def set(self, cluster, key, value, *args, **kwargs):
        return cluster.set(key, value, *args, **kwargs)