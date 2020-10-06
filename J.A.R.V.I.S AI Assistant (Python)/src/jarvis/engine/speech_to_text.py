import speech_recognition as sr

class SpeechToTextEngine:
    
    def recognize_voice(self):
        mic = sr.Microphone()
        recognize  = sr.Recognizer()

        with mic as source:
            recognize.adjust_for_ambient_noise(source)
            audio = recognize.listen(source)

        try:
            transcript = recognize.recognize_google(audio)
            print (transcript)
            #logging.info(transcript)
        except sr.RequestError:
            print ('API Error')
        except sr.UnknownValueError:
            print ('Unable to recognize speech')    

        return transcript
