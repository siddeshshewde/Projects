from jarvis.engine.speech_to_text import SpeechToTextEngine
from jarvis.utils.basic_skills import BasicSkills
from jarvis.skills.collection.date_time import DateTime 
from jarvis.skills.collection.speed_test import SpeedTest


SHUTDOWN = "exit quit bye shutdown goodbye"


class Processor:
    
    def __init__(self):
        self.speech = SpeechToTextEngine()
        self.basic_skills = BasicSkills()
        self.date_time = DateTime()
        self.speed_test = SpeedTest()

    def run(self):
        print ('Say Something..')
        transcript = self.speech.recognize_voice()
        self.analyze(transcript)

    def analyze(self, transcript):
        
        if any (keyword in transcript.lower() for keyword in SHUTDOWN.split(' ')):
            self.basic_skills.exit_application()

        if 'check' in transcript.lower() and 'internet' in transcript.lower() and 'connection' in transcript.lower():
            self.basic_skills.check_internet_connection()

        if 'clear' in transcript.lower() and ('console' in transcript.lower() or 'terminal' in transcript.lower()):
            self.basic_skills.clear_console()

        if 'date' in transcript.lower() or 'time' in transcript.lower():
            self.date_time.tell_date()
            self.date_time.tell_time()
            self.date_time.convert_12_hour_format()

        if 'speed' in transcript.lower() and 'test' in transcript.lower() and 'run' in transcript.lower():
            self.speed_test.run_speedtest()