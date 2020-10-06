from jarvis.engine.speech_to_text import SpeechToTextEngine
from jarvis.utils.basic_skills import BasicSkills

class Processor:
    
    def __init__(self):
        self.speech = SpeechToTextEngine()
        self.basic_skills   = BasicSkills()

    def run(self):
        print ('Say Something..')
        transcript = self.speech.recognize_voice()
        self.analyze(transcript)

    def analyze(self, transcript):
        
        if 'exit' in transcript.lower() or 'quit' in transcript.lower() or 'bye' in transcript.lower() or 'shutdown' in transcript.lower() or 'goodbye' in transcript.lower():
            self.basic_skills.exit_application()

        if 'check' in transcript.lower() and 'internet' in transcript.lower() and 'connection' in transcript.lower():
            self.basic_skills.check_internet_connection()

        if 'clear' in transcript.lower() and ('console' in transcript.lower() or 'terminal' in transcript.lower()):
            self.basic_skills.clear_console()
