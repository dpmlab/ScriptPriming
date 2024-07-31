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
import deepdish as dd
from tqdm import tqdm

from modules.make_BIDS_behav_dict import make_BIDS_behav_dict
from modules.get_listenorder import get_listenorder
from modules.listen_timing import listen_timing
from modules.avg_story_lens import avg_story_lens
from modules.create_residuals import create_residuals
from modules.all_voxels_story_data import all_voxels_story_data
from modules.all_ROIs_story_data import all_ROIs_story_data
from modules.process_Recall_Residuals import process_Recall_Residuals
from modules.do_motion_assessment import do_motion_assessment
from modules.create_residuals_no_mo import create_residuals_no_mo


subs = ['sub-01', 'sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06', 'sub-07', 'sub-08', 'sub-09', 'sub-10',
       'sub-12', 'sub-13','sub-14', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20', 'sub-21', 'sub-22',
        'sub-23', 'sub-24', 'sub-25', 'sub-26', 'sub-27', 'sub-28', 'sub-29', 'sub-30', 'sub-31', 'sub-32', 'sub-33', 
       'sub-34', 'sub-35', 'sub-36', 'sub-37', 'sub-38']

# import SLs
SL_dense = {'L':dd.io.load('SLs/SLlist_dense.lh.h5'),
            'R':dd.io.load('SLs/SLlist_dense.rh.h5')}

print(len(SL_dense['L'].keys()))

n_subs = len(subs)

story_lens = pickle.load(open('pickle/story_lens36.pickle', 'rb'))
timing = pickle.load(open('pickle/timing36.pickle', 'rb'))
listen_order = pickle.load(open('pickle/listen_order36.pickle', 'rb'))

for hem in SL_dense:
    print('processing... hem ', hem)
    for this_SL in tqdm(SL_dense[hem]):
        print('processing... SL ', this_SL)
        story_data = dict()
        nVox = len(SL_dense[hem][this_SL])
        for story in story_lens:
            story_data[story] = np.full((n_subs, nVox, story_lens[story]['ISC']['L'].shape[1]), np.nan)
        
        for sub_i, sub in enumerate(subs):
            filename = 'pickle/subs_encoding_storydict_ISC/' + sub + '_encoding_storydict_ISC.sav'
            this_sub_storydict = joblib.load(filename)
            for this_story in this_sub_storydict.keys():
                story_data[this_story][sub_i,:] = this_sub_storydict[this_story][hem][SL_dense[hem][this_SL]]

        filename = 'pickle/SLs_dense/' + hem + '/' + this_SL +'.sav'
        joblib.dump(story_data, filename)