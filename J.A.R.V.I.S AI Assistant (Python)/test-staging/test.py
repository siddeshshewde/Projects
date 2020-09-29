#pip install SpeechRecognition
import speech_recognition as sr

#pip install pyaudio


# version of speech recognizer
print (sr.__version__)

recognizer = sr.Recognizer()

song = sr.AudioFile('test.wav')

with song as source:
    audio = recognizer.record(source)

print(type(audio))


recognizer.recognize_google(audio)
