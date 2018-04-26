# -*- coding: utf-8 -*-
import sys
import os
import json
import copy
import glob
import tqdm

import download as dl

def readdata(datapath):
	with open(datapath) as f:
		squad = json.load(f)
	return squad

def isanswer(answers, context):
	for answer in answers:
		if answer['text'] in context:
			return True
	return False

def return_filename(pathname):
	names = pathname.split('/')[-1]
	name = names.rsplit('.')[0]
	return name

def save(data, savedir, name):
	if not os.path.exists(savedir):
		os.mkdir(savedir)
	with open(os.path.join(savedir, name), 'w') as f:
		json.dump(data, f)
		print('Save {}'.format(os.path.join(savedir, name	))) 

def makeNAQs(squad):
	version = squad['version']
	data = squad['data']
	
	bar = tqdm.tqdm(total=len(data))
	naq_data = []
	for d in data:
		paragraphs = d['paragraphs']
		title = d['title']

		naq_paragraphs = []
		for pnum, paragraph in enumerate(paragraphs):
			qas = paragraph['qas']
			if pnum < len(paragraphs)-1:
				context = paragraphs[pnum+1]['context']
			else:
				context = paragraphs[0]['context']

			naqs = []
			for qa in qas:
				answers = qa['answers']
				id = qa['id']
				question = qa['question']
				if not isanswer(answers, context):
					naq = copy.deepcopy(qa)
					naqs.append(naq)

			if len(naqs) > 0:
				naq_paragraphs.append({'qas':naqs, 'context':context})
		if len(naq_paragraphs) > 0:
			naq_data.append({'paragraphs':naq, 'title':title})
		bar.update(1)

	naqs = {'data':naq_data, 'version':version}
	return naqs



def main():
	if len(sys.argv) == 1: 
		datadir = 'data'
	else:
		datadir = sys.argv[1]
	savedir = 'save'


	datanames = glob.glob(os.path.join(datadir, '*.json'))
	if len(datanames) == 0:
		print('There is no SQuAD dataset in {}'.format(datadir))
		print('Will you download it? [Y/n]')
		res = input()
		if res.lower() == 'y':
			dl.download(datadir)
			datanames = glob.glob(os.path.join(datadir, '*.json'))
		elif res.lower() == 'n':
			print('Quit.')
			exit()
		else:
			print('Please input [Y/n]')

	for dataname in datanames:
		squad = readdata(dataname)
		NAQs = makeNAQs(squad)
		save(NAQs, savedir, 'NAQs_'+return_filename(dataname)+'.json')

	print('Done.')


if __name__ == '__main__':
	main()
