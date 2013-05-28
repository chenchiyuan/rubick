# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from rubick.metas import ProblemMetaClass, AVAILABLE_FIELD

class CacheServer(object):
    """
    cache server内部执行忽略延迟，认为延迟产生于客户端+网络（时间丢给客户端）
    """
    __metaclass__ = ProblemMetaClass

    def __init__(self, port=8000):
        self.cache = {}
        self.port = port

    def set(self, name, value, *args, **kwargs):
        self.cache[name] = value

    def get(self, name, *args, **kwargs):
        return self.cache.get(name, "")

    def ping(self):
        return bool(getattr(self, AVAILABLE_FIELD, False))