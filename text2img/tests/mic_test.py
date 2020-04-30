# Script to test speech recording and recognition

import RPi.GPIO as GPIO
import speech_recognition as sr
from PIL import Image
import PIL.ImageOps
import ST7735 as TFT
import Adafruit_GPIO as AGPIO
import Adafruit_GPIO.SPI as SPI
import time, sys, pyaudio, wave, os, subprocess

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

def mic_button_callback(channel):
    global mic_recording
    OUTFILE = "audio.wav"
    time.sleep(0.3)

    if(not mic_recording):
        print("audio recording...\n")
        # Start arecord process 
        subprocess.Popen(["arecord", "-D", "plughw:2,0", OUTFILE])
        mic_recording = True
    else:
        print("finished recording audio...\n")
        subprocess.Popen(["killall", "arecord"])

        # Perform the speech recog
        speechRecognition(OUTFILE)

        mic_recording = False

def speechRecognition(outfile):
    global disp
    disp_width = 128
    disp_height = 128
    speech = sr.AudioFile(outfile)
    try:
        with speech as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.record(source, offset = 0)
            letters = recognizer.recognize_google(audio)
            print(letters)
            #letter = letters.split()

            #  Display image 
            for c in letters:
                if c.lower() in alphabet:
                    im = Image.open("../letters/" + c.upper() + ".png")
                    im = im.resize((disp_width, disp_height))
                    im = PIL.ImageOps.invert(im)
                    disp.display(im)
                    time.sleep(2)
                    disp.display()
    except Exception as e:
        print("Error doing speech recog")
        print(e)
        mic_recording = False

########################
#   Display Setup      #
########################
SPEED_HZ = 4000000
DC = 26
RST = 19
SPI_PORT = 0
SPI_DEVICE = 0
disp = TFT.ST7735(
        DC,
        rst = RST,
        spi = SPI.SpiDev(
                SPI_PORT,
                SPI_DEVICE,
                max_speed_hz = SPEED_HZ))
disp.begin()

########################
#   Mic button Setup   #
########################
recognizer = sr.Recognizer()
alphabet = "abcdefghijklmnopqrstuvwxyz"
mic_recording = False
mic_pin = 17
GPIO.setup(mic_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.add_event_detect(mic_pin, GPIO.FALLING, callback = mic_button_callback, bouncetime = 1000)

msg = input("Enter to quit")
