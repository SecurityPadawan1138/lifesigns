# lifesigns
This projects came about because my internet connection keeps cutting out.  The problem is the cable modem status lights are all still showing connected.
The basic concept for this project is you start the Python script, put the ip address or site name you want to watch and let it run.  It pings the address and logs if it connects or not.  I tried a few python modules for pinging a website and getting a response back.  I kept getting various module errors so finally went with a subprocess.popen method which has worked well enough.


11/18/2020:  
I have v0.5 working you have an option to run a simple command line report for a time range or if there's any entries that are not connected.  The script uses sqlite3 file to store the entries and generate the reports.  If the sqllite file does not exist the script should auto create it in the folder the script is running in.


1.  Clone this repo to local:
git clone https://github.com/SecurityPadawan1138/lifesigns.git




Upcoming Releases:
11/27/2020:  Version: 1.0 will have better reporting.  Also I'll try to extract the ping latency with the existing function or get a Python module for pinging to work and extract the latency.

