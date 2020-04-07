import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time
from picamera import PiCamera
import sys

if(len(sys.argv) == 1):
    i = 0
else: 
    if(len(sys.argv) > 2):
        print("Usage: python video.py [number]")
        exit(-1)
    else:
        i = int(sys.argv[1])

camera = PiCamera()
camera.rotation = 180
recording = False

def button_callback(channel):
    global i
    global recording
    time.sleep(0.3)
    if(not recording):
        print("Started recording")
        camera.start_recording('/home/pi/camera/videos/video%s.h264' % i) # Maybe change to .bgr extension
        recording = True
    else:
        print("Stopped recording")
        camera.stop_recording()
        recording = False
    i = i + 1

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 10 to be an input pin and set initial value to be pulled low (off)
GPIO.add_event_detect(10,GPIO.FALLING,callback=button_callback,bouncetime=300) # Setup event on pin 10 rising edge
message = input("Press enter to quit\n\n") # Run until someone presses enter
GPIO.cleanup() # Clean up

