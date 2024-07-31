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
from modules.create_encoding_hipp_residuals_indiv_80 import create_encoding_hipp_residuals_indiv_80
import sys 

fmripreppath = '/data/topdown/fmriprep/fmriprep/'

for i in range(0, len(sys.argv)):
    if i == 0:
        pass
    else:
        print('Running...', sys.argv[i])
        residuals = create_encoding_hipp_residuals_indiv_80(sys.argv[i], fmripreppath)

        # Using Joblib to export residuals
        filename = 'pickle/subs_residuals/encoding_hipp_80/'+sys.argv[i]+ '_encoding_hipp_residuals_80.sav'
        joblib.dump(residuals, filename)