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
import pickle as pkl

request_url = 'https://beta.api.deepfri.flatironinstitute.org/workspace/MCHQGK/predictions'


HEADERS = {
            'Host': 'beta.api.deepfri.flatironinstitute.org',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Origin': 'https://beta.deepfri.flatironinstitute.org',
            'Connection': 'keep-alive',
            'Referer': 'https://beta.deepfri.flatironinstitute.org/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'TE': 'trailers'}
            
pdb_to_ids = {}
            
def parese_data(input_path,input_file):
    print(input_path+input_file+" start!!!!")
    
    m = MultipartEncoder(fields={
            'inputType':'structureFile',
            'file':(input_file,open(input_path+input_file, 'rb'),'application/octet-stream'),
            'tags':None
    })
    requestTimes = 0
    file_name = os.path.split(input_file)[-1].split('.')[0]
    while requestTimes < 3:
        try:

            HEADERS['Content-Type'] = m.content_type
            response = requests.post(url=request_url,data=m,headers=HEADERS,timeout=100) 
            protein_text = response.text
            
            pdb_to_ids[file_name] = protein_text
            print('***' ,file_name, protein_text)
            break
            
        except:

            time.sleep(5)
            requestTimes += 1
            continue
    
    if requestTimes == 3:
        print('###' ,input_path+input_file+" error!!!!")

def main():

    input_path = './test_one_pdb_data/' #所有蛋白质PDB文件
    files = os.listdir(input_path)

    for input_file in files:
    
        file_name = os.path.split(input_file)[-1].split('.')[0]
        if os.path.exists(input_path[:-1]+"_result/"+file_name+'.pkl'):
            # print(file_name)
            continue
            
        parese_data(input_path,input_file)
        time.sleep(5)

    with open('test_one_pdb_data_ids.pkl', 'wb') as fw:
        pkl.dump(pdb_to_ids, fw)

if __name__ == '__main__':
    main()