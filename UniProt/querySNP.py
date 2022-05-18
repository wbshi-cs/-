# coding=utf-8


import requests
from lxml import etree
import json
import time
import random
import string
import urllib.parse
import json
import base64
from collections import OrderedDict
import pandas as pd
import math

request_url = 'http://snpcurator.science.uu.nl/home'
result_url = 'http://snpcurator.science.uu.nl/results'

HEADERS = {'Host': 'snpcurator.science.uu.nl',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
           'Accept-Encoding': 'gzip, deflate',
           'Content-Type': 'application/x-www-form-urlencoded',
           'Content-Length': '50',
           'Origin': 'http://snpcurator.science.uu.nl',
           'Connection': 'keep-alive',
           'Referer': 'http://snpcurator.science.uu.nl/',
           'Upgrade-Insecure-Requests': '1'}

GET_HEADERS = {'Host': 'snpcurator.science.uu.nl',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
           'Accept-Encoding': 'gzip, deflate',
           'Content-Type': 'application/x-www-form-urlencoded',
           'Content-Length': '50',
           'Origin': 'http://snpcurator.science.uu.nl',
           'Connection': 'keep-alive',
           'Referer': 'http://snpcurator.science.uu.nl/',
           'Upgrade-Insecure-Requests': '1'}

def parese_data(tag, error_tags):
    post_data = {
        "nm": tag,
        "year1": 2000,
        "year2": 2018,
        "NumOfPub": 3000
    }
    ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 16))
    HEADERS['Cookie'] = 'session=.eJyrVvIrzfVPCyhNUrJSMjYwMFDSUcpLzE0F8grycyqTK4tLMpMV8ssSiyoViivzUorygXI6SpWpiUWGQDVGEB0grhGYa2ihVAsAaX4ZfA.EPcOZw.ohVO8l5qZkZ' + ran_str
    isError = True
    requestTimes = 0
    while requestTimes < 3:
        try:
            response = requests.post(url=request_url, data=post_data, headers=HEADERS, timeout=90)
            break
        except:
            time.sleep(3)
            requestTimes += 1
            continue

    if requestTimes == 3:
        error_tags.append(tag.replace('+', ' '))
    else:
        tree = etree.HTML(response.text)

        # print(tree.xpath('//*[@id="myTable"]/thead/tr/th[1]/text()'))
        csv_title = tree.xpath('//*[@id="myTable"]/thead/tr//text()')
        # print(len(csv_title))
        result = OrderedDict()
        title_list = []
        for ii, con in enumerate(csv_title):
            if ii % 2 != 0:
                result[con] = []
                title_list.append(con)

        csv_con = tree.xpath('//*[@id="myTable"]/tbody/tr')
        for ii, trs in enumerate(csv_con):
            if ii % 2 == 0:
                all_tds = trs.xpath('./td')
                for jj, td in enumerate(all_tds):

                    if jj < 10:
                        if jj != 1:
                            con = td.xpath('./text()')
                            if len(con) > 0:
                                result[title_list[jj]].append(con[0])
                            else:
                                result[title_list[jj]].append(math.nan)

                        else:
                            PMID = td.xpath('./a/text()')
                            if len(PMID) > 0:
                                result[title_list[jj]].append(PMID[0])
                            else:
                                result[title_list[jj]].append(math.nan)

                    else:
                        TextTd = csv_con[ii + 1]
                        TextCon = TextTd.xpath('./td/text()')
                        if len(TextCon) > 0:
                            result[title_list[jj]].append(TextCon[0])
                        else:
                            result[title_list[jj]].append(math.nan)

        if 'SNP' not in result.keys() or len(result['SNP']) == 0:
            error_tags.append(tag.replace('+', ' '))
            print("search the {} is error".format(tag.replace('+', ' ')))
        else:
            print("search the {} is right".format(tag.replace('+', ' ')))
            save_path = './section1/' + tag.replace('+', ' ') + '.csv'
            df = pd.DataFrame(result)
            df.to_csv(save_path)
    return error_tags


def getTags(input_path):
    tages = []
    with open(input_path, 'r') as fr:
        for line in fr:
            line = line.strip()
            if line:
                line = line.replace(' ', '+')
                tages.append(line)

    return tages


def main(input_path):

    num = 1
    error_tags = []
    tages = getTags(input_path)
    for tag in tages:
        print(num, )
        error_tags = parese_data(tag, error_tags)
        time.sleep(5)
        num += 1

    errorFiles = './disease/error_2101-2800.txt'
    with open(errorFiles, 'w') as fw:
        for line in error_tags:
            fw.write(line + '\n')


if __name__ == '__main__':
    input_path = './disease/2101-2800_disease_name.txt'  # 你输入的txt文件文件
    main(input_path)
