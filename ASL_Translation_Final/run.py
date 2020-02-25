# ASL Translator
# Andy Jeong, Leart Krasniqi, Kevin Lin, Ali Rahman
# This script runs the code for our senior project
# [Extended Explanation]

import RPi.GPIO as GPIO
from picamera import PiCamera
import speech_recognition as sr
from PIL import Image
import ST7735 as TFT

import Adafruit_GPIO as AGPIO
import Adafruit_GPIO.SPI as SPI
import time, sys, pyaudio, wave, os, subprocess

sys.path.append(os.path.realpath(__file__))
recording = False
mic_recording = False
disp = False

#############################
#   Function Definitions    #
#############################

# Runs when video button is pressed
def video_button_callback(channel):
    global recording 
    time.sleep(0.3)
    filename = "v.mjpeg"
    if(not recording):
        print("video recording...\n")
        camera.start_recording("./videos/" + filename)
        recording = True
    else:
        print("video finished recording...\n")
        camera.stop_recording()
        # Add stuff to send the video and wait for response from app
        sendVideo(filename)
        recording = False


# Runs when mic button is pressed
def mic_button_callback(channel):
    global mic_recording
    OUTFILE = "audio.wav"
    time.sleep(0.3)

    if(not mic_recording):
        print("audio recording...\n") 
        # Start arecord process (runs indefinitely until killed)
        subprocess.Popen(["arecord", "-D", "plughw:2,0", OUTFILE])
        mic_recording = True
    else:
        print("audio finished recording...\n")
        # Kill all arecord processes
        subprocess.Popen(["killall", "arecord"])

        # Do the speech recognition
        speechRecognition(OUTFILE)

        # Reset the flag
        mic_recording = False


# Uses google_recognizer to do speech detection and then display image
def speechRecognition(outfile):
    global disp
    disp_width = 128
    disp_height = 128
    speech = sr.AudioFile("./audio/" + outfile)
    try:
        with speech as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.record(source, offset = 0)
            letters = recognizer.recognize_google(audio)
            letter = letters.split()

            # Display the correct image
            for c in letters:
                if c in alphabet: 
                    im = Image.open("./letters/" + c.upper() + ".png")
                    im = im.resize((disp_width, disp_height))
                    disp.display(im)
                time.sleep(2)
                disp.clear()
    except:
        # Error occurred, maybe let user know?
        mic_recording = False


# Sends the video and waits for response from app
def sendVideo(f):
    # Do stuff
    gclient = storage.client()
    bucket = gclient.bucket("precise-airship-267920")
    blob = bucket.blob("videos/" + f)
    blob.upload_from_filename(filename = "./videos/" + f)

if __name__=="__main__":

    ###################
    #   Board Setup   #
    ###################
    GPIO.setwarnings(False)

    # Using BCM Pins!!
    GPIO.setmode(GPIO.BCM)

    ######################
    #   Display Setup    #
    ######################
    SPEED_HZ = 4000000

    # BCM PIN NUMBERS!!
    DC = 26
    RST = 19
    SPI_PORT = 0
    SPI_DEVICE = 0
    
    # initialize TFT LCD display class
    disp = TFT.ST7735(
            DC,
            rst = RST,
            spi = SPI.SpiDev(
                    SPI_PORT,
                    SPI_DEVICE,
                    max_speed_hz = SPEED_HZ))

    disp.begin()

    ###########################
    #   Camera Button Setup   #
    ###########################
    camera = PiCamera()
    camera.rotation = 180
    video_recording = False
    video_pin = 10
    GPIO.setup(video_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(video_pin, GPIO.FALLING, callback = video_button_callback, bouncetime = 300)

    ########################
    #   Mic button Setup   #
    ########################
    recognizer = sr.Recognizer()
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    mic_pin = 17
    GPIO.setup(mic_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(mic_pin, GPIO.FALLING, callback = mic_button_callback, bouncetime = 1000)
    









    ################
    #   Cleanup    #
    ################
    message = input("Press ENTER to quit \n\n") 
    GPIO.cleanup()












