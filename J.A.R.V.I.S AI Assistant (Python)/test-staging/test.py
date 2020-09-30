#pip install SpeechRecognition
import speech_recognition as sr

#pip install pyaudio


# version of speech recognizer
print (sr.__version__)

recognizer = sr.Recognizer()
mic = sr.Microphone()

song = sr.AudioFile('test.wav')

with mic as source:
    print ('with block')
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.listen(source)

try:
    print ('listening..')
    query = recognizer.recognize_google(audio)
    print (query)
except sr.RequestError:
    print('api error')

except sr.UnknownValueError:
    print ('Unable to recognise speech')

print(type(audio))


