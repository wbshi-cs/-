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

# request_url = 'https://beta.deepfri.flatironinstitute.org/workspace/MCHQGK/predictions/'
request_url = 'https://beta.api.deepfri.flatironinstitute.org/workspace/MCHQGK/predictions/'


# HEADERS = {
            # 'Host': 'beta.deepfri.flatironinstitute.org',
            # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0',
            # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            # 'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            # 'Accept-Encoding': 'gzip, deflate, br',
            # 'Connection': 'keep-alive',
            # 'Upgrade-Insecure-Requests': '1',
            # 'Sec-Fetch-Dest': 'document',
            # 'Sec-Fetch-Mode': 'navigate',
            # 'Sec-Fetch-Site': 'none',
            # 'Sec-Fetch-User': '?1'
            # }
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
            'Sec-Fetch-Site': 'same-site',}
                        

def download_files(input_file, output_path):
    with open(input_file, 'r') as fr:
        for line in fr:
            if line.startswith("***"):
                line = line.strip().split()
                # print(line)
                protein_name = line[1]
                if os.path.exists(output_path+protein_name+'.pkl'):
                    continue
                
                # try:
                tags = False
                for i in line:
                    if tags:
                        DeepFRI_id = i.split('\"')[1]
                        break
                    # print(i)
                    if i == '\"name\":':
                        # print(i)
                        tags = True
                # print(DeepFRI_id)
                # sys.exit(0)
                # print(protein_name, DeepFRI_id, line[-1])
                # print(request_url+DeepFRI_id)
                try:
                
                    response = requests.get(url=request_url+DeepFRI_id,headers=HEADERS,timeout=100)
                    # response = response.content.decode("utf-8")
                    # print( protein_name, DeepFRI_id, request_url+DeepFRI_id)
                    response = response.json()
                    # print(type(response), response.keys(), response['prediction'].keys())  # ['prediction', 'total']
                    # print('***', protein_name, DeepFRI_id, request_url+DeepFRI_id)
                    
                    save_dicts = response['prediction']['data']
                    with open(output_path+protein_name+'.pkl', 'wb') as fw:
                        pkl.dump(save_dicts, fw)
                    

                    print('***', protein_name, DeepFRI_id, request_url+DeepFRI_id)
                except:
                    print('###', protein_name, DeepFRI_id, request_url+DeepFRI_id)
                    continue
                
                # sys.exit(0)

            
def analysis_data(input_path,input_file):
    
    with open(input_path+input_file, 'rb') as fr:
        pro_data = pkl.load(fr)
        
    print(pro_data.keys())
    print(type(pro_data['data']), pro_data['data'].keys())
    print("pro_data['data']['A']",type(pro_data['data']['A']), pro_data['data']['A'].keys())
    print("pro_data['data']['A']['gcn_cc']",type(pro_data['data']['A']['gcn_cc']), pro_data['data']['A']['gcn_cc'].keys())
    print("pro_data['data']['A']['gcn_cc']['predictions']",type(pro_data['data']['A']['gcn_cc']['predictions']), pro_data['data']['A']['gcn_cc']['predictions'])
    print("pro_data['data']['A']['gcn_mf']['predictions']",type(pro_data['data']['A']['gcn_mf']['predictions']), pro_data['data']['A']['gcn_mf']['predictions'])
    print("pro_data['data']['B']",type(pro_data['data']['B']), pro_data['data']['B'].keys())
    print("pro_data['data']['B']['gcn_cc']['predictions']",type(pro_data['data']['B']['gcn_cc']['predictions']), pro_data['data']['B']['gcn_cc']['predictions'])
    print("pro_data['data']['B']['gcn_mf']['predictions']",type(pro_data['data']['B']['gcn_mf']['predictions']), pro_data['data']['B']['gcn_mf']['predictions'])
            
def main():
    
    # file_name = "test_two_pdb_data"
    file_name = "test_one_pdb_data"
    
    input_path = './{0}_result/'.format(file_name) #所有蛋白质PDB文件
    if not os.path.exists(input_path):
        os.makedirs(input_path)
    
    
    # 下载相关数据集
    down_file = file_name + "_out.txt"
    download_files(down_file, input_path)
    
    # files = os.listdir(input_path)

    # for input_file in files:
        # analysis_data(input_path,input_file)
        


if __name__ == '__main__':
    main()