from bluetooth import *
import RPi.GPIO as GPIO
import time
from PIL import Image, ImageDraw, ImageFont
import subprocess
import PIL.ImageOps

host = ""
server = BluetoothSocket(RFCOMM)
port = PORT_ANY

try:
    server.bind((host, port))
    print('Binded')
except:
    print('Not binded')

server.listen(1)
uuid = '8d0aa681-5e25-44b4-a5d3-d9d907d81c9d'
advertise_service(server, "Kevin Link", service_id = uuid, service_classes = [uuid, SERIAL_PORT_CLASS], profiles = [SERIAL_PORT_PROFILE])
client, address = server.accept()
print('Connected to', address)
print('Client', client)

try:
    while(True):
        msg2 = "Sent Message!"
        client.send(msg2)
        data = client.recv(1024)
        if data:
            print(data)
            client.send(msg2)
    
except:
    client.close()
    server.close()



client.close()
server.close()

