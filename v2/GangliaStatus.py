#!/usr/bin/python
#
#
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
    # Binding all Host information to the object of machine
    def __init__(self,name):       
	self.Name = name           # Name of the Host
	self.IP = None
	self.Reported = None
	self.Swap_Free = None      # Amount of free swap space
	self.Swap_Total = None     # Amount of total swap space
	self.Proc_Run = None       # Number of running processes
	self.Cpu_Aidle = None      # Percentage of CPU cycles spent idle since last boot 
	self.Cpu_User = None       # Percentage of CPU cycles spent in user mode
	self.Cpu_Wio = None        # Percentage of CPU cycles spent waiting for I/O 
	self.Load_One = None       # Reported system load, averaged over one minute
	self.Load_Five = None      # Reported system load, averaged over five minutes
	self.Load_Fifteen = None   # Reported system load, averaged over fifteen minutes
	self.Mem_Cached = None     # Amount of memory allocated to cached data 
	self.Mem_Total= None       # Total amount of physical memory
	self.Disk_Total = None     # Total capacity on the fullest local disk partition
	self.Disk_Free = None      # Total free space on the fullest local disk partition
        
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
        try:
            buff = s.recv(4096)
            if len(buff) == 0:
                break
            else:
                data += buff
        except socket.error, e:
            print "Socket Error Occured"
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

#if __name__ == '__main__':
    # For testing service assume this machine has a gmond that listens
#    import sys

#    if len(sys.argv) > 1:
#        host=sys.argv[1]
#    else:
#        host='localhost'

#    getData(host)
    #for h in Hosts.values():
#	if h.Swap_Free !=None:
#        	print h.Name, h.IP, h.Reported, now-h.Reported,h.Swap_Total,h.Swap_Free,(h.Swap_Total-h.Swap_Free)
