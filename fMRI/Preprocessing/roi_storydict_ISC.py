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

subs = ['sub-01', 'sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06', 'sub-07', 'sub-08', 'sub-09', 'sub-10', 'sub-11',
       'sub-12', 'sub-13','sub-14', 'sub-15', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20', 'sub-21', 'sub-22',
        'sub-23', 'sub-24', 'sub-25', 'sub-26', 'sub-27', 'sub-28', 'sub-29', 'sub-30', 'sub-31', 'sub-32', 'sub-33', 
       'sub-34', 'sub-35', 'sub-36', 'sub-37', 'sub-38']

# import residuals, listen order, timing, story_lens
residuals = joblib.load('pickle/residuals_30.sav')
story_lens = pickle.load(open('pickle/story_lens.pickle', 'rb'))
timing = pickle.load(open('pickle/timing.pickle', 'rb'))
listen_order = pickle.load(open('pickle/listen_order.pickle', 'rb'))



# Loading ROIs
ROIs = ['Ang', 'Aud', 'mPFC', 'PHC', 'PMC', 'SFG', 'STS']
masks = dict()
for i in range(len(ROIs)):
    with h5py.File('SchemaROIs/' + ROIs[i] + '_verts.h5', "r") as f:
        masks[ROIs[i]] = {'L': list(f['left']), 'R':list(f['right'])}
        
# Organizing Listening residuals by story (organizing all voxels, and all ROIs)
# Get all voxels for each story
#voxel_story_data = all_voxels_story_data(subs, residuals, listen_order, timing, story_lens)
# Get all ROIs for each story 
roi_story_data = all_ROIs_story_data(subs, residuals, listen_order, timing, story_lens)

filename = 'pickle/roi_story_data' + str(len(subs)) + '.sav'
joblib.dump(roi_story_data, filename)