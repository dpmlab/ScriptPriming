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
from modules.det_event_lens import det_event_lens
from modules.det_ev_bounds import det_ev_bounds


subs = ['sub-11', 'sub-15']
behav_files = make_BIDS_behav_dict(subs)

# create listen_order (dictionary with story count, story, and priming for each participant and run)
listen_order = get_listenorder(behav_files)

# create timing with the story onsets and offsets for GLM timing [+0 to start, +6 to end] and Hasson-type Analysis [+5 to start, +5 to end] timing
timing = {}
for sub in behav_files:
    for run in behav_files[sub]:
        if run == 'run-1':
            this_timing = listen_timing(behav_files[sub][run])
            timing[sub] = {run: this_timing}
        else:
            this_timing = listen_timing(behav_files[sub][run])
            timing[sub][run] = this_timing
        



# export stimulus information

filename = 'pickle/listen_order'+ str(len(subs)) + '.pickle'
with open(filename, 'wb') as handle:
    pickle.dump(listen_order, handle)
filename = 'pickle/timing'+ str(len(subs)) + '.pickle'
with open(filename, 'wb') as handle:
    pickle.dump(timing, handle)