import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time
import pyaudio
import wave
import sys
import os
import subprocess
import speech_recognition as sr

sys.path.append(os.path.realpath(__file__))
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
import PIL.ImageOps

# setup the Pi pin configuration
RST = 24
SPI_PORT = 0
SPI_DEVICE = 0

# 128x64 display with hardware I2C
# clear display 
disp = Adafuit_SSD1306_128_64(rst=RST)
disp.begin()
disp.clear()
disp.display()

# initialize recognizer
recognizer = sr.Recognizer()
folder = os.path.dirname(os.path.realpath(__file__))


recording = False
stream = 0
p = 0
frames = []

letters = "abcdefghijklmnopqrstuvwxyz"

def button_callback(channel):
    global recording
    global stream
    global p
    global frames
    #global audio
    #global recognizer

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
        recording = True
    else:
        print("Stopped Recording")
        # Kill all arecord processes
        subprocess.Popen(["killall", "arecord"])
        
        # Speech Recognition
        #print(recognizer.recognize_google(audio))       
        folder = os.path.dirname(os.path.realpath(__file__))
        speech = sr.AudioFile(folder + "/recording_test.wav")
        try:
            with speech as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.record(source, offset = 0)
                letters = recognizer.recognize_google(audio).split()
                print("Translating...\n")
                # display the corresponding image
                for letter in letters:
                    print("Displaying image for "+letter+"\n")
                    if c in letter:
                        im = Image.open('./'+c.upper()+'.jpeg').resize((disp.width, disp.height), Image.ANTIALIAS)
                        im = PIL.ImageOps.invert(im).convert('1')
                        disp.image(im)
                        disp.display()
                        time.sleep(2) # 2 second pause
                        disp.clear()
                    else:
                        disp.clear()
                disp.display()
                print("Completed translation")
                
                
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



