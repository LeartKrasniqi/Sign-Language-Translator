# ASL Translator
# Andy Jeong, Leart Krasniqi, Kevin Lin, Ali Rahman
# This script runs the code for our senior project
# [Extended Explanation]

import os
import subprocess
import sys
import time
import wave

import PIL.ImageOps
import pyaudio
import speech_recognition as sr
from google.cloud import storage
from PIL import Image

import Adafruit_GPIO as AGPIO
import Adafruit_GPIO.SPI as SPI
import bluetooth
import RPi.GPIO as GPIO
import ST7735 as TFT
from firebase import firebase
from picamera import PiCamera

sys.path.append(os.path.realpath(__file__))
video_recording = False
mic_recording = False
disp = False

#############################
#   Function Definitions    #
#############################

# Runs when video button is pressed
def video_button_callback(channel):
    global video_recording 
    time.sleep(0.3)
    filename = "./videos/newvideo.mjpeg"
    if(not video_recording):
        # uncomment for single snapshot
        # imagePath = './videos/image_capture.jpg'
        # camera.capture(imagePath)
        
        # video
        print("video recording...\n")
        camera.start_recording("./videos/" + filename)
        video_recording = True
    else:
        print("video finished recording...\n")
        camera.stop_recording()
        # Add stuff to send the video and wait for response from app
        sendVideo(filename)
        video_recording = False

def sendVideo(filename):
    os.environment["GOOGLE_APPLICATION_CREDENTIALS"]='./gcp/credentials.json'
    client = storage.Client()
    bucket = client.bucket('precise-airship-267920.appspot.com')

    # generate image blob
    imageBlob = bucket.blob("newVideoBlob")
    imageBlob.upload_from_filename(filename)

# Runs when mic button is pressed
def mic_button_callback(channel):
    global mic_recording
    OUTFILE = "./audio/audio.wav"
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
    speech = sr.AudioFile(outfile)
    
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    words_dict = ["goodbye","hello","no","please","sorry","thanks","yes","you're welcome"]
    try:
        with speech as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.record(source, offset = 0)
            # list of recognized words in list
            recog_words = recognizer.recognize_google(audio).lower().split(",!? ")

            for recognized_word in recog_words:
                # word check
                # check if recognized word matches any word in our dictionary
                if any(recognized_word in wd for wd in words_dict):
                    print("displaying gesture for word: ", recognized_word)
                    
                    # display gesture for that word
                    im = Image.open("./words/" + recognized_word + "jpg")
                    im = im.transpose(Image.FLIP_LEFT_RIGHT).resize((disp_width, disp_height))
                    im = PIL.ImageOps.invert(im)
                    disp.display(im)
                    time.sleep(2)
                    disp.clear()
                # else, move onto fingerspelling mode
                else:
                    print("fingerspelling for: ", recognized_word)
                    for letter in recognized_word:
                        # display image if letter is an alphabet
                        if letter in alphabet: 
                            im = Image.open("./letters/" + letter + ".png")
                            im = im.transpose(Image.FLIP_LEFT_RIGHT).resize((disp_width, disp_height))
                            im = PIL.ImageOps.invert(im)
                            disp.display(im)
                        time.sleep(2)
                        disp.clear()
    except Exception as e:
        print("Exception found! {}: {}".format(type(e), e.message))
        mic_recording = False


# Sends the video and waits for response from app
def sendVideo(f):
    # Do stuff
    gclient = storage.client()
    bucket = gclient.bucket("precise-airship-267920")
    blob = bucket.blob("videos/" + f)
    blob.upload_from_filename(filename = "./videos/" + f)

if __name__=="__main__":
    
    print("Starting run.py...\n")

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
    disp.clear()
    disp.display()
    disp.end()

    ###########################
    #   Camera Button Setup   #
    ###########################
    camera = PiCamera()
    camera.rotation = 180
    video_recording = False
    video_pin = 18
    GPIO.setup(video_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(video_pin, GPIO.FALLING, callback = video_button_callback, bouncetime = 1000)

    ########################
    #   Mic button Setup   #
    ########################
    recognizer = sr.Recognizer()
    mic_recording = False
    mic_pin = 17
    GPIO.setup(mic_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.add_event_detect(mic_pin, GPIO.FALLING, callback = mic_button_callback, bouncetime = 1000)
    
    ############################
    # Bluetooth communications #    
    ############################
    
    server = bluetooth.RFCOMM
    server_sock = bluetooth.BluetoothSocket( server ) 
    port = bluetooth.PORT_ANY
    host = ""
    server_sock.bind( (host,port) ) 
    server_sock.listen(1) 
    uuid = '8d0aa681-5e25-44b4-a5d3-d9d907d81c9d'
    bluetooth.advertise_service(server, "Kevin Link", service_id = uuid, service_classes = \
                    [uuid, bluetooth.SERIAL_PORT_CLASS], profiles = [bluetooth.SERIAL_PORT_PROFILE])
    client_sock,address = server_sock.accept() 

    print("Accepted connection from %s at address %s" % (client_sock, address))
    # continuously receive if not triggered by buttons
    while True: 
        recvdata = client_sock.recv(1024) 
        print("Received data: \"%s\" " % recvdata)
        if (recvdata == "Q"): 
            print ("Exiting") 
            break            
    client_sock.close() 
    server_sock.close()

    ################
    #   Cleanup    #
    ################
    message = input("Press ENTER to quit \n\n") 
    GPIO.cleanup()
