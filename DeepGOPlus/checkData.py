import os

all_proteins_file = os.listdir('./split_test_data_v2')
all_protein = []
for protein in all_proteins_file:
	protein = protein.split('.')[0]
	all_protein.append(protein)

success_protein_file = os.listdir('./success')
success_protein = []
for protein in success_protein_file:
	protein = protein.split('.')[0]
	success_protein.append(protein)

for protein in all_protein:
	if protein not in success_protein:
		commend_line = 'cp ./split_test_data_v2/'+protein+'.fasta ./split_test_data/'+protein+'.fasta'
		os.system(commend_line)


