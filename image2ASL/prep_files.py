import PIL
import os
import cv2
from pathlib import Path

rootdir = './Data/asl_alphabet_train/asl_alphabet_train'
train_file = './Data/train1.txt'
test_file = './Data/test.txt'
f = open(train_file, "a")

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        classtype = file[0]
        if (classtype != 'd' and classtype != 'n' and classtype != 's'):
            filepath = subdir + os.sep + file
            row = filepath + ', ' + classtype + '\n'
            f.write(row)
