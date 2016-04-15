#!/usr/bin/python
#
# Expect PBSQuery to be installed and that this machine
# can run pbsnodes to query torque server
from PBSQuery import PBSQuery, PBSError
import WrapperQStat
import re
Hosts={}


# The wrapper class for a Torque compute node
#
class TorqueHost:
    # What are we interested in from Torque?
    def __init__(self,name):       
        self.Name = name         # Node name based on torque server's node list
        self.State = None        # List of Torque states (free, job-exclusive, down, offline)
        self.Slots = None        # number of job slots define to torque server's node list
        self.SlotsUsed = None    # number of slots being used
        self.Jobs = None         # number of torque jobs on that node (as seen by mom?)
	self.AvailMem = None	 # Available Memory on each node
	self.TotalMem = None	 # Total Memory present on a machine
	self.RecTime = None	 # React time of a node
	self.LoadAve = None	 # Average load each second on node
	self.NetLoad = None      # Average load  Netload
    def setState(self,s): self.State=s
    def setSlots(self,s): self.Slots = s
    def setSlotsUsed(self,c): self.SlotsUsed = c
    def setJobList(self,j): self.Jobs=j
    def setAvailMem(self,s): self.AvailMem=s
    def setTotalMem(self,s): self.TotalMem=s
    def setRecTime(self,s): self.RecTime=s
    def setLoadAve(self,s): self.LoadAve=s
    def setNetLoad(self,s): self.NetLoad=s

########################################################################################################
# Moduel level function to fill the module level Hosts()
# 
def getData():
    p=PBSQuery()
    nodes=p.getnodes()
    for node in nodes.keys():
        host=TorqueHost(node)

#	Counting number of Cores in each sys based on type of jobs running
#
	count_core=0
        try:
            lst=WrapperQStat.multi_core_list
            jb=nodes[node]['status']['jobs'][0].split()
            for j in jb:
                l=re.sub('\.atlas-swt2.org','',j)
                if l in lst:
                        count_core=count_core+8
                else:
                        count_core=count_core+1
            host.setSlotsUsed(count_core)
        except:
            host.setSlotsUsed(0)
        try:
            host.setState(nodes[node]['state'])
        except:
            pass
        try:
            host.setSlots(int(nodes[node]['np'][0]))
        except:
            pass
        try:
            jobs=nodes[node]['status']['jobs'][0].split()
            host.setJobList(jobs)
        except:
            pass
        try:
            availmem=nodes[node]['status']['availmem'][0]
            host.setAvailMem((availmem))
        except:
            pass
        try:
            totalmem=nodes[node]['status']['totmem'][0]
            host.setTotalMem((totalmem))
        except:
            pass
        try:
            rectime=nodes[node]['status']['rectime'][0]
            host.setRecTime((rectime))
        except:
            pass
        try:
            loadave=nodes[node]['status']['loadave'][0]
            host.setLoadAve((loadave))
        except:
            pass
        try:
            netload=nodes[node]['status']['netload'][0]
            host.setNetLoad((netload))
        except:
            pass

        Hosts[host.Name] = host

if __name__ == '__main__':
    getData()
    #print Hosts.keys()
#    for h in Hosts.values():
#        print h.Name, h.State, h.Slots, h.SlotsUsed, h.Jobs
#	print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
#	print h
#	break

