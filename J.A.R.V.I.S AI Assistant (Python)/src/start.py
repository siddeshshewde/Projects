import logging

#pip install requests
import requests

def main():
    

    #Checking Internet Connection
    try:
        print ('Checking Internet Connection...')
        requests.get('https://google.com', timeout=3)
        print ('Internet Connection Passed.')

    except requests.ConnectionError:
        print ('Internet Connection not available.')
        print ('Skills which use internet will not work.')    

    print ('Application started.')
    print ('Jarvis at your service. Please tell me how can I help you')

    #while True:

    exit()





main()