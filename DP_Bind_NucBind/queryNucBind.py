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

request_url = 'https://yanglab.nankai.edu.cn/cgi-bin/NucBind.cgi'
HEADERS = {
            'Host': 'yanglab.nankai.edu.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Origin': 'https://yanglab.nankai.edu.cn',
            'Connection': 'keep-alive',
            'Referer': 'https://yanglab.nankai.edu.cn/NucBind/',
            'Upgrade-Insecure-Requests': '1'}

def parese_data(input_path,input_file):
    print(input_path+input_file+" start!!!!")
    all_length = 0
    with open(input_path+input_file,'r') as fr:
        for line in fr:
            
            all_length += len(line.strip())
    
    m = MultipartEncoder(fields={
            'PDB':None,
            'str_file':(input_file,open(input_path+input_file, 'rb'),'application/octet-stream'),
            #'REPLY-E-MAIL':'648810502@qq.com',
            'TARGET-NAME':input_file.split('.')[0],
            'submit':'submit',
            
    })
    requestTimes = 0
    tags = False
    temp_url = ''
    while requestTimes < 3:
        try:
            HEADERS['Content-Type'] = m.content_type
            HEADERS['Content-Length'] = str(all_length)
           
            response = requests.post(url=request_url,data=m,headers=HEADERS,timeout=300) 
            # text = ''
            # with open('a.html','r') as fr:
                # for line in fr:
                    # text += line
            tree = etree.HTML(response.text)
            temp_url = tree.xpath('//meta/@content')[0].split('=')[1]
            print(input_file,'post data',response.status_code,requestTimes)
            print('+'*20)
            print(input_file,response.text)
            print('#'*20)
            print(input_file,temp_url)
            print('*'*20)
            tags = True

            break
        except:
            time.sleep(30)
            requestTimes += 1
            
    
    if not tags:
    
        print(input_path+input_file+" error!!!!")
        return 'error'
        
    return temp_url


def isFinish(result_url):
    response = requests.get(url=result_url,timeout=300) 
    # print(response.status_code,response.text)
    tree = etree.HTML(response.text)
    content = tree.xpath('/html/body/font/text()')
    content = ''.join(content)
    if content.endswith("You can bookmark this page to check the results later."):
        return False
    else:
        return True


def main():
    num = 4
    all_list = []
    
    input_path = './fasta/'
    files = os.listdir(input_path)
    
    for input_file in files:
    
        if len(all_list) < num:
            urls = parese_data(input_path,input_file)
            all_result_url[input_file] = urls
            if urls == 'error':
                time.sleep(30)
                continue
            else:
                all_list.append(urls)
                time.sleep(3)

        list_length = len(all_list)
        
        while list_length == num:
            all_pop = []
            for i in range(list_length):
                finish_tag = isFinish(all_list[i])
                
                if finish_tag:
                    all_pop.append(all_list[i])
                time.sleep(30)
                
            for i in all_pop:
                all_list.remove(i)
                
            list_length = len(all_list)
            
    with open('NucBind_query_result.txt','w') as fw:
        for k,v in all_result_url.items():
            fw.write(k,' ', v)
        
if __name__ == '__main__':
    main()
