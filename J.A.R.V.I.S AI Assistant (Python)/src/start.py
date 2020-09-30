import time
import os

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
    for i in range (3):
        print ('.', sep=' ', end=' ', flush=True); 
        time.sleep(0.5)
    # Clear Screen
    print ('\n' + JARVIS_LOGO)    
    print ('Application started.')
    print ('Jarvis at your service. Please tell me how can I help you')

main()