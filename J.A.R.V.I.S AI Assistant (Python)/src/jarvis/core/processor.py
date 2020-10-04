from jarvis.engine.speech_to_text import SpeechToTextEngine

class Processor:
    
    def __init__(self):
        self.speech = SpeechToTextEngine()

    def run(self):
        print ('Say Something..')
        transcript = self.speech.recognize_voice()

    def analyze(self):
        if 'exit' in lower.transcript:
            
