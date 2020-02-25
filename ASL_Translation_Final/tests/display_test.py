from PIL import Image
import ST7735 as TFT
import Adafruit_GPIO as AGPIO
import Adafruit_GPIO.SPI as SPI
import time 
import sys 
import os 

sys.path.append(os.path.realpath(__file__))

print("Test of display:\n")
print("a->b->c->d->e->f(PAUSE)g->h->i->j->k->l->m->n->o->p(PAUSE)qrs(PAUSE)(PAUSE)t->u->v->w->x->y->z\n")

# Initialize the display
dc = 26
RST = 19
SPI_port = 0 
SPI_dev = 0
speed = 4000000
disp_width = 128
disp_height = 128
disp = TFT.ST7735(dc,rst=RST,spi=SPI.SpiDev(SPI_port,SPI_dev,speed))
disp.begin()


# Display each of the characters
alphabet = "abcdefghijklmnopqrstuvwxyz"
test = "abcdef_ghijklmnop_qrs!_tuvwxyz"

for c in test:
    if c in alphabet:
        im = Image.open("../letters/" + c.upper() + ".png")
        im = im.resize((disp_width, disp_height))
        disp.display(im)
        time.sleep(2)
        disp.display()
    else:
        time.sleep(1)
        disp.display()

disp.display()

