import requests
import time
import datetime
from pymongo import MongoClient

client = MongoClient()
db = client['data_monitor']

ganglia_req = requests.get('http://129.107.255.31:8080/atlas/ganglia')
torque_req = requests.get('http://129.107.255.31:8080/atlas/torque')

nagios_req = requests.get('http://129.107.255.31:8080/atlas/nagios/compute_nodes')

#r.json()
#for k,v in r.json:
#	print k

ganglia_data = ganglia_req.json()

torque_data = torque_req.json()

nagios_data = nagios_req.json()

##get Keys from Nagios:
keys=nagios_data.keys()
data=""
torque_header="T_State,T_Slots,T_SlotsUsed,T_AvailMem(MB),T_TotalMem(MB)/Swap,T_Time_Last_Rec,T_LoadAve,T_NetLoad(MB)".split(',')
ganglia_header="G_Swap_Total,G_Swap_Free,G_Swap_Used,G_Proc_Run,G_Cpu_User,G_Cpu_Wio,G_Load_One,G_Load,G_Five,G_Load_Fifteen,G_Mem_Cached,G_Mem_Total,G_Disk_Total,G_Disk_Free".split(',')
nagios_header="N_Status,N_Swap_Service,N_Swap_State,N_Swap_Info,N_IPMI_Service,N_IPMI_State,N_IPMI_Info,N_FreeSpace_Service,N_FreeSpace_State,N_FreeSpace_Info,N_CVMFS-OSG_Service,N_CVMFS-OSG_State,N_CVMFS-OSG_Info,N_CVMFS-CERN_Service,N_CVMFS-CERN_State,N_CVMFS-CERN_Info,N_CVMFS-CONDB_Service,N_CVMFS-CONDB_State,N_CVMFS-CONDB_Info".split(',')
data={}
count=0
for k in keys:
	#if k in ganglia_data and k in torque_data:

	data[k]=(zip(ganglia_header,ganglia_data[k].split(',')))+(zip(torque_header,torque_data[k].split(',')))+(zip(nagios_header,nagios_data[k].split(',')))
	#print (data)
	if count==2:
		break
	count=count+1
post={"date":datetime.datetime.utcnow(),
		"data":data}
print post
d=db.data
post_id=d.insert_one(post).inserted_id
print post_id
print db.collection_names(include_system_collections=False)

#dict(zip("N_Status,N_Swap_Service,N_Swap_State,N_Swap_Info,N_IPMI_Service,N_IPMI_State,N_IPMI_Info,N_FreeSpace_Service,N_FreeSpace_State,N_FreeSpace_Info,N_CVMFS-OSG_Service,N_CVMFS-OSG_State,N_CVMFS-OSG_Info,N_CVMFS-CERN_Service,N_CVMFS-CERN_State,N_CVMFS-CERN_Info,N_CVMFS-CONDB_Service,N_CVMFS-CONDB_State,N_CVMFS-CONDB_Info"
#.split(','),nagios_data['compute-6-26'].split(',')))


