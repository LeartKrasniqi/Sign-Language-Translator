
#import bluetooth
from bluetooth import *
import RPi.GPIO as GPIO
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image, ImageDraw, ImageFont
import subprocess
import PIL.ImageOps

RST = None
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
disp.begin()
disp.clear()
disp.display()

width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)
draw.rectangle((0,0,width,height), outline=0, fill=0)

padding = -2
top = padding
bottom = height-padding

x = 0
font = ImageFont.load_default()

host = ""
server = BluetoothSocket(RFCOMM)
port = PORT_ANY
img_ext = '.png'

try:
    server.bind((host, port))
    print('Binded')
except:
    print('Not binded')

server.listen(1)
uuid = '8d0aa681-5e25-44b4-a5d3-d9d907d81c9d'
#uuid = '94f39d29-7d6d-437d-973b-fba39e49d4ee'
advertise_service(server, "Kevin Link", service_id = uuid, service_classes = [uuid, SERIAL_PORT_CLASS], profiles = [SERIAL_PORT_PROFILE])
client, address = server.accept()
print('Connected to', address)
print('Client', client)

try:
    f = open('A.png', 'rb')
    l = f.read(1024)
    while(l):
        client.send(l)
        l = l.read(1024)
    f.close()
    print(client.rcv(1024))
    
except:
    client.close()
    server.close()

'''
try: 
    while True:
        data = client.recv(1024)
        print(data)
        display_text = str(data)
        display_text = display_text[2:-1]
        #display_text = 'test'
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        for i in range(len(display_text)):
            if display_text[i].isalpha():
                filename = display_text[i].upper() + img_ext
                image = Image.open(filename).resize((disp.width, disp.height), Image.ANTIALIAS)
                image = PIL.ImageOps.invert(image).convert('1')
                disp.image(image)
                disp.display()
                time.sleep(1)
                disp.clear()
                disp.display()
                time.sleep(0.1)
        disp.clear()
	#draw.text((x,top), display_text[2:-1], font=font, fill=255)
        #disp.image(image)
        #disp.display()
        #time.sleep(0.1)
        send_data = 'Received'
        client.send(send_data)
except:
    client.close()
    server.close()
'''
