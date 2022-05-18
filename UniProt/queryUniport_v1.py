# coding=utf-8


import requests
import os
from lxml import etree
import json
import time
import random
import string
import urllib.parse
import base64
from collections import OrderedDict
import pandas as pd
import math
import pickle as pkl
from requests_toolbelt import MultipartEncoder
import sys

# urls = "https://www.uniprot.org/uniprot/?query={0}&sort=score"
urls = 'https://www.uniprot.org/uniprot/{0}'
# 'Content-Type': 'multipart/form-data; boundary=---------------------------322470008841756697352887733435',
HEADERS = {'Host': 'www.uniprot.org',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://www.uniprot.org/',
            'Cookie': 'allSelected4=false; _ga=GA1.2.19763555.1589526543; _gid=GA1.2.181935432.1589526543; _gat=1',
            'Upgrade-Insecure-Requests': '1'}



def parese_data(entry):
    print(entry+" start!!!!")
    get_data = {
    "query":entry,
    "sort":"score"
    }
    # requestTimes = 0
    # while requestTimes < 3:
        # try:
    request_url = urls.format(entry)#
    print(request_url)
    # print(get_data)data=get_data,headers=HEADERS,
    s = requests.session()
    response = s.get(url=request_url,data=get_data,headers=HEADERS,timeout=30) 
    print(entry,response.status_code,response.headers)
    print(response.content)
            # break
        # except:
            # time.sleep(2)
            # requestTimes += 1
            # continue
    
    # if requestTimes == 3:
        # print(entry,'error')
        # with open('./errors/'+input_file,'w') as fw:
            # fw.write('error'+'\n')


def main():
    entrys = ['P30486']
    for entry in entrys:

        parese_data(entry)
        time.sleep(2)


if __name__ == '__main__':

    main()
