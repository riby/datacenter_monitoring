#!/bin/sh
cd v2/
virtualenv -p python2.7 venv
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

FILE="credentials.json"
 
if [ -f "$FILE" ];
then
   echo "File $FILE exist."
else
   echo "File $FILE does not exist"
   touch $FILE
   echo "File created,Enter Data"
fi

FILE="config.json"
 
if [ -f "$FILE" ];
then
   echo "File $FILE exist."
else
   echo "File $FILE does not exist"
   touch $FILE
   echo "File Created,Enter Data"
fi

#python app.py

