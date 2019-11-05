from __future__ import print_function, division
import numpy as np
from pathlib2 import Path
from itertools import *
import os
import sys
import pickle

root_dir = Path('/')
home_dir = Path(os.getenv('HOME'))
data_dir = Path('/data')
dev_dir = home_dir / 'dev'

########################################################################################################################

def iter_pickle_load(f):
	
	if isinstance(f, file):
		
		try:
			while True:
				yield pickle.load(f)
		except EOFError:
			pass
	
	else:
		
		with open(str(f), 'rb') as f_:
			for data in iter_pickle_load(f_):
				yield data

########################################################################################################################

def f(s):
	pass

########################################################################################################################
