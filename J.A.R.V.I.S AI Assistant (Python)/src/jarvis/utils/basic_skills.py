import requests
import os

class BasicSkills:

    def exit_application(self):
        print ('Jarvis is shutting down the system.')
        exit()

    def check_internet_connection(self):
        #Checking Internet Connection
        try:
            print ('Checking Internet Connection...')
            requests.get('https://google.com', timeout=3)
            print ('Internet Connection Passed.')

        except requests.ConnectionError:
            print ('Internet Connection not available.')
            print ('Skills which use internet will not work.')    

    def clear_console(self):
        print ('clear console')    
        if os.name =='posix':
            os.system('clear')
        else:
            os.system('cls')
