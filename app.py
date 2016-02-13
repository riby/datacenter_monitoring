#!flask/bin/python
from flask import Flask, jsonify
import GangliaStatus
from flask import Response
import fabfile as fb
#Hosts={}

app = Flask(__name__)


@app.route('/', methods=['GET'])
def test_server():
    return "Hello World"

@app.route('/atlas/nagios',methods=['GET'])
def get_nagios_data():
    fb.getValue()
    Hosts=fb.Hosts
    print len(Hosts)
    return jsonify(Hosts)
@app.route('/atlas/ganglia',methods=['GET'])
def get_ganglia_data():
    GangliaStatus.getData('admin')
    lst=[]
    dct=dict()
    Hosts=GangliaStatus.Hosts
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
