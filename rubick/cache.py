# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from util.exceptions import CacheDownException
import random
import time

failure_rate = 100 # 1/100
AVAILABLE_FIELD = "__AVAILABLE"
DELAY_AREA = (0, 100)

def delay_decorator(func):
    def wrapper(*args, **kwargs):
        delay = kwargs.pop("delay", 0) or random.randint(*DELAY_AREA)
        time.sleep(delay/1000)
        res = func(*args, **kwargs)
        return res
    return wrapper

def problem_decorator(func):
    def wrapper(*args, **kwargs):
        instance = args[0]
        if not getattr(instance, AVAILABLE_FIELD, True):
            raise CacheDownException()
        worked = random.randint(0, failure_rate)
        if not worked:
            setattr(instance, AVAILABLE_FIELD, False)
        else:
            return func(*args, **kwargs)
    return wrapper

class ActionMetaClass(type):
    DECORATORS = [delay_decorator, problem_decorator]
    def __new__(cls, class_name, bases, class_dict):
        for attr, item in class_dict.items():
            if callable(item):
                for decorator in cls.DECORATORS:
                    item = decorator(item)
                class_dict[attr] = item

        if not AVAILABLE_FIELD in class_dict:
            class_dict[AVAILABLE_FIELD] = True
        return type.__new__(cls, class_name, bases, class_dict)

class CacheServer(object):
    __metaclass__ = ActionMetaClass

    def __init__(self, port=8000):
        self.cache = {}
        self.port = port

    def set(self, name, value, *args, **kwargs):
        self.cache[name] = value

    def get(self, name, *args, **kwargs):
        return self.cache.get(name, "")

    def ping(self):
        return bool(getattr(self, AVAILABLE_FIELD, False))
