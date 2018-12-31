#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 27 22:43:52 2018

@author: chengxin
"""

from hashlib import md5
import NeteaseMusic_api as api


class NeteaseMusicUser(object):
    def __init__(self, username='', password=''):
        self.username = username
        self.password = md5(password.encode(encoding='utf-8')).hexdigest()

    def login(self):
        return api.login(self.username, self.password)
