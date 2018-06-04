# -*- coding: utf-8 -*-
import sys
import os
import json
import copy
import glob
import tqdm

import create_NAQdataset as cn
#import funcs
import glove as glv

def return_level(context, question, bounds):
	# level = {0,1,2}

	love = glv.Glove()

	cws = glove.document_normalization(context)
	qws = glove.document_normalization(question)

	cwvecs = []
	for cw in cws:
		cwvec = glove.return_vec(cw)
		if not cwvec == -1:
			cwvecs.append(cwvec)
	maxcos = 0
	coss = []
	for qw in qws:
		qwvec = glove.return_vec(qw)
		if qwvec == -1:
			continue
		for cwvec in cwvecs:
			cos = glove.cossim(qwvec, cwvec)
			maxcos = max(cos, maxcos)
		coss.append(maxcos)
	if len(coss) == 0:
		cosmean = 0
	else:
		cosmean = sum(coss)/len(coss)

	if cosmean < bounds[0]:
		level = 0
	elif cosmean >= bounds[0] and cosmean < bounds[1]:
		level = 1
	elif cosmean >= bounds[1]:
		level = 2
	else:
		level = -1

	return level

def split(NAQs):
	version = NAQs['version']
	data = NAQs['data']

	bar = tqdm.tqdm(total=len(data))
	cosmean_boundaries = [0.5, 0.8]

	levels_data = [[],[],[]]
	for d in data:
		paragraphs = d['paragraphs']
		title = d['title']

		levels_paragraphs = [[],[],[]]
		for pnum, paragraph in enumerate(paragraphs):
			qas = paragraph['qas']
			if pnum < len(paragraphs)-1:
				context = paragraphs[pnum+1]['context']
			else:
				context = paragraphs[0]['context']

			levels_naqs = [[],[],[]]
			for qa in qas:
				id = qa['id']
				NAQ = qa['question']
				l = return_level(context, NAQ, cosmean_boundaries)
				if l < 0:
					print('Assing Level Error.')
					sys.exit()
				levels_naqs[l].append(qa)
			for l in range(3):
				if len(levels_naqs[l]) > 0:
					levels_paragraphs[l].append({'qas':levels_naqs[l], 'context':context})
		for l in range(3):
			if len(levels_paragraphs[l]) > 0:
				levels_data[l].append({'paragraphs':levels_paragraphs[l],'title':title})
		bar.update(1)

	level1 = {'data':levels_data[0], 'version':version}
	level2 = {'data':levels_data[1], 'version':version}
	level3 = {'data':levels_data[2], 'version':version}
	return level1, level2, level3




def main():
	savedir = 'save'
	if not os.path.exists(savedir):
		print('Please crete NAQs first, and then save it to "save" directory.')
		sys.exist()

	datanames = glob.glob(os.path.join(savedir, 'NAQs_*.json'))
	for dataname in datanames:

		NAQs = cn.readdata(dataname)
		level1, level2, level3 = split(NAQs)
		cn.save(level1, savedir, 'level1_'+cn.return_filename(dataname)+'.json')
		cn.save(level2, savedir, 'level2_'+cn.return_filename(dataname)+'.json')
		cn.save(level3, savedir, 'level3_'+cn.return_filename(dataname)+'.json')
	print('Done.')

if __name__ == '__main__':
	main()
