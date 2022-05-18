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


all_result = {}
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
    global all_result
    print(entry+" start!!!!")
    get_data = {
    "query":entry,
    "sort":"score"
    }
    requestTimes = 0
    while requestTimes < 3:
        try:
            request_url = urls.format(entry)#
            # print(request_url)
            # print(get_data)data=get_data,headers=HEADERS,
            s = requests.session()
            response = s.get(url=request_url,data=get_data,headers=HEADERS,timeout=100) 
            
            print(entry,response.status_code)
            with open('./error_protein_result/{0}.txt'.format(entry),'wb') as fw:
                fw.write(response.content)
                
            tree = etree.HTML(response.text)
            temp_con = tree.xpath('//*[@id="page-header"]/h2/text()')[0]
            print(temp_con)
            temp_con = temp_con.strip().split()[-1]
            print(temp_con)
            print('*'*100)
            all_result[entry] = temp_con
            
            
            break
        except:
            time.sleep(2)
            requestTimes += 1
            continue
    
    if requestTimes == 3:
        with open('./error_protein/'+entry,'w') as fw:
            fw.write('error'+'\n')


def main():
    global all_result
    # not_find_test.pkl
    entrys = []
    with open('error_protein.txt','r') as fr:
        for line in fr:
            entrys.append(line.strip())
    for entry in entrys:
        parese_data(entry)
        time.sleep(4)


if __name__ == '__main__':

    main()
    with open('mapping_result_error_protein.pkl','wb') as fw:
        pkl.dump(all_result,fw)
