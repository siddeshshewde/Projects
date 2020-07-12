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



def storing_data_to_database (connection, url_queue, domain_queue):
    
    row_count = 0

    myheaders = {
        'User-Agent': 'AdxTxtCrawler/1.0; +Siddesh Test',
        'Accept'    : 'text/plain',
    }

    for domain in range(0, len(url_queue)):
        print (url_queue[domain])
        
        # if we can't connect, then move on
        try:
            response = requests.get(url_queue[domain], headers=myheaders, allow_redirects=True, timeout=2)
            #encoding = response.encoding
            #print (response.raise_for_status())
            #print (response.status_code)
            #print (response.history)
            #print (response)
            
        except requests.exceptions.RequestException as e:
            # log warnings in db and also count of errors - error_domain_count
            logging.warning(e)
            continue
        
        # Checking for redirects/http errors/content        
        # disallow anything where response history > 3
        if (len(response.history) > 3):
            error_log (connection, domain_name, data_row = None, comment, line_number = None, 'too many redirects.'):
            continue

        # HTML content, skipping
        if (re.search('^([^,]+,){2,3}?[^,]+$', response.text, re.MULTILINE) is None):
            logging.warning("schema inappropriate, skipping")
            continue

        temp_file = 'temp_file.csv'
        with open(temp_file, 'wb') as t:
            t.write(response.text)
            t.close()

        with open(temp_file, 'rU') as t:
            #read the line, split on first comment and keep what is to the left (if any found)
            line_reader = csv.reader(t, delimiter='#', quotechar='|')
            comment = ''

            line_number = 1
            for line in line_reader:
                #print (line)
                try:
                    data_line = line[0]
                except:
                    data_line = ""

                #determine delimiter, conservative = do it per row
                if data_line.find(",") != -1:
                    data_delimiter = ','
                elif data_line.find("\t") != -1:
                    data_delimiter = '\t'
                else:
                    data_delimiter = ' '     
                #print (data_line)
                data_reader = csv.reader([data_line], delimiter=',', quotechar='|')
                #print (data_reader)
                for row in data_reader:
                    if len(row) > 0 and row[0].startswith( '#' ):
                        continue

                    if (len(line) > 1) and (len(line[1]) > 0):
                         comment = line[1]
                    #print (row)
                    row_count = row_count + processing_row_to_database(connection, row, comment, domain_queue[domain], line_number)
                    line_number += 1

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
