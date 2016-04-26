# datacenter_monitoring
A tool to combine data from Nagios, Ganglia and Torque in order to perform Machine learning based analytics.

Project Structure

RestAPIs
Flask based rest APIs which connect to all monitoring solutions on demand.
Single App file: app.py

Rest End Points:

Title
	* URL
	* Method
	* Requried
	* Success Response
	* Data Params
	* Error Response
	* Sample Call


Nagios Data Retrieval:
	* URL 
		129.107.255.31:8080/atlas/nagios/<params>
	* Method = POST
	* Data Params
		compute_nodes
		storage_nodes
		switches
	* Success Response
		200
	* Error Respone
	* Response
		Snapshot of state of all machines
Ganglia Data Retrieval:
	* URL 
		129.107.255.31:8080/atlas/ganglia
	* Method = Get
	* Success Response
		200
	* Error Respone
	* Response
		Snapshot of state of all machines

Torque Data Retrieval:
	* URL 
		129.107.255.31:8080/atlas/torque
	* Method = Get
	* Success Response
		200
	* Error Respone
	* Response
		Snapshot of state of all machines

Error Handling:
We are handling below type of errors in the application:
- Page Not Found : The template displays the correct URS
- Internal Application Error: It logs error in the application in server.log file

Requirement.txt

Backend Application :
app.py - 
