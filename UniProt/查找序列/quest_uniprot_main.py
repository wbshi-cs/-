import os
import time
import subprocess

commond_line = "nohup python -u quest_uniprot_{0}.py >>quest_uniprot_{0}_out4.txt 2>&1 &"
number_line = "ps aux|grep quest_uniprot_{0}.py|grep -cv grep"

while True:
    for i in range(1,2):
        cmd = (subprocess.run(number_line.format(i),shell=True,stdout=subprocess.PIPE))
        num = int(cmd.stdout.strip())
        
        if num < 1:
            time.sleep(3)
            print(commond_line.format(i), 'error')
            os.system(commond_line.format(i))
        else:
            time.sleep(3)
