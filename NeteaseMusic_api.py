#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 27 15:24:13 2018

@author: chengxin
"""

import requests
from http.cookiejar import LWPCookieJar
from http.cookiejar import Cookie
from NeteaseMusic_encrypt import encrypted_request

BASE_URL = 'https://music.163.com'
COOKIE_PATH = '/Users/chengxin/workplace/GitHub/python3.6/NeteaseMusicSpider/cookies'
COOKIE_KEY = '__csrf'


class NeteaseMusicSpider(object):
    def __init__(self):
        self.cookie_path = COOKIE_PATH
        self.proxy_pool = []
        cookie_jar = LWPCookieJar('cookies')
        # cookie_jar.load()
        self.session = requests.Session()
        self.session.cookies = cookie_jar

        self.header = {
                    'Accept': '*/*',
                    'Accept-Encoding': 'gzip,deflate,sdch',
                    'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
                    'Connection': 'keep-alive',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Cookie': 'appver=2.7.1',
                    'Host': 'music.163.com',
                    'Referer': 'http://music.163.com',
                    'User-Agent':
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'  # NOQA
                    }

    def request(self, method, action, params):
        path = BASE_URL + action
        if method == 'POST':
            req = self.session.post(headers=self.header,
                                    url=path,
                                    params=params)
        elif method == 'GET':
            req = self.session.get(headers=self.header,
                                   url=path,
                                   params=params)
        self.session.cookies.save()
        return req
        # json_data = req.json()
        # return json_data

    def login(self, username, password):
        action = '/weapi/login/cellphone'
        text = dict(phone=username, password=password, rememberLogin="true")
        params = encrypted_request(text)
        data = self.request('POST', action, params)
        return data
