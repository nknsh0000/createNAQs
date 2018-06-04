import os
import numpy as np
import json
import re
import zipfile

import download as dl

class Glove:
    def __init__(self):
        if not os.path.exists(os.path.join('data', 'glove.6B.100d.json')):
        	dl.download_glove('data')
        	self.glove = self.create_glove_json('data', 'glove.6B.100d.txt', 'glove.6B.100d.json')

        else:
        	with open(os.path.join('data', 'glove.6B.100d.json')) as f:
        		self.glove = json.load(f)

    def create_glove_json(self, datadir, textname, dataname):
        if not os.path.exists(os.path.join(datadir, textname)):
            print('Unzip files.')
        	os.chdir(datadir)
        	with zipfile.ZipFile('glove.6B.zip') as zip:
        		zip.extractall()
        		os.chdir('..')
        	print('Done.')

    	glove_dict = {}
    	with open(os.path.join(datadir, textname)) as f:
    		lines = f.readlines()
    	for line in lines:
    		line = line.split()
    		word = str(line[0])
    		vec = [float(list[i] for i in range(1, len(line)))]
    		glove_dict[word] = vec
    	with open(datadir, dataname) as f:
    		json.dump(glove_dict, f)
    	return glove_dict

    def document_normalization(self, document):
    	with open('data/stopwords.json') as f:
    		stopwords = json.load(f)
    	words = document.split()
    	norm_words = []
    	for i, word in enumerate(words):
    		word = word.lower()
    		word = re.sub('[,.!?;:()''""]','', word)
    		if word not in stopwords:
    			norm_words.append(word)
    	return norm_words

    def return_vec(self, word):
    	try:
    		vec = self.glove[word]
    	except KeyError:
    		vec = -1
    	return vec

    def cossim(self, vec1, vec2):
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
