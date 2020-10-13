import requests
import json
import csv
import logging



# Declaring Variables
csv_customer_list         = 'Customer List.csv'
csv_final                 = 'Final Customer Mapping.csv'
customer_list             = []
product_list              = []
request_list              = []
myheaders                 = {
        'User-Agent': 'APICrawler/1.0; +Siddesh Media.net',
        'Accept'    : 'text/plain',
    }


with open(csv_customer_list, 'rt') as csvfile:

    print ('Reading Customers from csv - customer_list.csv')
    reader = csv.reader(csvfile)

    for row in reader:
        customer_list.append(row[0])
        product_list.append(row[1])
        request_list.append('/adminviewStormLive/rule/{customer_id}/publisher/provider?pdt={product_type}'.format(customer_id = row[0], product_type = row[1]))
    print ('Reading of Customers - Done!')


with open(csv_final, 'w') as csvfinal:
    
    writer = csv.writer(csvfinal, delimiter=',', lineterminator='\n')
    
    print ('Writing data into final csv - customer_mapping.csv')

    writer.writerow(['HB Customer ID','Product Type ID', 'Provider ID','External Publisher Code'])
    
    for i in range(0, len(customer_list)):
        try:
            print (i)
            response = requests.get(request_list[i])

        except requests.exceptions.RequestException as e:
            logging.warning(e)
            print ('Error Block')
            continue

        a = json.loads(response.text)
        providers = a['data']['prvList'].keys()

        for p in providers:
            try:
                writer.writerow([customer_list[i], product_list[i], p, a['data']['rules']['publisher'][0]['config'][p]['ext_pub_code']['val']])	
            except:
                writer.writerow([customer_list[i], product_list[i], p, 'Provider Mapping not Present'])
                continue
			    