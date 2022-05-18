import pickle as pkl
import sys
import os
import pandas as pd
import requests
import time
import sys
import threading



# 在UniProt中获取每个蛋白质的序列信息
error_proteins = []
url = 'https://rest.uniprot.org/beta/uniprotkb/{0}.fasta'

def request_uniprot(protein_accessions, output_file):
    print(output_file)
    
    success_proteins = {}
    if os.path.exists(output_file):
        with open(output_file, 'r') as fr:
            for line in fr:
                if line.startswith('>'):
                    entry = line.split('|')[1]
                    success_proteins[entry] = 0
    
    
    with open(output_file,'a') as fw:
        for p in protein_accessions:
            if p in success_proteins:
                continue
                
            p_url = url.format(p)
            try:
                down_res = requests.get(url=p_url)
                down_res = str(down_res.content, encoding="utf-8")

                fw.write(down_res)
                # with open(output_path+p+'.fasta',"w") as code:
                    # code.write(down_res)
                time.sleep(0.5)
                
            except:
                error_proteins.append(p)
                print('error', p)
                time.sleep(0.5)
                
threads=[]
counts = 50

protein_accessions_file = './PPI_protein_accessions_4.csv'
output_path = './fasta_results/'
if not os.path.exists(output_path):
    os.mkdir(output_path)


protein_accessions = list(pd.read_csv(protein_accessions_file)['proteins'])
group_num = len(protein_accessions)//counts+1

for i in range(40, 50):
    output_file = output_path+'all_PPI_protein_sequences_{0}_4.fasta'.format(i)
    t = threading.Thread(target=request_uniprot,args=(protein_accessions[i*group_num:(i+1)*group_num],output_file,))
    threads.append(t)
    t.start()
    print(i*group_num, (i+1)*group_num)
    
    
for t in threads:
    t.join()   
       
print('this is in parent')       

df = pd.DataFrame({'proteins':error_proteins})
ouput_file =  './not_find_in_uniprot_PPI_protein_accessions4.csv'
df.to_csv(ouput_file)
