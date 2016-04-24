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
    # Write some HTML about the state of this service
    # These colors are associated with the colors for nagios status
    # shown in RackStatus.css
    def getSummary(self):
        if self.State==0:
            state='OK'
            stateColor='green'
        elif self.State == 1:
            state='Warning'
            stateColor='Gold'
        elif self.State == 2:
            if self.Ack:
                state = 'Critical-Acked'
                stateColor = 'LightPink'
            else:
                state ='Critical'
                stateColor='red'
        else:
            state = 'Unknown'
            stateColor='orange'

        output='<tr><td>%s</td><td style="color: %s;font-weight: bold;">%s</td><td>%s</td></tr>\n' % (self.Name, stateColor, state, self.Info)
        return output

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

    #
    # Cycle throuh the service to determine how many service are in an Alert Count
    # and how many are Acknowledged
    #
    def getAlertCount(self):  #Get this to return a dict
        count={'count':0,'Acks':0}
        for s in self.Services:
            if s.State ==2:
                count['count'] += 1
            if s.Ack:
                count['Acks'] +=1
        return count
    #
    # Cycle through service and count warnings
    #
    def getWarningCount(self):
        count = 0
        for s in self.Services:
            if s.State ==1:
                count += 1
        return count

    #
    # Cycle through service and count number of serives with an Unknown status
    #
    def getUnknownCount(self):
        count = 0
        for s in self.Services:
            if s.State ==3:
                count += 1
        return count
    #
    # Generate the HTML Nagios Status of a Node and its services
    #
    #
    def getSummary(self,NagiosURL):
        output='<a href="%s/status.cgi?host=%s">Service Details</a><br>\n' % (NagiosURL, self.Name)
        output +='<a href="%s/extinfo.cgi?type=1&host=%s">Host Details</a><br><br>\n' % (NagiosURL, self.Name)

        if self.State == 0:
            state = 'UP'
        else:
            state = 'Down'
        output +='State: %s<br>\n' % (state)
        if len(self.Services) > 0:
            output +='Services:<br>\n'
            output +='<table><tr><th>Name</th><th>State</th><th>Information</th></tr>'
            for s in self.Services:
                output += s.getSummary()
            output += '</table>'
        return output

#
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
        buff = s.recv(4096)
        if len(buff) == 0:
            break
        else:
            answer += buff
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

    f_storage=open(SCRIPT_DIR+'storage_nodes.csv','w+')
    f_compute=open(SCRIPT_DIR+'compute_nodes.csv','w+')
    f_switches=open(SCRIPT_DIR+"switches.csv","w+")
    
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
