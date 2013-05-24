# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
import hashlib

def md5(value):
    md5_ = hashlib.md5()
    md5_.update(value)
    return md5_.hexdigest()