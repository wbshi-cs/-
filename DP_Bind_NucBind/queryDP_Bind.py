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
import json

request_url = 'http://lcg.rit.albany.edu/dp-bind/cgi-bin/parseform.cgi'
HEADERS = {
        'Host': 'lcg.rit.albany.edu',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        # 'Content-Type': 'multipart/form-data; boundary=---------------------------7921120811457743223170692629
        # 'Content-Length': '948
        'Origin': 'http://lcg.rit.albany.edu',
        'Connection': 'keep-alive',
        'Referer': 'http://lcg.rit.albany.edu/dp-bind/',
        # 'Cookie': 'sc_is_visitor_unique=rx4573300.1617847087.24BF06988D524F16B2F898006ACDEE4A.4.3.2.2.2.2.2.2.2',
        'Upgrade-Insecure-Requests': '1'}

def parese_data(input_path,input_file):
    print(input_path+input_file+" start!!!!")
    all_length = 0
    with open(input_path+input_file,'r') as fr:
        for line in fr:
            
            all_length += len(line.strip())
    
    m = MultipartEncoder(fields={
            'seq_input_method':'upload',
            'file_uploaded':(input_file,open(input_path+input_file, 'rb'),'application/octet-stream'),
            'encoding':'pssm',
            'delivery':'link_to_file',
    })
    requestTimes = 0
    tags = False
    temp_url = ''
    while requestTimes < 3:
        try:
            HEADERS['Content-Type'] = m.content_type
            HEADERS['Content-Length'] = str(all_length)
            response = requests.post(url=request_url,data=m,headers=HEADERS,timeout=300)
            tree = etree.HTML(response.text)
            temp_url = tree.xpath('//a/text()')[0]
            print('*'*5, input_file, temp_url)
            tags = True
            break
        except:
            time.sleep(5)
            requestTimes += 1

    if not tags:
        print('#'*5,input_path+input_file+" error!!!!")
        return 'error'
        
    return temp_url


def isFinish(result_url):
    response = requests.get(url=result_url,timeout=300) 
    # print(response.status_code,response.text)
    # tree = etree.HTML(response.text)
    # content = tree.xpath('//body/text()')
    # print(content)
    # content = ''.join(content)
    content = str(response.text)
    if content.startswith("Process is still running."):
        return False
    else:
        time.sleep(3)
        tree = etree.HTML(response.text)
        result = tree.xpath('//tt/text()')
        # print(result)
        # for ii,c in enumerate(result):
            # print(ii,c)
        with open('./dp_bind_result/'+result[12][1:].strip()+'_dp_bind.result','w') as fw:
            for i in result:
                fw.write(i)
            
        
        return True


def main():
    num = 30
    all_list = []
    
    input_path = './fasta/'
    files = os.listdir(input_path)
    
    for input_file in files:
    
        if len(all_list) < num:
            urls = parese_data(input_path,input_file)
            if urls == 'error':
                time.sleep(3)
                continue
            else:
                all_list.append(urls)
                time.sleep(3)
        
        list_length = len(all_list)
        
        while list_length == num:
            all_pop = []
            for i in range(list_length):
                finish_tag = isFinish(all_list[i])
                
                if not finish_tag:
                    all_pop.append(all_list[i])
                time.sleep(2)
                
            
            all_list = all_pop    
            list_length = len(all_list)
    #sys.exit(0)
    while list_length != 0:
        all_pop = []
        for i in range(list_length):
            finish_tag = isFinish(all_list[i])
            
            if not finish_tag:
                all_pop.append(all_list[i])
            time.sleep(2)
            
        all_list = all_pop    
        list_length = len(all_list)
        
if __name__ == '__main__':
    main()
