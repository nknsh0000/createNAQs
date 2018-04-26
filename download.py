# -*- coding:utf-8 -*-
import os
import urllib.request

def download_from_url(url, filetitle):
	urllib.request.urlretrieve(url, '{}'.format(filetitle))

def download(datadir):
	trainurl = 'https://rajpurkar.github.io/SQuAD-explorer/dataset/train-v1.1.json'
	devurl = 'https://rajpurkar.github.io/SQuAD-explorer/dataset/dev-v1.1.json'

	if not os.path.exists(datadir):
		os.mkdir(datadir)
	if not os.path.exists(os.path.join(datadir, trainurl)):
		print('Download train dataset.')
		download_from_url(trainurl, os.path.join(datadir, 'train-v1.1.json'))
		print('Save {}'.format(os.path.join(datadir, 'train-v1.1.json')))
	if not os.path.exists(os.path.join(datadir, devurl)):
		print('Download dev dataset.')
		download_from_url(devurl, os.path.join(datadir, 'dev-v1.1.json'))
		print('Save {}'.format(os.path.join(datadir, 'dev-v1.1.json')))
	print('Done.')


if __name__ == '__main__':
	main()
