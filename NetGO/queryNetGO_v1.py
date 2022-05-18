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

request_url = 'http://issubmission.sjtu.edu.cn/netgo/submit/'
# 'Content-Type': 'multipart/form-data; boundary=---------------------------322470008841756697352887733435',
HEADERS = {'Host': 'issubmission.sjtu.edu.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Length': '23103',
            'Origin': 'http://issubmission.sjtu.edu.cn',
            'Connection': 'keep-alive',
            'Referer': 'http://issubmission.sjtu.edu.cn/netgo/',
            'Upgrade-Insecure-Requests': '1'}

# -----------------------------38855140308536049692995224775
# Content-Disposition: form-data; name="fasta"
# -----------------------------38855140308536049692995224775
# Content-Disposition: form-data; name="file"; filename="atest.fasta"
# Content-Type: application/octet-stream
# >P08246
# MTLGRRLACLFLACVLPALLLGGTALASEIVGGRRARPHAWPFMVSLQLRGGHFCGATLIAPNFVMSAAHCVANVNVRAVRVVLGAHNLSRREPTRQVFAVQRIFENGYDPVNLLNDIVILQLNGSATINANVQVAQLPAQGRRLGNGVQCLAMGWGLLGRNRGIASVLQELNVTVVTSLCRRSNVCTLVRGRQAGVCFGDSGSPLVCNGLIHGIASFVRGGCASGLYPDAFAPVAQFVNWIDSIIQRSEDNPCPHPRDPDPASRTH
# >Q9M2T9
# MAARINTSLHNALSFLKPFNTPLNTKPFSFRRNSFRFSKKLPYYSQFSSGKRALYCTSSSQESTVDEGETFVLTTPLYYVNAPPHMGSAYTTIAADSIARFQRLLGKKVIFITGTDEHGEKIATSAAANGRNPPEHCDLISQSYRTLWKDLDIAYDKFIRTTDPKHEAIVKEFYARVFANGDIYRADYEGLYCVNCEEYKDEKELLENNCCPVHQMPCVARKEDNYFFALSKYQKPLEDILAQNPRFVQPSYRLNEVQSWIKSGLRDFSISRALVDWGIPVPDDDKQTIYVWFDALLGYISALTEDNKQQNLETAVSFGWPASLHLIGKDILRFHAVYWPAMLMSAGLELPKMVFGHGFLTKDGMKMGKSLGNTLEPFELVQKFGPDAVRYFFLREVEFGNDGDYSEDRFIKIVNAHLANTIGNLLNRTLGLLKKNCESTLVVDSTVAAEGVPLKDTVEKLVEKARTNYENLSLSSACEAVLEIGNAGNTYMDQRAPWFLFKQGGVSAEEAAKDLVIILEVMRVIAVALSPVAPCLSLRIYSQLGYTEDQFNSITWSDTKWGGLKGGQVMEQASPVFARIELNPEKEEDEKKPKVGKKTGKAKVKVVEQTPTVAEA
# >Q9EQR5
# MRPPVPSAPLALWVLGCFSLLLWLWALCTACHRKRAQRQQTGLQDSLVPVEMPLLRQTHLCSLSKSDTRLHELHRGPRSSIAPRPASMDLLHPRWLEMSRGSTRSQVPNSAFPPRQLPRAPPAAPATAPSTSSEATYSNVGLAAIPRASLAASPVVWAGTQLTISCARLGPGAEYACIQKHKGTEQGCQELQQKAKVIPATQMDVLYSRVCKPKRRDPRPVTDQLNLQDGRTSLPLGSDVEYEAINLRGQDMKQGPLENVYESIKEMGL
# >Q00888
# MGPLSAPPCTQRITWKGVLLTASLLNFWNPPTTAQVTIEAQPPKVSEGKDVLLLVHNLPQNLAGYIWYKGQMTYLYHYITSYVVDGQRIIYGPAYSGRERVYSNASLLIQNVTQEDAGSYTLHIIKRRDGTGGVTGHFTFTLHLETPKPSISSSNLNPREAMEAVILTCDPATPAASYQWWMNGQSLPMTHRLQLSKTNRTLFIFGVTKYIAGPYECEIRNPVSASRSDPVTLNLLPKLSKPYITINNLNPRENKDVLTFTCEPKSKNYTYIWWLNGQSLPVSPRVKRPIENRILILPNVTRNETGPYQCEIRDRYGGIRSDPVTLNVLYGPDLPSIYPSFTYYRSGENLYLSCFAESNPRAQYSWTINGKFQLSGQKLSIPQITTKHSGLYACSVRNSATGKESSKSITVKVSDWILP
# -----------------------------38855140308536049692995224775
# Content-Disposition: form-data; name="email"
# -----------------------------38855140308536049692995224775--


