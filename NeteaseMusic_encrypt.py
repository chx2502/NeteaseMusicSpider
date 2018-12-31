#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 27 14:50:42 2018

@author: chengxin
"""

import json
import os
import base64
import binascii
from Crypto.Cipher import AES

from builtins import chr
from builtins import int
from builtins import pow

NONCE = b'0CoJUm6Qyw8W8jud'
PUBKEY = '010001'
MODULUS = ('00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7'
           'b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280'
           '104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932'
           '575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b'
           '3ece0462db0a22b8e7')
default_timeout = 10


#def createSecretKey(size):
#    return binascii.hexlify(os.urandom(size))[:16]
#
#
#def aesEncrypt(text, secKey):
#    pad = 16 - len(text) % 16
#    text = text + chr(pad) * pad
#    encryptor = AES.new(secKey, 2, '0102030405060708')
#    ciphertext = encryptor.encrypt(text)
#    ciphertext = base64.b64encode(ciphertext).decode('utf-8')
#    return ciphertext
#
#
#def rsaEncrypt(text, pubKey, modulus):
#    text = text[::-1]
#    rs = pow(int(binascii.hexlify(text), 16),
#             int(pubKey, 16),
#             int(modulus, 16))
#    return format(rs, 'x').zfill(256)
#
#
#def encrypted_request(text):
#    text = json.dumps(text).encode('utf-8')
#    secKey = createSecretKey(16)
#    encText = aesEncrypt(aesEncrypt(text, NONCE), secKey)
#    encSecKey = rsaEncrypt(secKey, pubKey, modulus)
#    data = dict(encSecKey=encSecKey, params=encText)
#    return data

# 登录加密算法, 基于https://github.com/stkevintan/nw_musicbox

def aes(text, key):
    pad = 16 - len(text) % 16
    text = text + bytearray([pad] * pad)
    encryptor = AES.new(key, 2, b"0102030405060708")
    ciphertext = encryptor.encrypt(text)
    return base64.b64encode(ciphertext)


def rsa(text, pubkey, modulus):
    text = text[::-1]
    rs = pow(int(binascii.hexlify(text), 16), int(pubkey, 16), int(modulus, 16))
    return format(rs, "x").zfill(256)


def create_key(size):
    return binascii.hexlify(os.urandom(size))[:16]


def encrypted_request(text):
    # type: (str) -> dict
    data = json.dumps(text).encode("utf-8")
    secret = create_key(16)
    params = aes(aes(data, NONCE), secret)
    encseckey = rsa(secret, PUBKEY, MODULUS)
    return {"params": params, "encSecKey": encseckey}
