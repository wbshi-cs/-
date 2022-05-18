
max_length = 900
with open('TestDataset.fasta','r') as fr:
    for line in fr:
        line = line.strip()
        sequence = fr.readline().strip()
        if len(sequence) > max_length:
            print(line, len(sequence))
        
        
        
        