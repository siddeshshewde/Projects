import sys
import time
import csv
import sqlite3
import logging
from optparse import OptionParser
#pip install requests
import requests
import re
from datetime import datetime

try:
    from urllib.parse import urlparse
except ImportError:
     from urlparse import urlparse

from tld import get_fld



def load_url_queue(csv_domain_list, url_queue, domain_queue):
    
    row_count = 0

    with open(csv_domain_list, 'rb') as csvfile:
        print ('Reading Domains from csv')
        domains = csv.reader(csvfile, delimiter=',', quotechar='|')
        
        for domain in domains:
            
            try:
                host = get_fld(domain[0])
            except:
                host = domain[0]
            domain_queue[row_count] = host
            url_queue[row_count] = 'http://{host}/ads.txt'.format(host=host)
            row_count += 1    
    print ('Stored URLs and Domains in a variable.')
    #print ("domain queue")
    #for i in range (0, row_count):
    #        print (domain_queue[i])    

    return row_count



### MAIN Function ###

start_time = time.time()

host = 'google.com'
url = 'https://forbes.com/ads.txt'


logging.warning("Siddesh")

domain_queue = {}
url_queue    = {}
csv_domain_list = 'domain_list.csv'
connection = None
total_domain_count = 0
valid_domain_count = 0
error_domain_count = 0
total_time_taken   = 0
average_time_taken = 0



total_domain_count = load_url_queue(csv_domain_list,url_queue ,domain_queue)


if total_domain_count > 0:
    connection = sqlite3.connect('testdb.db')
    print ('Database Connected')
with connection:
    valid_domain_count = storing_data_to_database (connection, url_queue, domain_queue)
    if(valid_domain_count > 0):
        connection.commit()

connection.close()
print ('Database Connection Closed.')       
    

end_time = time.time()

print ('Total Number of Domains: ' + str(total_domain_count))
print ('Total Number of Entries Added: ' + str(valid_domain_count)) 
print ('Start Time: ' + time.asctime( time.localtime(start_time)))
print ('End TIme: ' + time.asctime( time.localtime(end_time)))
print ('Total Time Taken: ' + str(end_time-start_time))