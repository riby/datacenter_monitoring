#!/usr/bin/python
#
# Module to talk with a gmond and determine what hosts are reporting
# and some basic information
import socket
import xml.etree.cElementTree as ET
import time
now=time.time()

Hosts={}

###############################################
#  Wrapper for a Gmond host
#  Interested in Name, IP address, The last reported time and the load_one value
#
class GangliaHost:
    # What are we interested in for ganglia metrics?
    def __init__(self,name):       
        self.Name = name
        self.IP = None
        self.Reported = None
#        self.Load = None
	self.Swap_Free = None
	self.Swap_Total = None
	self.Proc_Run = None
	self.Cpu_Aidle = None
	self.Cpu_User = None
	self.Cpu_Wio = None
	self.Load_One = None
	self.Load_Five = None
	self.Load_Fifteen = None
	self.Mem_Cached = None
	self.Mem_Total= None
	self.Disk_Total = None
	self.Disk_Free = None
 
        
    def setIP(self,s): self.IP=s
    def setReported(self,s): self.Reported = s
    def setLoad(self,s): self.Load = s
    def setSwap_Free(self,s): self.Swap_Free = s
    def setSwap_Total(self,s): self.Swap_Total = s
    def setProc_Run(self,s): self.Proc_Run = s
    def setCpu_User(self,s): self.Cpu_User = s
    def setCpu_Wio(self,s): self.Cpu_Wio = s
    def getState(self,s): return self.State
    def setLoad_One(self,s): self.Load_One = s
    def setLoad_Five(self,s): self.Load_Five = s
    def setLoad_Fifteen(self,s): self.Load_Fifteen = s
    def setMem_Cached(self,s): self.Mem_Cached = s
    def setMem_Total(self,s): self.Mem_Total = s
    def setDisk_Total(self,s): self.Disk_Total = s
    def setDisk_Free(self,s): self.Disk_Free = s
    #
    # Generate the HTML summary status for the host including a link to node's
    # Ganglia page
    #
    def getSummary(self,GangliaURL):
        output='<a href="%s&h=%s"> %s </a><br><br>' % (GangliaURL, self.Name, self.Name)
        if self.Load:
            output += 'Load_one: %f<br>\n' % (self.Load)
        if self.IP:
            output+='IP address: %s<br>\n' % (self.IP)
        if self.Reported:
            output+='Time since last heard from (s): %d <br>\n' % (now - self.Reported)
            output+='Last Report timestamp: %s<br>\n' % (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(self.Reported)))
        output+='<br>\n'
        return output

#######################################################################
# Module level function to query Ganglia and get hosts
#
#
def getData(GMONDHost):
    # This whole thing needs to be bullet proofed
    # socket timeout
    # XML parsing should be a lot saner
    #
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((GMONDHost, 8651))
    data=''
    while True:
        buff = s.recv(4096)
        if len(buff) == 0:
            break
        else:
            data += buff
    s.close()
    #
    #
    # This is really meant to be a backstop so that 
    # problems with parsing can be traced back to the buffer
    # retrieved from the socket.  Should this exist?
    #f=open('/tmp/gmond','w')
    #f.write(data)
    #f.close()
    #
    #
    
    # gmond returns xml so use cElementTree to parse it
    # into a reasonable structure that can be iterated over
    # 
    root = ET.fromstring(data)
    #
    # gmond's <grid xxxx> tag is the first child of root
    # gmond's <cluster xxxx> tag is the first child of the grid tag
    grid=root[0]
    cluster=grid[0]
    #The children of the cluster tag should be <HOST xxxx> tags
    for elem in cluster:
        # Elem should be a  Host Tag
        #
        # Ganglia Name is FQDN
        # 
        #
        # from the <host > tag determine name, ip, and reporting time
        #
        host = GangliaHost(elem.attrib['NAME'])
        try:
            host.setIP(elem.attrib['IP'])
        except:
            pass
        
        try:
            host.setReported(int(elem.attrib['REPORTED']))
        except:
            pass
        #
        # the children of the host tag are <metric > tags
        # look for load_one
        #
        for metric in elem:
            if metric.attrib['NAME'] == 'load_one':
                host.setLoad_One(float(metric.attrib['VAL']))
                #break
	    elif metric.attrib['NAME'] == 'swap_free':
		host.setSwap_Free(float(metric.attrib['VAL']))
	    elif metric.attrib['NAME'] == 'swap_total':
		host.setSwap_Total(float(metric.attrib['VAL']))	
	    elif metric.attrib['NAME'] == 'proc_run':
		host.setProc_Run(float(metric.attrib['VAL']))	
            elif metric.attrib['NAME'] == 'cpu_user':
                host.setCpu_User(float(metric.attrib['VAL']))
            elif metric.attrib['NAME'] == 'cpu_wio':
                host.setCpu_Wio(float(metric.attrib['VAL']))
            elif metric.attrib['NAME'] == 'load_five':
                host.setLoad_Five(float(metric.attrib['VAL']))
            elif metric.attrib['NAME'] == 'load_fifteen':
                host.setLoad_Fifteen(float(metric.attrib['VAL']))
            elif metric.attrib['NAME'] == 'mem_cached':
                host.setMem_Cached(float(metric.attrib['VAL']))
            elif metric.attrib['NAME'] == 'mem_total':
                host.setMem_Total(float(metric.attrib['VAL']))
            elif metric.attrib['NAME'] == 'disk_total':
                host.setDisk_Total(float(metric.attrib['VAL']))
            elif metric.attrib['NAME'] == 'disk_free':
                host.setDisk_Free(float(metric.attrib['VAL']))
#def setProc_Run(self,s): self.Proc_Run = s
#    def setCpu_User(self,s): self.Cpu_User = s
#    def setCpu_Wio(self,s): self.Cpu_Wio = s

        Hosts[host.Name] = host
        #save particular metrics?
        # load one/five/fifteen
        # free space on disk
        # swap usage
        # os version
        # bytes in/ out
        # what about ganglia hosts without these metrics
        #    switch CPU usage
        #    CRAC issues

        #if elem.attrib['NAME'] == 'compute-1-26.local':
        #    for metric in elem:
        #        # each elem should be wrapping a node
        #        print metric.tag, metric.attrib
 
if __name__ == '__main__':
    # For testing service assume this machine has a gmond that listens
    import sys

    if len(sys.argv) > 1:
        host=sys.argv[1]
    else:
        host='localhost'

    now=time.time()
    getData(host)
    for h in Hosts.values():
	if h.Swap_Free !=None:
        	print h.Name, h.IP, h.Reported, now-h.Reported,h.Swap_Total,h.Swap_Free,(h.Swap_Total-h.Swap_Free)
