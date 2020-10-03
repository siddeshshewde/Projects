import time
import os
import logging

#pip install requests
import requests

#Using platform instead, don't need finer granularity
#from sys import platform
import platform

#pip install psutil
import psutil

#pip install speech_recognition 
import speech_recognition as sr

JARVIS_LOGO = "\n" \
              "      ██╗ █████╗ ██████╗ ██╗   ██╗██╗███████╗\n" \
              "      ██║██╔══██╗██╔══██╗██║   ██║██║██╔════╝\n" \
              "      ██║███████║██████╔╝██║   ██║██║███████╗\n" \
              " ██   ██║██╔══██║██╔══██╗╚██╗ ██╔╝██║╚════██║\n" \
              " ╚█████╔╝██║  ██║██║  ██║ ╚████╔╝ ██║███████║\n" \
              "  ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝\n"




def main():
    print ('JARVIS is starting.')
    print ('performing initial checks...')
    for i in range (5):
        print ('.', sep=' ', end=' ', flush=True)
        time.sleep(1)

    time.sleep(2)
    #clear = lambda: os.system('cls')
    #clear()
    
    print ('\n' + JARVIS_LOGO)
    print ('Note: CTRL + C If you want to Exit.')

    # Detecting whether linux/windows depending on which we will print system checks. 

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

    #Checking Internet Connection
    try:
        print ('Checking Internet Connection...')
        requests.get('https://google.com', timeout=3)
        print ('Internet Connection Passed.')

    except requests.ConnectionError:
        print ('Internet Connection not available.')
        print ('Skills which use internet will not work.')    

    #engine.say('siddesh')



    print ('Application started.')
    print ('Jarvis at your service. Please tell me how can I help you')

    #while True:
    mic = sr.Microphone()
    recognize  = sr.Recognizer()

    with mic as source:
        recognize.adjust_for_ambient_noise(source)
        audio = recognize.listen(source)

    try:
        transcript = recognize.recognize_google(audio)
        print (transcript)
        logging.info(transcript)
    except sr.RequestError:
        print ('API Error')
    except sr.UnknownValueError:
        print ('Unable to recognize speech')    

    exit()





main()