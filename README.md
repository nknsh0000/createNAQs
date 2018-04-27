# create NAQ from SQuAD 

### Packeges used:
- tqdm 

### If you don't have SQuAD dataset
```
python download.py
```
then it makes data directory and download it.

### create NAQs dataset
If SQuAD dataset is somewhere in your own directory
```
python create_NAQdataset.py [dataset directory path]
```

or if You executed download.py, then
```
python create_NAQdataset.py
```
The created files will be saved in save directory.
