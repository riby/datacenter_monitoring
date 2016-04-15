import GangliaStatus
Hosts={}
GangliaStatus.getData('admin')
Hosts=GangliaStatus.Hosts
lst=[]
for h in Hosts.values():
	if h.Swap_Free !=None:
		print h.Name, h.IP, h.Reported, h.Swap_Total,h.Swap_Free,(h.Swap_Total-h.Swap_Free)
		lst.append(h.Name+","+ str(h.IP)+","+str(h.Swap_Total)+","+str(h.Swap_Free)+","+str(h.Swap_Total-h.Swap_Free))

