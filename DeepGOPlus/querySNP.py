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

request_url = 'http://deepgoplus.bio2vec.net/deepgo/'

HEADERS = {'Host': 'deepgoplus.bio2vec.net',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': '1200',
            'Origin': 'http://deepgoplus.bio2vec.net',
            'Connection': 'keep-alive',
            'Referer': 'http://deepgoplus.bio2vec.net/deepgo/',
            'Upgrade-Insecure-Requests': '1'}



def parese_data(input_data,file,count):
    # print('*'*100)
    print(file+" start!!!!")
    post_data = {
        'csrfmiddlewaretoken':'RLUlVZ5DWToE286dET7wRAhK3QE3wGkoXFVOZI8v87qfN8yvGQ5AEHGyb5ZFgM4Y',
        'data_format':'fasta',
        'threshold':'0.0'
    }
    post_data['data'] = input_data
    ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 16))
    HEADERS['Cookie'] = 'csrftoken=RLUlVZ5DWToE286dET7wRAhK3QE3wGkoXFVOZI8v87qfN8yvGQ5AEHGyb5ZFgM4Y'
    # isError = True
    requestTimes = 0
    while requestTimes < 3:
        try:
            print("*"*50,requestTimes,"*"*50)
            response = requests.post(url=request_url, data=post_data, headers=HEADERS, timeout=90) 
            #print(response.text)
            print(response.status_code)
            #sys.exit(0)
            tree = etree.HTML(response.text)
            # 此处div[51]要修改
            title = tree.xpath('/html/body/div/div/div[{0}]/a[1]/@href'.format(count+1))[0]
            print(title)
            get_url = request_url+title[8:]
            print(file,get_url,requestTimes)
            #time.sleep(0.5)
            response = requests.get(get_url)
            result = json.loads(response.text)
            temp_file = file.split('.')[0] + '.pkl'
            with open('./all_2016_uniport_sport_test_50_result/'+temp_file,'wb') as fw:
                pkl.dump(result,fw)
            break
        except:
            time.sleep(5)
            requestTimes += 1
            continue
    
    if requestTimes == 3:
        with open('./all_2016_uniport_sport_test_50_error/'+file,'w') as fw:
            fw.write('error'+'\n')
            
    print(file+" has done!!!!!")
        


def getTags(input_path):
    input_data = ''
    count = 0
    with open(input_path, 'r') as fr:
        for line in fr:
            line = line.strip()
            if line:
                input_data += line+'\r\n'
                count += 1

    return input_data,count//2


def main():
    num = 1
    files = os.listdir('./all_2016_uniport_sport_test_50/')
    # print(files)
    # sys.exit(0)
    for file in files:
        input_data,count = getTags('./all_2016_uniport_sport_test_50/'+file)
        parese_data(input_data,file,count)
        time.sleep(10)


if __name__ == '__main__':
    # input_path = './cluster_test_protein_sequence_501_550.fasta'  # 你输入的txt文件文件
    # main(input_path)
    main()
