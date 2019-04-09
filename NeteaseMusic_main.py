#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import NeteaseMusic_api

if __name__ == "__main__":
    spider = NeteaseMusicSpider()
    print('代理池ip数量：', spider.proxy_capacity())
    print(spider.get_proxy_ip())
    spider.get_comments('326719')