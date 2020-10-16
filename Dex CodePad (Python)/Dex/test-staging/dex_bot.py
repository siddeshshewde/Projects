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
                
                if 'declare' in transcript.lower() or 'variable' in transcript.lower() or 'with value' in transcript.lower():
                    variable = transcript.split('variable', 1)[1]
                    value = transcript.split("value", 1)[0]
                    transcript = '{} = {}'.format(variable, value)

            
                file.write(transcript)
                file.write('\n')

bot()