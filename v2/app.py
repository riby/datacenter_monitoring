#!flask/bin/python
from flask import Flask, jsonify
import GangliaStatus
from flask import Response
import fabfile as fb
import TorqueStatus as TS
from flask import render_template
import time
import logging
from logging.handlers import RotatingFileHandler

Hosts={}

app = Flask(__name__)

# We need to define headers from compute nodes, storage nodes and switches for future ease if attributes required for action
upper_id={"compute_nodes":"Timestamp,Status,Swap_Service,Swap_State,Swap_Info,IPMI_Service,IPMI_State,IPMI_Info,FreeSpace_Service,FreeSpace_State,FreeSpace_Info,CVMFS-OSG_Service,CVMFS-OSG_State,CVMFS-OSG_Info,CVMFS-CERN_Service,CVMFS-CERN_State,CVMFS-CERN_Info,CVMFS-CONDB_Service,CVMFS-CONDB_State,CVMFS-CONDB_Info","storage_nodes":"Timestamp,Status,XrootD_Service,XrootD_State,XrootD_Info,OMReport_Service,OMReport_State,OMReport_Info","switches":"Timestamp,Status,PowerSupply_Service,PowerSupply_State,PowerSupply_Info,GlobalStatus_Service,GlobalStatus_State,GlobalStatus_Info,Fan_Service,Fan_State,Fan_Info" }

@app.route('/', methods=['GET'])
def test_server():
    return "Hello World"
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 4044

@app.errorhandler(500)
def internal_server_error(error):
    app.logger.error('Server Error: %s', (error))
    return render_template('500.html'), 500


@app.route('/atlas/nagios/<string:device>',methods=['GET','POST'])
def get_nagios_data(device):
    #device can be 'compute_nodes' or 'storage_nodes' or 'switches': Depending on the variable passed
    fb.run_on_host()	#Runs the file on Monitor machine to create snapshot of states of all machines
    fb.getValue()	#Get value by extracting data received from Nagios	
    data=fb.Hosts[device] #Extract the devices based on params
    dict_return={}
    ## Removal of extra attibutes from the data and set into dictionary
    for line in data:
        l=line.split(',')
	dict_return[l[1]]=','.join(l[2:])

    return jsonify(dict_return) #Return the results back in json format


@app.route('/atlas/torque',methods=['GET'])
def get_torque_data():
    TS.getData()
    lst=[]
    dct=dict()
    Hosts=TS.Hosts
    #dct['Host']='State,Slots,SlotsUsed,AvailMem(MB),TotalMem(MB)or Swap,Time_Last_Rec,LoadAve,NetLoad(MB)'
    Job_State_Dict={"down":0,"free":1,'job-exclusive':2,'job-sharing':3,'offline':4,'reserve':5,'time-shared':6,'unknown':7}
    for h in Hosts.values():
	#data is cleaned ,clean JOB list(not Required)
	if h.RecTime is None:
        	continue
	t=round(time.time()-int(h.RecTime),2)
	l1=(str(Job_State_Dict[h.State[0]])+","+str(h.Slots)+","+str(h.SlotsUsed)+","+str(round(float(h.AvailMem[0:-2])/1024,2))+","+str(round(float(h.TotalMem[0:-2])/1024,2))+','+str(t)+","+str(h.LoadAve)+","+str(round(float(h.NetLoad)/(1024*1024),2)))
	dct[h.Name]=l1
                #lst.append(dict)    
    #print dct
    return jsonify(dct)




@app.route('/atlas/ganglia',methods=['GET'])
def get_ganglia_data():
    GangliaStatus.getData('admin')
    lst=[]
    dct=dict()
    Hosts=GangliaStatus.Hosts
    #dct['aahosts']='Swap_Total,Swap_Free,Swap_Used,Proc_Run,Cpu_User,Cpu_Wio,Load_One,Load,Five,Load_Fifteen,Mem_Cached,Mem_Total,Disk_Total,Disk_Free'
    for h in Hosts.values():
        if h.Swap_Free !=None:
    #            print h.Name, h.IP, h.Reported, h.Swap_Total,h.Swap_Free,(h.Swap_Total-h.Swap_Free)
		#lst.append(h.Name+","+ str(h.IP)+","+str(h.Swap_Total)+","+str(h.Swap_Free)+","+str(h.Swap_Total-h.Swap_Free))
		l1=(str(round((h.Swap_Total)/1024,2))+","+str(round((h.Swap_Free)/1024,2))+","+str(round(h.Swap_Total/1024-h.Swap_Free/1024,2))+","+str(h.Proc_Run)+","+str(h.Cpu_User)+","+str(h.Cpu_Wio)+','+str(h.Load_Five)+','+str(h.Load_Fifteen)+','+str(h.Mem_Cached)+','+str(h.Mem_Total)+','+str(h.Disk_Total)+','+str(h.Disk_Free))
		dct[h.Name[0:-6]]=l1   # cut .local to keep in syn
		#lst.append(dict)    
    #print dct
    return jsonify(dct) 
    #return Response(json.dumps(dct),  mimetype='application/json')
if __name__ == '__main__':
    print 'End Points /atlas/ganglia  /todo/api/v1.0/tasks'
    handler = RotatingFileHandler('server.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(host='0.0.0.0',port='8080')
