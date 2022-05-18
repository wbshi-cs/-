import requests
import sys


with open('./netgo_test_split_data_v1_out.txt','r') as fr:
	t = fr.readline()
	for line in fr:
		line = line.strip()
		if line:
			mess = line.split(' ')
			if mess[1].endswith('txt'):
				download_response = requests.get(url=mess[1])
				result = download_response.content.decode()
				file_name = mess[0].split('.')[0]+'.result'
				with open('./netgo_test_split_data_result_v1/'+file_name,'w') as fw:
					fw.write(result)
##				sys.exit(0)	

