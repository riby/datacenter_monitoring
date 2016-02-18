import TorqueStatus as TS
import time
TS.getData()
lst=[]
dct=dict()
Job_State_Dict={"free":1,'job-exclusive':2,'job-sharing':3,'offline':4,'reserve':5,'time-shared':6,'unknown':7} 
Hosts=TS.Hosts
for h in Hosts.values():
#    l1=(str(h.State)+","+str(h.Slots)+","+str(h.SlotsUsed)+","+str(h.Jobs)+","+str(h.AvailMem)+","+str(h.TotalMem))# last is memory used
    t=time.time()-int(h.RecTime)
    t=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(h.RecTime))
    l1=(str(Job_State_Dict[h.State[0]])+","+str(h.Slots)+","+str(h.SlotsUsed)+","+str(round(int(h.AvailMem[0:-2])/1024,2))+","+str(round(int(h.TotalMem[0:-2])/1024,2))+","+str((int(h.TotalMem[0:-2])-int(h.AvailMem[0:-2])))+','+str(t)+","+str(h.LoadAve)+","+str(round(int(h.NetLoad)/(1024*1024),2)))
    dct[h.Name]=l1
            #lst.append(dict)    
print dct

