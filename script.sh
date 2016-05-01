#!/bin/sh
cd v2/
virtualenv -p /usr/bin/python2.6 venv
source venv/bin/activate
#pip install -r requirement.txt
#pip -V
## Set credentials
## set Path
#!/bin/bash

filename="requirement.txt"
while read -r line
do
    name="$line"
    echo $(pip install $name)
done < "$filename"
python app.py
