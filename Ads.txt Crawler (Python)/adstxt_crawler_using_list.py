import sys
import time
import sqlite3
import logging
import re
import datetime

#pip install tld
from tld import get_fld
import tld

#pip install requests
import requests

#install certificates or import ssl as below (https://stackoverflow.com/questions/35569042/ssl-certificate-verify-failed-with-python3)
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

#increasing csv field size limit to 262144
import csv
csv.field_size_limit(256<<10)

def load_url_queue(csv_domain_list, url_queue):
    
    row_count = 0

    with open(csv_domain_list) as csvfile:
        print ('Reading Domains from csv')
        domains = csv.reader(csvfile, delimiter=',', quotechar='|')

        for domain in domains:
            try:
                host = get_fld(domain[0], fix_protocol=True)
            except:
                host = domain[0]

            url_queue.append('http://{host}/ads.txt'.format(host=host))

            row_count += 1    
    print ('Stored URLs and Domains in a variable.')

    return row_count


def storing_data_to_database (connection, url_queue):
    
    global error_domain_count
    row_count = 0

    myheaders = {
        'User-Agent': 'AdxTxtCrawler/1.0; +Siddesh Test',
        #'User-Agent': 'Mediapartners-Google',
        #'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'),
        'Accept'    : 'text/plain',
    }

    print ('Below is the domain list:')

    for url in url_queue:

        print (url)

        try:
            domain = get_fld(url, fix_protocol=True)
        except:
            domain = url

        # if we can't connect, then move on
        try:
            response = requests.get(url, headers=myheaders, allow_redirects=True, timeout=2)
            response.raise_for_status()
            if (response.status_code != 200):
                error_log (connection, domain, 'HTTP Status Error', response.status_code)
                error_domain_count += 1
                continue

        except requests.exceptions.RequestException as e:
            # log warnings in db and also count of errors - error_domain_count
            error_log (connection, domain, str(e), None)
            error_domain_count += 1
            continue

        # Checking for redirects/http errors/content        
        # disallow anything where response history > 3
        if (len(response.history) > 3):
            error_log (connection, domain, "too many redirects", response.status_code)
            error_domain_count += 1
            continue

        # HTML or js content, skipping
        if (re.search('^([^,]+,){2,3}?[^,]+$', response.text, re.MULTILINE) is None):
            #logging.warning("schema inappropriate, skipping")
            error_log (connection, domain, "schema inappropriate, skipping", '200')
            error_domain_count += 1
            continue

        if ('<html' in response.text or '<script' in response.text):
            #logging.warning("html or js content, skipping")
            error_log (connection, domain, "html or js content, skipping", '200')
            error_domain_count += 1
            continue

        with open(target_file, 'wb') as t:
            t.write(response.text.encode())
            t.close()

        with open(target_file, 'r', encoding="utf-8") as t:
            #read the line, split on first comment and keep what is to the left (if any found)
            line_reader = csv.reader(t, delimiter='#', quotechar='|')
            comment = ''

            line_number = 1
            for line in line_reader:
                
                try:
                    data_line = line[0]
                except:
                    data_line = ""

                #if length of line is > 5000 then skip
                if len(data_line) > 5000:
                    continue    

                data_reader = csv.reader([data_line], delimiter=',', quotechar='|')

                for row in data_reader:
                    if len(row) > 0 and row[0].startswith( '#' ):
                        continue

                    if (len(line) > 1) and (len(line[1]) > 0):
                         comment = line[1]

                    row_count = row_count + processing_row_to_database(connection, row, comment, domain, line_number)
                    line_number += 1

    return row_count


