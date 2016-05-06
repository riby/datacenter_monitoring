# datacenter_monitoring
A tool to combine data from Nagios, Ganglia and Torque in order to perform Machine learning based analytics.

# MongoDB Data Base required:
Install
https://docs.mongodb.com/manual/tutorial/install-mongodb-on-red-hat/

- Configure the package management system

Create a /etc/yum.repos.d/mongodb-org-3.2.repo file so that you can install MongoDB directly, using yum.

Enter below info:

[mongodb-org-3.2]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/redhat/$releasever/mongodb-org/3.2/x86_64/
gpgcheck=1
enabled=1

- Install latest stabe release
sudo yum install -y mongodb-org

- run mongo service
service mongod start

# Install Python2.7 on system

cd /usr/local/
wget https://www.python.org/ftp/python/2.7.10/Python-2.7.10.tgz
tar xzf Python-2.7.10.tgz
cd Python-2.7.10
./configure --prefix=/usr/local/ --enable-shared
make altinstall

- Set Path 

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib
Use .bashrc to make permanent changes 

- Install setup tools
Install virtual environment for python to run the scripts

curl -o /tmp/ez_setup.py https://bootstrap.pypa.io/ez_setup.py
/usr/local/bin/python2.7 /tmp/ez_setup.py

# Get all the scripts from GITHUM https://github.com/riby/datacenter_monitoring.git
- Create a home directory you want to place code in 

mkdir HOME_DIR
cd HOME_DIR
git clone https://github.com/riby/datacenter_monitoring.git
cd datacenter_monitoring

Follow below steps in base folder

Steps to run:

- Run script.sh file
chmod +x script.sh
./script.sh

- Enter values of credentials and config file created in v2 folder

- Run the virtualenv environment
source v2/venv/bin/activate

- run app.py
python app.py

- Update crontab

Instuction to install other libraries:
scpipy need dependencies

# Handling library errors in installing dependencies:
- Use of Conda
wget https://repo.continuum.io/miniconda/Miniconda2-latest-Linux-x86_64.sh
chmod +x Miniconda2-latest-Linux-x86_64.sh
./Miniconda2-latest-Linux-x86_64.sh

- Install scipy
conda install scipy






