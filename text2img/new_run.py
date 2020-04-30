# Script to translate text into proper images
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from PIL import Image 
import time
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Read in the dictionary file
dict_dir = "../img/"
dict_filename = dict_dir + "dict.txt"
dict_file = open(dict_filename, "r")
dict_lines = dict_file.read().splitlines()


# Quick test to make sure files exist
# for line in dict_lines:
# 	split = line.split()
# 	file = dict_dir + split[1]
# 	try:
# 		open(file, "r")
# 	except:
# 		print("{} DOES NOT EXIST".format(file))


# Create dictionary 
word_dict = dict()
stem_dict = dict()

# Create stemmer
stemmer = PorterStemmer()

# Make map of word and word stem to file
for line in dict_lines:
	split = line.split()
	word = split[0]
	file = dict_dir + split[1]

	if word not in word_dict.keys():
		word_dict[word] = file

	stem = stemmer.stem(word)
	if stem not in stem_dict.keys():
		stem_dict[stem] = file

def show_img(s,t):
	img = mpimg.imread(s)
	plt.imshow(img)
	plt.show(block=False)
	plt.pause(t)
	plt.close()

# Translate the sentences
sentences_file = open("./tests/sentences.txt", "r")
sentences = sentences_file.read().splitlines()
for s in sentences:
	tokens = word_tokenize(s)
	for t in tokens:
		t = t.lower()
		if t in word_dict.keys():
			show_img(word_dict[t],2)
		elif stemmer.stem(t) in stem_dict.keys():
			show_img(stem_dict[stemmer.stem(t)],2)
		else:
			chars = list(t)
			for c in chars:
				path = "../img/letters/{}.png".format(c)
				show_img(path,0.5)
	time.sleep(1)


