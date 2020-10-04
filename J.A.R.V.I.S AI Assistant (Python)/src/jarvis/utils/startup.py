#pip install psutil
import psutil

#Using platform instead, don't need finer granularity
#from sys import platform
import platform

#pip install requests
import requests

from jarvis.core.console import ConsoleManager
import time

JARVIS_LOGO = "\n" \
              "      ██╗ █████╗ ██████╗ ██╗   ██╗██╗███████╗\n" \
              "      ██║██╔══██╗██╔══██╗██║   ██║██║██╔════╝\n" \
              "      ██║███████║██████╔╝██║   ██║██║███████╗\n" \
              " ██   ██║██╔══██║██╔══██╗╚██╗ ██╔╝██║╚════██║\n" \
              " ╚█████╔╝██║  ██║██║  ██║ ╚████╔╝ ██║███████║\n" \
              "  ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝\n"

ASSISTANT_NAME = 'Jarvis'

def __init__(self):
    console_manager = ConsoleManager()

def check_internet_connection():
    #Checking Internet Connection
    try:
        print ('Checking Internet Connection...')
        requests.get('https://google.com', timeout=3)
        print ('Internet Connection Passed.')

    except requests.ConnectionError:
        print ('Internet Connection not available.')
        print ('Skills which use internet will not work.')    

def start_up(self):
    print ('JARVIS is starting.')
    print ('performing initial checks...')
    self.check_internet_connection()
    for i in range (5):
        print ('.', sep=' ', end=' ', flush=True)
        time.sleep(1)

    time.sleep(1.5)
    
    self.clear_console()
    
    print ('\n' + JARVIS_LOGO)
    print ('Note: CTRL + C If you want to Exit.')

    print ('------------System Information------------')
    #CPU
    print ('Operation System: ' + platform.system() + ' ' + platform.release())
    print ('Processor: ' + platform.processor())
    print ('Architecture: ' + platform.machine())
    print ('CPU Count: ' + str(psutil.cpu_count()))
    #Memory 
    # (https://github.com/giampaolo/psutil/blob/master/scripts/disk_usage.py)
    # https://github.com/giampaolo/psutil/blob/1626bae30349627e4d0a25ac9fb4cf3a743b94e7/psutil/_common.py#L730
    print ('Total Memory: ' + str(psutil.virtual_memory().total/1000000) + ' GB')
    print ('Available Memory: ' + str(psutil.virtual_memory().available/1000000) + ' GB')
    print ('Available Percent: ' + str(psutil.virtual_memory().percent) + ' %')
    #print (psutil.virtual_memory())
    #Disk
    #print (psutil.disk_usage('/'))
    #print (psutil.disk_io_counters())
    #print (psutil.disk_io_counters(perdisk=True))
    #Network
    #print (psutil.net_io_counters())
    #print (psutil.net_io_counters(pernic=True))
    #Sensors
    #print (psutil.sensors_temperatures())
    #print (psutil.sensors_fans())
    print (psutil.sensors_battery())
    time.sleep(2)

    print ('Application started.')
    print ('Jarvis at your service. Please tell me how can I help you')