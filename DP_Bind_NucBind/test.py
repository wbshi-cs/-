
def save_file(count,all_len):

    with open('./DPBind/'+str(count)+'_'+str(count+len(all_len)-1)+'.fasta','w') as fw:
        for line, sequence in all_len:
            fw.write(line+'\n')
            fw.write(sequence)


all_len = []
count = 1
with open('TestDataset.fasta','r') as fr:
    for line in fr:
        line = line.strip()
        sequence = fr.readline()
        all_len.append((line,sequence))
        
        if len(all_len) == 45:
            save_file(count,all_len)
            count += len(all_len)
            all_len = []
            
save_file(count,all_len)
        