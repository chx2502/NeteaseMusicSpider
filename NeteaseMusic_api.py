#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 27 15:24:13 2018

@author: chengxin
"""

import requests
import json
from bs4 import BeautifulSoup
from http.cookiejar import LWPCookieJar
from http.cookiejar import Cookie
from NeteaseMusic_encrypt import encrypted_request
import random

BASE_URL = 'https://music.163.com'
COOKIE_PATH = '/Users/chengxin/workplace/GitHub/python3.6/NeteaseMusicSpider/cookies'
COOKIE_KEY = '__csrf'
PROXY_POOL_URL = 'http://127.0.0.1:5010/'

headers_list = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]

def proxy_capacity():
    url = PROXY_POOL_URL + 'get_status'
    msg = requests.request('get', url)
    data = msg.json()
    return int(data['useful_proxy'])

class NeteaseMusicSpider(object):
    def __init__(self):
        self.proxies = dict()
        # self.cookie_path = COOKIE_PATH
        # cookie_jar = LWPCookieJar('cookies')
        # cookie_jar.load()
        self.session = requests.Session()
        # self.session.cookies = cookie_jar

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
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'  # NOQA
                    }

    def add_proxy(self):
        url = PROXY_POOL_URL + 'get'
        req = requests.request('get', url)
        ip = req.text
        if proxy_capacity() != 0:
            self.proxies['http'] = 'http://' + ip
            self.proxies['https'] = 'https://' + ip

    def delete_proxy(self):
        string = self.proxies['http']
        ip = (string.split('//'))[1]
        url = PROXY_POOL_URL + 'delete?proxy=' + ip
        req = requests.request('get', url)
        self.proxies.clear()
        if req.text == 'success':
            return True
        else:
            print(req.text)
            return False

    def get_proxy(self):
        if len(self.proxies) == 0:
            self.add_proxy()
        return self.proxies

    def repalce_proxy(self):
        self.delete_proxy()
        self.add_proxy()

    def request(self, method, action, params):
        i = random.randrange(0, 18)
        self.header['User-Agent'] = headers_list[i]
        path = BASE_URL + action
        proxy = self.get_proxy()
        if method == 'POST':
            req = self.session.post(headers=self.header,
                                    url=path,
                                    proxies=proxy,
                                    params=params)
        elif method == 'GET':
            req = self.session.get(headers=self.header,
                                   url=path,
                                   proxies=proxy,
                                   params=params)
        # self.session.cookies.save()
        return req

    def login(self, username, password):
        action = '/weapi/login/cellphone'
        text = dict(phone=username, password=password, rememberLogin="true")
        params = encrypted_request(text)
        data = self.request('POST', action, params)
        return data
    
    def get_parmas(self, page, music_id):
        text = {}
        if page == 1:
            text = {
                    'rid': music_id,
                    'offset': '0',
                    'total': 'true',
                    'limit': '20',
                    'csrf_token': ''
                    }
        else:
            offset = str((page - 1)*20)
            text = {
                    'rid': music_id,
                    'offset': offset,
                    'total': 'false',
                    'limit': '100',
                    'csrf_token': ''
                    }
        return text

    def get_comments(self, music_id):
        '''
        request 返回为 json 数据，热门评论在 'hotComments' 字段
        hotComments 为 list，包含的元素 comment 为 dict ，
        comment 中，评论内容字段为 'content', 用户信息为 'user'，
        用户 id 为 user['userId'], 昵称为 user['nickname']
        '''
        action = '/weapi/v1/resource/hotcomments/R_SO_4_{}?csrf_token='.format(music_id) 
        for i in range(1, 16):
            text = self.get_parmas(i, music_id)
            params = encrypted_request(text)
            try:
                content = self.request('POST', action, params)
            except requests.exceptions.RequestException as e:
                print(e)
                self.repalce_proxy()
                continue
            soup = BeautifulSoup(content.text, 'lxml')
            jsonObj = json.loads(soup.find('p').string)
            print('第{:d}页'.format(i))
            comment_list = jsonObj['hotComments']
            with open('指定评论.txt', 'a+') as f:
                for comment in comment_list:
                    f.write(comment['content']+'\n')
            f.close()

    def test_req(self, music_id):
        action = '/weapi/v1/resource/hotcomments/R_SO_4_{}?csrf_token='.format(music_id)
        ret = list()
        with open('指定某人的评论.txt', 'a+') as f: 
            for i in range(0, 11):
                text = self.get_parmas(i, music_id)
                params = encrypted_request(text)
                try:
                    json_data = self.request('POST', action, params)
                except requests.exceptions.RequestException as e:
                    print(e)
                    i = i-1
                    self.proxies.clear()
                    self.add_proxy()
                    continue
                print('第{:d}页'.format(i))
                ret.append(json_data)
        f.close()
        return ret

if __name__ == "__main__":
    spider = NeteaseMusicSpider()
    print('代理池ip数量：', proxy_capacity())
    print(spider.get_proxy())   
    spider.get_comments('476181079')
    # data = spider.test_req('326719')
    # print('hC类型：', type(hotComments))
    # for comment in hotComments:
    #     user = comment['user']
    #     print('user类型：', type(user))
    #     userId = user['userId']
    #     print('userId类型：', type(userId))
