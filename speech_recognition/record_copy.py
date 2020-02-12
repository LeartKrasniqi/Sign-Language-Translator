import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time
import pyaudio
import wave
import sys
import os
import subprocess
import speech_recognition as sr

recording = False
stream = 0
p = 0
frames = []

def button_callback(channel):
    global recording
    global stream
    global p
    global frames
    
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    DEV_INDEX = 3
    CHUNK = 512
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "rec_test.wav"
    time.sleep(0.3)

    if(not recording):
        print("Started Recording")
        
        # Start arecord process (runs indefinitely until killed)
        subprocess.Popen(["arecord", "-D", "plughw:2,0", "recording_test.wav"])
        '''recognizer = sr.Recognizer()
        mic = sr.Microphone(device_index = 3)
        with mic as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
            #audio = recognizer.record(source, offset=0)
            #type(audio)
            #print(recognizer.recognize_google(audio))'''
            
        recording = True
    else:
        print("Stopped Recording")
        # Kill all arecord processes
        subprocess.Popen(["killall", "arecord"])
        
        # Speech Recognition
        recognizer = sr.Recognizer()
        folder = os.path.dirname(os.path.realpath(__file__))
        speech = sr.Microphone(device_index=DEV_INDEX, sample_rate=RATE, chunk_size=CHUNK)
        
        try:
            with speech as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)

                audio = recognizer.record(source, offset = 0)
                print(recognizer.recognize_google(audio))
        except:
            print("Come again??")
            recording = False
        
        # Reset flag
        recording = False


'''
    if(not recording):
        print("Started recording")
        p = pyaudio.PyAudio()
        frames = []
        stream = p.open(format = FORMAT, channels = CHANNELS, rate = RATE, input_device_index = DEV_INDEX, input = True, frames_per_buffer = CHUNK)
        #for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
        recording = True
    else:
        print("Stopped recording")
        stream.stop_stream()
        stream.close()
        p.terminate()

        # Make wav file
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        recording = False
'''

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.add_event_detect(11,GPIO.FALLING,callback=button_callback,bouncetime=1000) # Setup event on pin 10 rising edge
message = input("Press enter to quit\n\n") # Run until someone presses enter
GPIO.cleanup() # Clean up



