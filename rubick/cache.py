# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
import random
failure_rate = 100 # 1/100
AVAILABLE_FIELD = "__AVAILABLE"

def problem_decorator(func):
    def wrapper(*args, **kwargs):
        instance = args[0]
        if not getattr(instance, AVAILABLE_FIELD, True):
            raise Exception()
        worked = random.randint(0, failure_rate)
        if not worked:
            setattr(instance, AVAILABLE_FIELD, False)
        else:
            return func(*args, **kwargs)
    return wrapper

class ProblemMetaClass(type):
    def __new__(cls, class_name, bases, class_dict):
        for attr, item in class_dict.items():
            if callable(item):
                class_dict[attr] = problem_decorator(item)
        if not AVAILABLE_FIELD in class_dict:
            class_dict[AVAILABLE_FIELD] = True
        return type.__new__(cls, class_name, bases, class_dict)

class BaseCache(object):
    __metaclass__ = ProblemMetaClass

    def __init__(self):
        self.cache = {}

    def set(self, name, value):
        self.cache[name] = value

    def get(self, name):
        return self.cache.get(name, "")

