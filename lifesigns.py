#11/18/2020
#Lifesigns V0.5
#Author:  Andy Arter
import sqlite3
import traceback
import subprocess
import datetime 
import time

def startup_monitoring(): #prompt for the router ip address and the external address you will be pinging
    router_ip_address = input('Router IP Address: ')
    external_site_address = input('External Site Address: ')
    #comment out one of the connection lines
    #connection = sqlite3.connect(':memory:') #use this to create a database only in memory 
    connection = sqlite3.connect('lifesigns.db') #use this to create a sqlite file in the script root directory
    cursor = connection.cursor()

    try:
        create = '''CREATE TABLE SANSTEST (
        'ip_address' text,
        'date_time' text,
        'status' text
         )'''
        cursor.execute(create)
        connection.commit()

    except Exception as e:
        print("error: "+str(e))
    return router_ip_address,external_site_address,cursor,connection



def reporting_v1(): #reporting function using the sqlite file
    connection = sqlite3.connect('lifesigns.db')
    cursor = connection.cursor()
    reporting_choice = input('\n\n\n\nFilter Report \nD: Date\nS: Connection errors\n(D or S):')
    if reporting_choice.upper() == 'D': #Date range filter
        start_year = input('Starting Year: ')
        start_month = input('Starting Month: ')
        start_day = input('Starting Day: ')
        end_year = input('Ending Year: ')
        end_month = input('Ending Month: ')
        end_day = input('Ending Day: ')

        cursor.execute("select ip_address,date_time,status from SANSTEST where date_time between '"+start_year+"-"+start_month+"-"+start_day+"' AND '"+end_year+"-"+end_month+"-"+end_day+"'")
        connection.commit()
        results = cursor.fetchall()
        for entry in results:
            print("Site: "+entry[0]+"\nTime Stamp: "+entry[1]+"\nConnection Status: "+entry[2]+"\n\n\n")

    if reporting_choice.upper() == 'S': #if the user selects connection errors
        cursor.execute("select ip_address,date_time,status from SANSTEST where status != 'connected'") #find all entries where the status is not connected
        connection.commit()
        results = cursor.fetchall()
        for entry in results:
            print("Site: "+entry[0]+"\nTime Stamp: "+entry[1]+"\nConnection Status: "+entry[2]+"\n\n\n")

def ping_status (ip_address): #function to ping an address.
        p = subprocess.Popen(['ping', ip_address], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        status = "connected"
        for line in p.stdout:
            output = line.rstrip().decode('UTF-8')
            print(output)
            if (output.startswith('PING')):
                print('First Line')
            else:
                print('output')
                if (output.endswith('Unreachable')):
                   status = "unreachable"
                   break
                if (output.endswith('find host')):
                   status = 'host not found'
                break
                if (output.endswith('name resolution')):
                    status = 'Temporary Failure in Name Resolution'
                break
                if (output.endswith('request timed out')):
                   status = 'request timed out'
                   break
                else:
                   break
        p.stdout.close() #this fixed the too many open files error
        return status
entries = []

menu_selection = input ('R: Reporting  \nS: Startup Monitoring\n(R or S): ') #prompts the user for if they want to access reporting or monitoring


if menu_selection.upper()=='S':
   router_ip_address, external_site_address, cursor,connection = startup_monitoring() #run startup monitoring to get the ip, site address, cursor, connection
   try:
       while(True):
            #insert two records into the database, one for the router and one for the external site
            cursor.execute("INSERT INTO SANSTEST VALUES " + str((str(router_ip_address),str(datetime.datetime.now()),ping_status(router_ip_address))))
            cursor.execute("INSERT INTO SANSTEST VALUES " + str((str(external_site_address),str(datetime.datetime.now()),ping_status(external_site_address))))
            connection.commit()
            time.sleep(25) #delay the loop for 25 seconds
            
   except Exception as e:
        test2 = e
        print('error:'+str(e))

if menu_selection.upper()=='R':
    reporting_v1() #if the user selects R for reporting open the reporting function
