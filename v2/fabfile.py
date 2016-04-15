from fabric.api import run,hosts
from fabric.context_managers import env
from StringIO import StringIO
from fabric.api import get

env.hosts = ['monitor']
env.password = 'KXUb##doN6'

Hosts={}
class FileSshGet:
	def __init__(self,name):
		self.compute_nodes = compute_nodes
		self.storage_nodes = storage_nodes
		self.switches = switches
@hosts(['monitor'])
def run_on_host():
	env.host_string='monitor'
	run('python /cluster/home/rsidhu/code/NagiosStatus.py')

@hosts(['monitor'])
def getValue():
	env.host_string='monitor'
	st=['compute_nodes','storage_nodes','switches']
	for s in st:
		content=open("/cluster/home/rsidhu/code/"+str(s)+".csv", 'r').readlines()
		Hosts[s]=content
