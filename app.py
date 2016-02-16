#!flask/bin/python
from flask import Flask, jsonify
import GangliaStatus
from flask import Response
import fabfile as fb
import TorqueStatus as TS
Hosts={}

app = Flask(__name__)


@app.route('/', methods=['GET'])
def test_server():
    return "Hello World"

@app.route('/atlas/nagios/<string:device>',methods=['GET','POST'])
def get_nagios_data(device):
    #device='compute_nodes'
    #if Hosts=={}:
    fb.getValue()
    Hosts=fb.Hosts
    data=Hosts[device]
    dict_return={}
    count=0
    for line in data:
        l=line.split(',')
	dict_return[l[1]]=l[0]+','+','.join(l[2:])
    #print len(dict_return)
    #return "hello"
    return jsonify(dict_return)


@app.route('/atlas/torque',methods=['GET'])
def get_torque_data():
    TS.getData()
    lst=[]
    dct=dict()
    Hosts=TS.Hosts
    dct['Host']='State,Slots,SlotsUsed,Jobs,AvailMem,TotalMem'
    for h in Hosts.values():
	l1=(str(h.State[0])+","+str(h.Slots)+","+str(h.SlotsUsed)+","+str(h.Jobs)+","+str(h.AvailMem)+","+str(h.TotalMem))# last is memory used
	dct[h.Name]=l1
                #lst.append(dict)    
    print dct
    return jsonify(dct)




@app.route('/atlas/ganglia',methods=['GET'])
def get_ganglia_data():
    GangliaStatus.getData('admin')
    lst=[]
    dct=dict()
    Hosts=GangliaStatus.Hosts
    dct['hosts']='IP,Swap_Total,Swap_Free,Swap_Used,Proc_Run,Cpu_User,Cpu_Wio'
    for h in Hosts.values():
        if h.Swap_Free !=None:
    #            print h.Name, h.IP, h.Reported, h.Swap_Total,h.Swap_Free,(h.Swap_Total-h.Swap_Free)
		#lst.append(h.Name+","+ str(h.IP)+","+str(h.Swap_Total)+","+str(h.Swap_Free)+","+str(h.Swap_Total-h.Swap_Free))
		l1=(str(h.IP)+","+str(h.Swap_Total)+","+str(h.Swap_Free)+","+str(h.Swap_Total-h.Swap_Free)+","+str(h.Proc_Run)+","+str(h.Cpu_User)+","+str(h.Cpu_Wio))
		dct[h.Name]=l1
		#lst.append(dict)    
    print dct
    return jsonify(dct) 
    #return Response(json.dumps(dct),  mimetype='application/json')
if __name__ == '__main__':
    print 'End Points /atlas/ganglia  /todo/api/v1.0/tasks'
    app.run(host='0.0.0.0',port='8080')
