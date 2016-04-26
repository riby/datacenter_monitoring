#!/usr/bin/python
# Module to retrieve information about nodes from Nagios
# It is assumed that this runs on the Nagios host AND
# that nagios is using the MKLivestatus event broker module
# that is compiled separately.
#
import socket



Hosts={}
############
# Wrapper class for a Nagios SERVICE
# A service has a Name, a state, associated information and an indication
# if an issue has been acknowledged.
#
#
class NagiosService:
    def __init__(self,name):
        self.Name = name
        self.State = None
        self.Info = None
        self.Ack = False

    def setState(self,s): self.State=s
    def setInfo(self,i): self.Info=i
    def setAck(self,a, ): self.Ack = a

############################################################
# A wrapper class for a Nagios Host
# hosts have a state (based on its check_command)
# and any number of services
#
class NagiosHost:
    def __init__(self,name):
        self.Name = name
        self.State = None
	self.Group = None
        self.Services=[]
    def setState(self,s): self.State=s
    def setGroup(self,s): self.Group=s
    def addService(self,s): self.Services.append(s)
    def getState(self,s): return self.State

# Module level function to populate Hosts{} with discoved nodes
#
#
def getData(NagiosSocket):
    #NagiosSocket is a file (pipe) created by Nagios via MKLivestatus
    #
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect(NagiosSocket)

    # Write command to socket
    s.send("GET hosts\n")
    #s.send("GET services\n")
    s.send("Columns: groups name state services_with_fullstate\n")
    s.send("ColumnHeaders: on\n")
    s.send("OutputFormat: python\n")

    # Important: Close sending direction. That way
    # the other side knows we are finished.
    s.shutdown(socket.SHUT_WR)

    #Now retrieve data
    answer=''
    while True:
        try:
            buff = s.recv(4096)
            if len(buff) == 0:
                break
            else:
                answer += buff
        except socket.error, e:
            print "Socket Error Occured"
    s.close()

    # This is meant as a backstop for when the eval
    # fails and we want to see what was eval'ed
    # probably shouldn't be here
    #f=open('/tmp/RackStatus-nagios','w')
    #f.write(answer)
    #f.close()
    
    h=eval(answer)

    #h[0] is column headers
    #h[1-n] is columns per host
    for index,row in enumerate(h[1:]):
        rawdict=dict((key, value) for (key, value) in zip(h[0],row))
       
	host=NagiosHost(rawdict['name'])
        host.setState(rawdict['state'])
	host.setGroup(rawdict['groups'])
        for s in rawdict['services_with_fullstate']:
            service=NagiosService(s[0])
            service.setState(s[1])
            service.setInfo(s[3])
            # Should this be specified better
            if s[-1] == 1:
                service.setAck(True)
            host.addService(service)
        Hosts[host.Name] = host


if __name__ == '__main__':
    import sys
    import time
    import datetime
    import os
    #Path of script and config is same, we will extract the path from OS
 
    SCRIPT_DIR=os.path.dirname(os.path.realpath(__file__))

    if len(sys.argv) > 1:
        pipe=sys.argv[1]
    else:
        pipe='/var/log/nagios/live'
    # Need to allow arguments so that value can be added
    getData(pipe)
    l=Hosts.values()
    
    print 'Hosts discovered:', len(Hosts)

    node=l[0]
    ts=time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    f_storage=open(SCRIPT_DIR+'/storage_nodes.csv','w+')
    f_compute=open(SCRIPT_DIR+'/compute_nodes.csv','w+')
    f_switches=open(SCRIPT_DIR+"/switches.csv","w+")
    
    #In case we need header information it is below for each segment of machines

    #Compute: ("Timestamp,Device_Name,Status,Swap_Service,Swap_State,Swap_Info,IPMI_Service,IPMI_State,IPMI_Info,FreeSpace_Service,FreeSpace_State,FreeSpace_Info,CVMFS-OSG_Service,CVMFS-OSG_State,CVMFS-OSG_Info,CVMFS-CERN_Service,CVMFS-CERN_State,CVMFS-CERN_Info,CVMFS-CONDB_Service,CVMFS-CONDB_State,CVMFS-CONDB_Info\n")
    #Storage: ("Timestamp,Device_Name,Status,XrootD_Service,XrootD_State,XrootD_Info,OMReport_Service,OMReport_State,OMReport_Info\n")
    #Switches: ("Timestamp,Device_Name,Status,PowerSupply_Service,PowerSupply_State,PowerSupply_Info,GlobalStatus_Service,GlobalStatus_State,GlobalStatus_Info,Fan_Service,Fan_State,Fan_Info\n")
    for l1 in l:
	st=""
        for s in l1.Services:
            st=st+str(s.Name)+","+str(s.State)+","+str(s.Info).replace(",","/")+","
        group=''.join(l1.Group)
        if group=="storage-nodes":
		f_storage.write(timestamp+","+l1.Name+","+str(l1.State)+","+st+"\n")
	elif group=="compute-nodes":
		f_compute.write(timestamp+","+l1.Name+","+str(l1.State)+","+st+"\n")
	elif group=="4032-switches" or group=="6248-switches":
		f_switches.write(timestamp+","+l1.Name+","+str(l1.State)+","+st+"\n")
    print "Done Writing Files"