def processing_row_to_database(connection, data_row, comment, domain_name, line_number):

    insert_stmt = "INSERT INTO ads_txt (domain_name, advertiser_domain, publisher_id, account_type, cert_authority_id, line_number, raw_string) VALUES (?,?,?,?,?,?,?);"

    domain_name       = domain_name
    advertiser_domain = ''
    publisher_id      = ''
    account_type      = ''
    cert_authority_id = ''
    raw_string        = ','.join(data_row)

    if len(data_row) >= 3:
        advertiser_domain  = data_row[0].lower()
        publisher_id       = data_row[1].lower()
        account_type       = data_row[2].lower()

    if len(data_row) == 4:
        cert_authority_id  = data_row[3].lower()

    #data validation
    data_valid = 1

    # Minimum length of a domain name is 1 character, not including extensions.
    # Domain Name Rules - Nic AG
    # www.nic.ag/rules.htm
    if(len(domain_name) < 3):
        data_valid = 0

    if(len(advertiser_domain) < 3):
        data_valid = 0

    # could be single digit integers
    if(len(publisher_id) < 1):
        data_valid = 0

    # ads.txt supports 'DIRECT' and 'RESELLER'
    if(len(account_type) < 6):
        data_valid = 0

    if(data_valid > 0):
        # Insert a row of data using bind variables (protect against sql injection)
        c = connection.cursor()
        c.execute(insert_stmt, (domain_name.strip(), advertiser_domain.strip(), publisher_id.strip(), account_type.strip(), cert_authority_id.strip(), line_number, raw_string,))

        data = c.fetchall()
        try:
            if not data:
                connection.commit()
        except sqlite3.Error as e:
            print("Database error: %s" % (' '.join(e.args)))
        except Exception as e:
            print("Exception in _query: %s" % e)

        # Save (commit) the changes
        connection.commit()
        return 1

    return 0


def error_log (connection, domain_name, error_message, status_code):
    insert_stmt = "INSERT INTO ads_txt_error_logs (domain_name, error, status_code) VALUES (?,?,?);"
    c = connection.cursor()
    c.execute(insert_stmt, (domain_name, error_message, status_code))

    data = c.fetchall()
    try:
        if not data:
            connection.commit()
    except sqlite3.Error as e:
        print("Database error: %s" % (' '.join(e.args)))
    except Exception as e:
        print("Exception in _query: %s" % e)

    # Save (commit) the changes
    connection.commit()
    pass



### MAIN Function ###

start_time = time.time()

url_queue    = []
csv_domain_list = 'Domain List.csv'
target_file = 'Crawled Domains.csv'
connection = None
total_domain_count = 0
error_domain_count = 0
valid_entry_count = 0
total_time_taken   = 0
average_time_taken = 0


total_domain_count = load_url_queue(csv_domain_list,url_queue)


if total_domain_count > 0:
    connection = sqlite3.connect('ads_txt.db')
    print ('Database Connected')
    
with connection:
    #create_ads_txt_stmt = "create table ads_txt (        row_id integer NOT NULL PRIMARY KEY AUTOINCREMENT, domain_name varchar(100) NOT NULL,        advertiser_domain varchar(100),        publisher_id int(50),        account_type varchar(100),        cert_authority_id varchar(100),        line_number int(10),        is_valid_syntax tinyint(1) DEFAULT 0,        raw_string varchar(200),        creation_date datetime DEFAULT CURRENT_TIMESTAMP,        updation_date datetime DEFAULT CURRENT_TIMESTAMP    );"
    #create_error_log_stmt = "create table ads_txt_error_logs (        row_id integer NOT NULL PRIMARY KEY AUTOINCREMENT, domain_name varchar(100) NOT NULL, error varchar(1000), status_code varchar(100),      creation_date datetime DEFAULT CURRENT_TIMESTAMP,        updation_date datetime DEFAULT CURRENT_TIMESTAMP    );"
    #c = connection.cursor()
    #c.execute(create_stmt)
    #c.execute(create_error_log_stmt)
    print('Table Created')
    valid_entry_count = storing_data_to_database (connection, url_queue)
    if(valid_entry_count > 0): 
        connection.commit()

connection.close()
print ('Database Connection Closed.')       
    
end_time = time.time()

print ('Total Number of Domains: ' + str(total_domain_count))
print ('Number of Proper Domains: ' + str(total_domain_count-error_domain_count))
print ('Number of Error Domains: ' + str(error_domain_count))
print ('Total Number of Entries Added: ' + str(valid_entry_count)) 
print ('Start Time: ' + time.asctime( time.localtime(start_time)))
print ('End Time: ' + time.asctime( time.localtime(end_time)))
print ('Total Time Taken: ' + str(datetime.timedelta(seconds=(end_time-start_time))))
