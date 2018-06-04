# -*- coding:utf-8 -*-
import sys
import os
import urllib.request
import zipfile

def progress( block_count, block_size, total_size ):
    ''' コールバック関数 '''
    percentage = 100.0 * block_count * block_size / total_size
    sys.stdout.write( "%.2f %% ( %d KB )\r"% ( percentage, total_size / 1024 ) )

def download_from_url(url, filetitle):
	print(url)
	print(filetitle)
	urllib.request.urlretrieve(url, '{}'.format(filetitle), reporthook = progress)

def download(datadir):
	trainurl = 'https://rajpurkar.github.io/SQuAD-explorer/dataset/train-v1.1.json'
	devurl = 'https://rajpurkar.github.io/SQuAD-explorer/dataset/dev-v1.1.json'

	if not os.path.exists(datadir):
		os.mkdir(datadir)
	if not os.path.exists(os.path.join(datadir, 'train-v1.1.json')):
		print('Download train dataset.')
		download_from_url(trainurl, os.path.join(datadir, 'train-v1.1.json'))
		print('Save {}'.format(os.path.join(datadir, 'train-v1.1.json')))
	if not os.path.exists(os.path.join(datadir, 'dev-v1.1.json')):
		print('Download dev dataset.')
		download_from_url(devurl, os.path.join(datadir, 'dev-v1.1.json'))
		print('Save {}'.format(os.path.join(datadir, 'dev-v1.1.json')))
	print('Done.')

def download_glove(datadir):
	glove_url = 'http://nlp.stanford.edu/data/wordvecs/glove.6B.zip'

	if not os.path.exists(os.path.join(datadir, 'glove.6B.zip')):
		print('Downloading GloVe...')
		download_from_url(glove_url, os.path.join(datadir, 'glove.6B.zip'))
		print('Done')


if __name__ == '__main__':
	main()
