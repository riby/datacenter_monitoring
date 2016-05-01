from fabric.api import run,hosts
from fabric.context_managers import env
from StringIO import StringIO
from fabric.api import get
import json

with open('credentials.json') as data_file:
    data = json.load(data_file)

env.hosts = data['host']
env.password = data['password']

with open('config.json') as data_file:
    data = json.load(data_file)

SCRIPT_DIR=data['SCRIPT_DIR']
Hosts={}
class FileSshGet:
        def __init__(self,name):
                self.compute_nodes = compute_nodes
                self.storage_nodes = storage_nodes
                self.switches = switches
@hosts(['monitor'])
def run_on_host():
        env.host_string='monitor'
	#run('export PATH=$PATH:'+SCRIPT_DIR)
	#run('pwd')
        run('python '+SCRIPT_DIR+'NagiosStatus.py')

@hosts(['monitor'])
def getValue():
        env.host_string='monitor'
        st=['compute_nodes','storage_nodes','switches']
        for s in st:
                content=open(SCRIPT_DIR+str(s)+".csv", 'r').readlines()
                Hosts[s]=content