# -----------------------------3830169424175207560750492704
# Content-Disposition: form-data; name="fasta"


# -----------------------------3830169424175207560750492704
# Content-Disposition: form-data; name="file"; filename="atest.fasta"
# Content-Type: application/octet-stream

# >P08246
# MTLGRRLACLFLACVLPALLLGGTALASEIVGGRRARPHAWPFMVSLQLRGGHFCGATLIAPNFVMSAAHCVANVNVRAVRVVLGAHNLSRREPTRQVFAVQRIFENGYDPVNLLNDIVILQLNGSATINANVQVAQLPAQGRRLGNGVQCLAMGWGLLGRNRGIASVLQELNVTVVTSLCRRSNVCTLVRGRQAGVCFGDSGSPLVCNGLIHGIASFVRGGCASGLYPDAFAPVAQFVNWIDSIIQRSEDNPCPHPRDPDPASRTH
# >Q9M2T9
# MAARINTSLHNALSFLKPFNTPLNTKPFSFRRNSFRFSKKLPYYSQFSSGKRALYCTSSSQESTVDEGETFVLTTPLYYVNAPPHMGSAYTTIAADSIARFQRLLGKKVIFITGTDEHGEKIATSAAANGRNPPEHCDLISQSYRTLWKDLDIAYDKFIRTTDPKHEAIVKEFYARVFANGDIYRADYEGLYCVNCEEYKDEKELLENNCCPVHQMPCVARKEDNYFFALSKYQKPLEDILAQNPRFVQPSYRLNEVQSWIKSGLRDFSISRALVDWGIPVPDDDKQTIYVWFDALLGYISALTEDNKQQNLETAVSFGWPASLHLIGKDILRFHAVYWPAMLMSAGLELPKMVFGHGFLTKDGMKMGKSLGNTLEPFELVQKFGPDAVRYFFLREVEFGNDGDYSEDRFIKIVNAHLANTIGNLLNRTLGLLKKNCESTLVVDSTVAAEGVPLKDTVEKLVEKARTNYENLSLSSACEAVLEIGNAGNTYMDQRAPWFLFKQGGVSAEEAAKDLVIILEVMRVIAVALSPVAPCLSLRIYSQLGYTEDQFNSITWSDTKWGGLKGGQVMEQASPVFARIELNPEKEEDEKKPKVGKKTGKAKVKVVEQTPTVAEA
# >Q9EQR5
# MRPPVPSAPLALWVLGCFSLLLWLWALCTACHRKRAQRQQTGLQDSLVPVEMPLLRQTHLCSLSKSDTRLHELHRGPRSSIAPRPASMDLLHPRWLEMSRGSTRSQVPNSAFPPRQLPRAPPAAPATAPSTSSEATYSNVGLAAIPRASLAASPVVWAGTQLTISCARLGPGAEYACIQKHKGTEQGCQELQQKAKVIPATQMDVLYSRVCKPKRRDPRPVTDQLNLQDGRTSLPLGSDVEYEAINLRGQDMKQGPLENVYESIKEMGL
# >Q00888
# MGPLSAPPCTQRITWKGVLLTASLLNFWNPPTTAQVTIEAQPPKVSEGKDVLLLVHNLPQNLAGYIWYKGQMTYLYHYITSYVVDGQRIIYGPAYSGRERVYSNASLLIQNVTQEDAGSYTLHIIKRRDGTGGVTGHFTFTLHLETPKPSISSSNLNPREAMEAVILTCDPATPAASYQWWMNGQSLPMTHRLQLSKTNRTLFIFGVTKYIAGPYECEIRNPVSASRSDPVTLNLLPKLSKPYITINNLNPRENKDVLTFTCEPKSKNYTYIWWLNGQSLPVSPRVKRPIENRILILPNVTRNETGPYQCEIRDRYGGIRSDPVTLNVLYGPDLPSIYPSFTYYRSGENLYLSCFAESNPRAQYSWTINGKFQLSGQKLSIPQITTKHSGLYACSVRNSATGKESSKSITVKVSDWILP

