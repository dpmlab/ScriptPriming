import glob
import nibabel as nib
import pandas as pd
import numpy as np
import os
import h5py
from sklearn import linear_model
from scipy.stats import zscore
from scipy import stats
import matplotlib.pyplot as plt
import math
import pickle
import joblib
import sys

from modules.create_sub_encoding_hipp_storydict_ISC import create_sub_encoding_hipp_storydict_ISC

for i in range(1, len(sys.argv)):
    print('Runnning this sub...', sys.argv[i])
    this_storydict = create_sub_encoding_hipp_storydict_ISC(sys.argv[i])
    filename = 'pickle/subs_encoding_hipp_storydict_ISC/' + sys.argv[i] + '_encoding_hipp_storydict_ISC.sav'
    joblib.dump(this_storydict, filename)