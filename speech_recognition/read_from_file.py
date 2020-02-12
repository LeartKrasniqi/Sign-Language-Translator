import speech_recognition as sr
import os

recognizer = sr.Recognizer()
folder = os.path.dirname(os.path.realpath(__file__))
harvard = sr.AudioFile(folder + '/recording_test.wav')#'/test.wav')
microphone = sr.Microphone()
print(sr.Microphone.list_microphone_names())
mic = sr.Microphone(device_index=0)

with harvard as source:
    recognizer.adjust_for_ambient_noise(source)
    audio = recognizer.record(source, offset=0)
    type(audio)
    print(recognizer.recognize_google(audio))
    