# -----------------------------3830169424175207560750492704
# Content-Disposition: form-data; name="email"

# 1281867218@qq.com
# -----------------------------3830169424175207560750492704--


def parese_data(input_path,input_file):
    print(input_path+input_file+" start!!!!")
    m = MultipartEncoder(fields={
            'fasta':None,
            'file':(input_file,open(input_path+input_file, 'rb'),'application/octet-stream'),
            'email':None
    })
    requestTimes = 0
    # while requestTimes < 3:
        # try:
    HEADERS['Content-Type'] = m.content_type
    response = requests.post(url=request_url,data=m,headers=HEADERS,timeout=30000) 
    print(input_file,'post data',response.status_code,requestTimes)
    tree = etree.HTML(response.text)
    temp_url = tree.xpath('//*[@id="content"]/a/@href')[0]
    print(input_file,temp_url,requestTimes)
    temp_response = requests.get(url=temp_url)
    tree = etree.HTML(temp_response.text)
    temp_con = tree.xpath('//*[@id="content"]/h3/text()')[0]
    # print(temp_con)
    while temp_con.startswith('Sorry, the data is still'):
        time.sleep(3)
        temp_response = requests.get(url=temp_url)
        tree = etree.HTML(temp_response.text)
        temp_con = tree.xpath('//*[@id="content"]/h3/text()')[0]
        
    down_load_url = tree.xpath('//*[@id="content"]/h3/a[1]/@href')[0]
# down_load_url = 'http://issubmission.sjtu.edu.cn/netgo/1585296470/result.txt'
    print(input_file,down_load_url,requestTimes)
    download_response = requests.get(url=down_load_url)
    time.sleep(2)
    # all_contents = str(download_response.content).split('\n')
    all_contents = download_response.content.decode()
    file_name = input_file.split('.')[0]
    with open('./all_CAFA_test_50_result/'+file_name+'.result','w') as fw:
        #for line in all_contents:
        fw.write(all_contents)
    print(input_path+input_file+" success!!!!")
        # break
        # except:
            # time.sleep(5)
            # requestTimes += 1
            # continue
    sys.exit(0)
    # if requestTimes == 3:
        # print(input_path+input_file+" error!!!!")
        # with open('./all_CAFA_test_50_error/'+input_file,'w') as fw:
            # fw.write('error'+'\n')


def main():
    num = 1
    input_path = './all_CAFA_test_49/'
    files = os.listdir(input_path)
    # for file in files:
    for input_file in files:
        # input_file = 'cluster_test_protein_sequence_1_50.fasta'
        parese_data(input_path,input_file)
        time.sleep(10)
        #print(input_file)
        #sys.exit(0)


if __name__ == '__main__':
    # input_path = './cluster_test_protein_sequence_501_550.fasta'  # 你输入的txt文件文件
    # main(input_path)
    main()
