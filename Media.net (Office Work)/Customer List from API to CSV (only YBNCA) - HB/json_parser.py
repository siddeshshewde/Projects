#pip install requests
import requests
import logging
from datetime import datetime
import time
import json
import csv

# Declaring Variables
csv_customer_list         = 'customer_list.csv'
csv_final                 = 'customer_mapping.csv'
customer_list             = []
product_list              = []
request_list              = []
myheaders                 = {
        'User-Agent': 'APICrawler/1.0; +Siddesh Media.net',
        'Accept'    : 'text/plain',
    }

# Time Taken
csv_read_start_time       = 0
csv_read_end_time         = 0
csv_write_start_time      = 0
csv_write_end_time        = 0
api_request_start_time    = 0
api_request_end_time      = 0
api_request_total_time    = 0

# Count
total_error_count         = 0
api_error_count           = 0
ybnca_mapping_error_count = 0

csv_read_start_time = time.time()
with open(csv_customer_list, 'rb') as csvfile:
	
	print ('Reading Customers from csv - customer_list.csv')

	reader = csv.reader(csvfile)
	for row in reader:
		customer_list.append(row[0])
		product_list.append(row[1])
		request_list.append('/adminviewStormLive/rule/{customer_id}/hp/provider?pdt={product_type}'.format(customer_id = row[0], product_type = row[1]))
	print ('Reading of Customers - Done!')
csv_read_end_time = time.time()

csv_write_start_time = time.time()

with open(csv_final, 'w') as csvfinal:
	writer = csv.writer(csvfinal, delimiter=',', lineterminator='\n')

	print ('Writing data into final csv - customer_mapping.csv')

	writer.writerow(['HB Customer ID','Product Type ID','YBNCA Customer ID'])
	
	for i in range(0, len(customer_list)):
		print (i)
		api_request_start_time = time.time()
		try:
			response = requests.get(request_list[i])#, headers=myheaders)

		except requests.exceptions.RequestException as e:
	    	
			logging.warning(e)
			print ('Error Block')
			writer.writerow([customer_list[i], product_list[i], 'API Failure'])
			api_error_count += 1
			continue

		api_request_end_time = time.time()
		api_request_total_time += api_request_end_time - api_request_start_time
		
		a = json.loads(response.text)	

		try:
			writer.writerow([customer_list[i], product_list[i], a['data']['rules']['publisher'][0]['config']['10000']['ext_pub_code']['val']])	
		except:
			writer.writerow([customer_list[i], product_list[i], 'YBNCA Mapping not Present'])
			ybnca_mapping_error_count += 1		

csv_write_end_time = time.time()		
	
print ('Writing of Data - Done!')
print ('Total Records: {num_records}'.format(num_records=len(customer_list)))
print ('Time taken to Read from CSV: {csv_read_time}'.format(csv_read_time= csv_read_end_time-csv_read_start_time))
print ('Time taken to Write to CSV: {csv_write_time}'.format(csv_write_time= csv_write_end_time-csv_write_start_time-api_request_total_time))
print ('Total Time taken for API request: {api_time}'.format(api_time= api_request_total_time))
print ('YBNCA Mapping not present: {ybnca}'.format(ybnca = ybnca_mapping_error_count))
print ('API Errors: {api}'.format(api = api_error_count))
print ('Total Error Count: {total}'.format(total = total_error_count))
