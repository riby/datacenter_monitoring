from fabric.api import run,hosts
from fabric.context_managers import env
from StringIO import StringIO
from fabric.api import get

#env.passwords = {'rsidhu@monitor': 'KXUb##doN6'}
env.hosts = ['monitor']
env.password = 'KXUb##doN6'
#print env
Hosts={}
class FileSshGet:
	def __init__(self,name):
		self.compute_nodes = compute_nodes
		self.storage_nodes = storage_nodes
		self.switches = switches
def run_on_host():
	run('python /cluster/home/rsidhu/code/NagiosStatus.py')
#	fd = StringIO()
#	get('/cluster/home/rsidhu/code/compute_nodes.csv', fd)
#	content=fd.getvalue()
#	print content
@hosts(['monitor'])
def getValue():
	#env.host='monitor'
	env.host_string='monitor'
	st=['compute_nodes','storage_nodes','switches']
	for s in st:
	#	fd = StringIO()
	#	get("/cluster/home/rsidhu/code/"+str(s)+".csv", fd)
		content=open("/cluster/home/rsidhu/code/"+str(s)+".csv", 'r').readlines()
		#get(s,fd)
		#content=fd.getvalue()
        	#print content
		#print type(content)
		Hosts[s]=content
	#print (Hosts['compute_nodes'])
#print Hosts['compute_nodes']
#print Hosts
#from StringIO import StringIO
#from fabric.api import get

#fd = StringIO()
#get('/cluster/home/rsidhu/code/compute_nodes.csv', fd)
#content=fd.getvalue()
#print content

