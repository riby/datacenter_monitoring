import requests
import time
import datetime
from pymongo import MongoClient

client = MongoClient()
db = client['data_monitor']

ganglia_req = requests.get('http://129.107.255.31:8080/atlas/ganglia')
torque_req = requests.get('http://129.107.255.31:8080/atlas/torque')

nagios_req = requests.get('http://129.107.255.31:8080/atlas/nagios/compute_nodes')
machine=['compute-2-29',  'compute-9-30', 'compute-9-36', 'compute-9-35','compute-9-34','compute-2-23', 'compute-2-25', 'compute-2-24', 'compute-2-27', 'compute-2-26', 'compute-6-29', 'compute-6-28', 'compute-6-25', 'compute-6-24', 'compute-6-27', 'compute-6-26', 'compute-6-23', 'compute-9-33', 'compute-9-32', 'compute-22-17', 'compute-22-16', 'compute-22-15', 'compute-22-14', 'compute-22-13', 'compute-22-12', 'compute-22-11', 'compute-22-18', 'compute-7-39', 'compute-7-38', 'compute-21-29', 'compute-21-28', 'compute-21-27', 'compute-21-26', 'compute-21-25', 'compute-21-24', 'compute-21-23', 'compute-5-1', 'compute-14-1', 'compute-14-2', 'compute-14-3', 'compute-14-4', 'compute-14-5', 'compute-14-6', 'compute-14-7', 'compute-14-8', 'compute-13-6', 'compute-13-5', 'compute-13-4', 'compute-7-40', 'compute-13-2', 'compute-13-1', 'compute-14-30', 'compute-5-8', 'compute-14-32', 'compute-14-33', 'compute-14-34', 'compute-14-35', 'compute-18-18', 'compute-14-37', 'compute-14-38', 'compute-18-17', 'compute-5-3', 'compute-18-15', 'compute-5-5', 'compute-18-13', 'compute-5-7', 'compute-5-6', 'compute-6-2', 'compute-3-41', 'compute-6-1', 'compute-6-6', 'compute-6-7', 'compute-6-4', 'compute-6-5', 'compute-6-8', 'compute-13-28', 'compute-13-29', 'compute-13-26', 'compute-13-27', 'compute-13-24', 'compute-13-25', 'compute-13-23', 'compute-2-10', 'compute-2-11', 'compute-2-12', 'compute-2-14', 'compute-2-15', 'compute-2-16', 'compute-2-17', 'compute-2-18', 'compute-14-40', 'compute-2-8', 'compute-2-9', 'compute-2-7', 'compute-20-40', 'compute-1-9', 'compute-1-8', 'compute-6-11', 'compute-8-40', 'compute-6-14', 'compute-6-15', 'compute-6-16', 'compute-6-17', 'compute-6-10', 'compute-5-4', 'compute-6-12', 'compute-6-13', 'compute-6-18', 'compute-4-29', 'compute-4-28', 'compute-23-38', 'compute-22-2', 'compute-23-36', 'compute-23-37', 'compute-23-34', 'compute-23-35', 'compute-4-27', 'compute-23-33', 'compute-4-25', 'compute-11-18', 'compute-8-38', 'compute-8-39', 'compute-11-17', 'compute-11-16', 'compute-22-40', 'compute-1-11', 'compute-1-10', 'compute-1-13', 'compute-1-12', 'compute-1-15', 'compute-1-14', 'compute-1-17', 'compute-1-16', 'compute-5-15', 'compute-5-14', 'compute-12-8', 'compute-5-16', 'compute-5-11', 'compute-5-10', 'compute-5-13', 'compute-5-12', 'compute-12-2', 'compute-12-3', 'compute-12-1', 'compute-12-6', 'compute-12-7', 'compute-12-4', 'compute-12-5', 'compute-12-27', 'compute-12-26', 'compute-12-18', 'compute-19-37', 'compute-19-36', 'compute-12-10', 'compute-12-11', 'compute-12-12', 'compute-12-13', 'compute-12-14', 'compute-12-15', 'compute-12-16', 'compute-12-17', 'compute-20-37', 'compute-20-36', 'compute-20-35', 'compute-20-39', 'compute-20-38', 'compute-23-39', 'compute-23-32', 'compute-4-26', 'compute-23-30', 'compute-12-23', 'compute-12-22', 'compute-12-25', 'compute-12-24', 'compute-19-39', 'compute-19-38', 'compute-12-29', 'compute-12-28', 'compute-19-35', 'compute-9-27', 'compute-21-40', 'compute-9-28', 'compute-9-29', 'compute-11-40', 'compute-21-38', 'compute-21-39', 'compute-21-30', 'compute-21-33', 'compute-21-34', 'compute-21-35', 'compute-21-36', 'compute-21-37', 'compute-5-28', 'compute-5-29', 'compute-5-24', 'compute-5-25', 'compute-5-26', 'compute-5-27', 'compute-5-23', 'compute-13-18', 'compute-13-13', 'compute-13-12', 'compute-13-11', 'compute-13-10', 'compute-13-17', 'compute-13-16', 'compute-13-15', 'compute-13-14', 'compute-14-15', 'compute-22-39', 'compute-22-38', 'compute-22-30', 'compute-22-33', 'compute-22-35', 'compute-22-34', 'compute-22-37', 'compute-22-36', 'compute-7-17', 'compute-7-16', 'compute-7-18', 'compute-5-17', 'compute-14-18', 'compute-14-12', 'compute-14-13', 'compute-14-10', 'compute-14-11', 'compute-14-16', 'compute-14-17', 'compute-14-14', 'compute-5-18', 'compute-21-8', 'compute-21-1', 'compute-21-2', 'compute-21-3', 'compute-21-4', 'compute-21-5', 'compute-21-6', 'compute-21-7', 'compute-4-30', 'compute-18-14', 'compute-23-27', 'compute-23-26', 'compute-12-37', 'compute-12-38', 'compute-21-11', 'compute-5-39', 'compute-5-38', 'compute-5-37', 'compute-5-36', 'compute-5-35', 'compute-5-34', 'compute-5-33', 'compute-5-32', 'compute-5-30', 'compute-22-3', 'compute-18-35', 'compute-22-1', 'compute-18-37', 'compute-22-7', 'compute-22-6', 'compute-22-5', 'compute-22-4', 'compute-22-8', 'compute-18-38', 'compute-18-39', 'compute-20-15', 'compute-20-17', 'compute-20-16', 'compute-20-18', 'compute-9-25', 'compute-2-38', 'compute-2-39', 'compute-2-36', 'compute-2-37', 'compute-2-34', 'compute-2-35', 'compute-2-32', 'compute-2-33', 'compute-2-30', 'compute-6-32', 'compute-6-33', 'compute-6-30', 'compute-6-36', 'compute-6-37', 'compute-6-34', 'compute-6-35', 'compute-6-38', 'compute-6-39', 'compute-9-26', 'compute-21-12', 'compute-21-13', 'compute-23-16', 'compute-23-17', 'compute-21-16', 'compute-21-17', 'compute-21-14', 'compute-21-15', 'compute-21-18', 'compute-23-18', 'compute-8-18', 'compute-8-16', 'compute-8-17', 'compute-11-39', 'compute-11-38', 'compute-22-28', 'compute-22-29', 'compute-22-23', 'compute-22-26', 'compute-22-27', 'compute-22-24', 'compute-22-25', 'compute-13-8', 'compute-13-7', 'compute-19-13', 'compute-19-15', 'compute-19-14', 'compute-19-17', 'compute-19-16', 'compute-13-3', 'compute-14-27', 'compute-14-26', 'compute-14-25', 'compute-14-24', 'compute-14-23', 'compute-14-36', 'compute-14-29', 'compute-14-28', 'compute-18-16', 'compute-14-39', 'compute-3-39', 'compute-3-38', 'compute-5-2', 'compute-13-39', 'compute-13-38', 'compute-13-35', 'compute-13-34', 'compute-13-37', 'compute-13-36', 'compute-13-30', 'compute-13-33', 'compute-13-32', 'compute-3-40', 'compute-6-3', 'compute-13-40', 'compute-18-36', 'compute-23-29', 'compute-23-28', 'compute-23-25', 'compute-4-32', 'compute-4-33', 'compute-4-34', 'compute-4-35', 'compute-19-40', 'compute-18-40']
keys=machine
#r.json()
#for k,v in r.json:
#	print k

ganglia_data = ganglia_req.json()

torque_data = torque_req.json()

nagios_data = nagios_req.json()

##get Keys from Nagios:
#keys=nagios_data.keys()

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
	#if count==2:
	#	break
	#count=count+1
post={"date":datetime.datetime.utcnow(),
		"data":data}
#print post
d=db.data
post_id=d.insert_one(post).inserted_id
print post_id
print db.collection_names(include_system_collections=False)

#dict(zip("N_Status,N_Swap_Service,N_Swap_State,N_Swap_Info,N_IPMI_Service,N_IPMI_State,N_IPMI_Info,N_FreeSpace_Service,N_FreeSpace_State,N_FreeSpace_Info,N_CVMFS-OSG_Service,N_CVMFS-OSG_State,N_CVMFS-OSG_Info,N_CVMFS-CERN_Service,N_CVMFS-CERN_State,N_CVMFS-CERN_Info,N_CVMFS-CONDB_Service,N_CVMFS-CONDB_State,N_CVMFS-CONDB_Info"
#.split(','),nagios_data['compute-6-26'].split(',')))


