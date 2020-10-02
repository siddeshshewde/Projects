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
    for i in range (5):
        print ('.', sep=' ', end=' ', flush=True); 
        time.sleep(1)
    time.sleep(2)
    clear = lambda: os.system('cls')
    clear()
    print ('\n' + JARVIS_LOGO)    
    print ('Application started.')
    print ('Jarvis at your service. Please tell me how can I help you')

main()