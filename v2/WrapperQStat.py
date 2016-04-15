import os

multi_core_list=[]
f=os.popen('qstat multi_core_q')
count=0
#multi_core_list=[]
for f1 in f:
	if count>=2:
		s=f1.split()
		multi_core_list.append(s[0])
	count=count+1
#print multi_core_list

