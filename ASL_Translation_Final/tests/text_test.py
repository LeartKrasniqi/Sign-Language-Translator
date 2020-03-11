from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import textwrap
import PIL.ImageOps

import ST7735 as TFT
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI


WIDTH = 128
HEIGHT = 128#160
SPEED_HZ = 4000000


# Raspberry Pi configuration.
DC = 26
RST = 19
SPI_PORT = 0
SPI_DEVICE = 0


# Create TFT LCD display class.
disp = TFT.ST7735(
    DC,
    rst=RST,
    spi=SPI.SpiDev(
        SPI_PORT,
        SPI_DEVICE,
        max_speed_hz=SPEED_HZ))

# Initialize display.
disp.begin()

image = Image.new('RGB', (WIDTH,HEIGHT))
draw = ImageDraw.Draw(image)
draw.rectangle((0,0,WIDTH,HEIGHT), fill=(255,255,255))
disp.display(image)

BORDER=20
FONTSIZE = 24

#draw.rectangle((BORDER,BORDER,WIDTH-BORDER-1,HEIGHT-BORDER-1), fill=(170,0,136))
font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf', FONTSIZE)
#font = ImageFont.load_default()
text = "Kevin Lin is nice"
para = textwrap.wrap(text,width=10)
im = Image.new('RGB', (WIDTH,HEIGHT), (0,0,0,0))
draw = ImageDraw.Draw(im)
#(font_width,font_height) = font.getsize(text)
#draw.text((WIDTH//4 - font_width//4, HEIGHT//4 - font_height//2), text, font=font, fill=(0,0,0))
current_h, pad = 50, 10
for line in para:
    w,h = draw.textsize(line, font=font)
    draw.text(((WIDTH-w)/2, current_h), line, font=font)
    current_h += h + pad
im = PIL.ImageOps.invert(im)
disp.display(im)
