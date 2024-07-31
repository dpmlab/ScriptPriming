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

subs = ['sub-01', 'sub-02', 'sub-03', 'sub-04', 'sub-05', 'sub-06', 'sub-07', 'sub-08', 'sub-09', 'sub-10',
       'sub-12', 'sub-13','sub-14', 'sub-16', 'sub-17', 'sub-18', 'sub-19', 'sub-20', 'sub-21', 'sub-22',
        'sub-23', 'sub-24', 'sub-25', 'sub-26', 'sub-27', 'sub-28', 'sub-29', 'sub-30', 'sub-31', 'sub-32', 'sub-33', 
       'sub-34', 'sub-35', 'sub-36', 'sub-37', 'sub-38']

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
        

# Get story lens
story_lens = avg_story_lens(listen_order, timing)

# Get event lens i.e. determine which event each TR is assigned to 
# ISC event lens do not have 6 seconds added to end
# GLM event lens do have 6 sec HRF added to end
event_lens = det_event_lens(listen_order, story_lens, timing, behav_files)

# Get event bounds i.e. determine which TR to use as the event boundary
# ISC event boundaries do not have HRF added bc the start times are 5 TRs after
# GLM event boundaries have 6 TRs added bc the start time is exactly when the audio starts
ev_bounds = det_ev_bounds(event_lens)

# export stimulus information
filename = 'pickle/story_lens'+ str(len(subs)) + '.pickle'
with open(filename, 'wb') as handle:
    pickle.dump(story_lens, handle)
filename = 'pickle/listen_order'+ str(len(subs)) + '.pickle'
with open(filename, 'wb') as handle:
    pickle.dump(listen_order, handle)
filename = 'pickle/timing'+ str(len(subs)) + '.pickle'
with open(filename, 'wb') as handle:
    pickle.dump(timing, handle)
filename = 'pickle/event_lens'+ str(len(subs)) + '.pickle'
with open(filename, 'wb') as handle:
    pickle.dump(event_lens, handle)
    
filename = 'pickle/ev_bounds'+ str(len(subs)) + '.pickle'
with open(filename, 'wb') as handle:
    pickle.dump(ev_bounds, handle)