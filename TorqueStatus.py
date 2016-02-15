#!/usr/bin/python
#
# Expect PBSQuery to be installed and that this machine
# can run pbsnodes to query torque server
from PBSQuery import PBSQuery, PBSError

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
	self.AvailMem = None
	self.TotalMem = None
        
    def setState(self,s): self.State=s
    def setSlots(self,s): self.Slots = s
    def setSlotsUsed(self,c): self.SlotsUsed = c
    def setJobList(self,j): self.Jobs=j
    def setAvailMem(self,s): self.AvailMem=s
    def setTotalMem(self,s): self.TotalMem=s
    #
    # Generate HTML description for the node (mostly point to CGI script)
    def getSummary(self,CGIURL='Something'):
        output='' 
        if self.State:
            output+='State: %s' %(self.State[0])
            for s in self.State[1:]:
                output+=',%s ' %(s)
            output+='<br>\n'
        if self.Slots and self.SlotsUsed:
            output+='<table><caption>Slots</caption><tr><th>Used</th><th>Defined</th></tr>'
            output+='<tr><td>%d</td><td>%d</td></tr></table><br>\n' % (self.SlotsUsed, self.Slots)            
        if self.Jobs:
            output+='Number of Jobs: %d<br>\n' % (len(self.Jobs))

        output+='<a href="%s%s">Live pbsnodes information</a>\n' % (CGIURL, self.Name)
        return output
########################################################################################################
# Moduel level function to fill the module level Hosts()
# 
def getData():
    p=PBSQuery()
    nodes=p.getnodes()
    for node in nodes.keys():
        host=TorqueHost(node)
        try:
            host.setState(nodes[node]['state'])
        except:
            pass

        try:
            host.setSlots(int(nodes[node]['np'][0]))
        except:
            pass

        try:
            host.setSlotsUsed(len(nodes[node]['jobs']))
        except:
            host.setSlotsUsed(0)

        try:
            jobs=nodes[node]['status']['jobs'][0].split()
            host.setJobList(jobs)
        except:
            pass
        try:
            availmem=nodes[node]['status']['availmem'][0]
            host.setAvailMem(availmem)
        except:
            pass
        try:
            totalmem=nodes[node]['status']['totmem'][0]
            host.setTotalMem(totalmem)
        except:
            pass
        Hosts[host.Name] = host

if __name__ == '__main__':
    getData()
    #print Hosts.keys()
    for h in Hosts.values():
        print h.Name, h.State, h.Slots, h.SlotsUsed, h.Jobs
#	print '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$'
#	print h
#	break

