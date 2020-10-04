from subprocess import call
import os

from jarvis.utils.startup import check_internet_connection, start_up

class ConsoleManager:
    def __init__(self):
        self.check_internet_connection = check_internet_connection()
        self.start_up = start_up()


    def console_log(self, text = '', is_startup = 0, clear_console = 0):
        
        if clear_console:
            self.clear_console()

        if is_startup:
            self.start_up()

        if text:
            print (text)

    def clear_console(self):
        print ('clear console')    
        call('clear' if os.name =='posix' else 'cls')