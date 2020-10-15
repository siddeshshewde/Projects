import speech_recognition as sr
import os

def bot():
    mic = sr.Microphone()
    recognize = sr.Recognizer()

    if not os.path.exists("test.txt"):
        with open('test.txt', 'w'):
            pass

    with open('test.txt', 'w') as file:

        while True:
            with mic as source:
                print('Say Something...')
                recognize.adjust_for_ambient_noise(source)
                audio = recognize.listen(source)

                try:
                    transcript = recognize.recognize_google(audio)
                    print (transcript)
                except sr.RequestError:
                    print ('API Error')
                    return
                except sr.UnknownValueError:
                    print ('Unable to recognize speech')    
                    return

                if 'exit' in transcript.lower() or 'quit' in transcript.lower():
                    exit()

            
                file.write(transcript)
                file.write('\n')

bot()