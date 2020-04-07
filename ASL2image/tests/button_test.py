from picamera import PiCamera
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

def video_button_callback(channel):
    global video_recording
    time.sleep(0.3)
    filename = "v.mjpeg"
    if(not video_recording):
        print("Video recording...\n")
        #camera.start_recording(filename)
        video_recording = True
    else:
        print("done video recording...\n")
        #camera.stop_recording()
        video_recording = False


def mic_button_callback(channel):
    global mic_recording
    OUTFILE = "audio.wav"
    time.sleep(0.3)

    if(not mic_recording):
        print("audio recording...\n")
        # Start arecord process 
        #subprocess.Popen(["arecord", "-D", "plughw:2,0", OUTFILE])
        mic_recording = True
    else:
        print("finished recording audio...\n")
        #subprocess.Popen(["killall", "arecord"])
        mic_recording = False

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
alphabet = "abcdefghijklmnopqrstuvwxyz"
mic_recording = False
mic_pin = 17
GPIO.setup(mic_pin, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.add_event_detect(mic_pin, GPIO.FALLING, callback = mic_button_callback, bouncetime = 1000)

msg = input("Enter to quit")
