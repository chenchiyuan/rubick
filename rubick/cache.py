# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
import random
failure_rate = 100 # 1/100

def problem_decorator(func):
    def wrapper(*args, **kwargs):
        worked = random.randint(0, failure_rate)
        if not worked:
            raise Exception()
        else:
            return func(*args, **kwargs)
    return wrapper

class ProblemMetaClass(type):
    def __new__(cls, class_name, bases, class_dict):
        for attr, item in class_dict.items():
            if callable(item):
                class_dict[attr] = problem_decorator(item)

        return type.__new__(cls, class_name, bases, class_dict)

class BaseCache(object):
    __metaclass__ = ProblemMetaClass

    def __init__(self):
        self.cache = {}

    def set(self, name, value):
        self.cache[name] = value

    def get(self, name):
        return self.cache.get(name, "")

