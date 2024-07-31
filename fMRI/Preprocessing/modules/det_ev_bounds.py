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

def det_ev_bounds(event_lens):
    # Defining beginning of each event
    HRF_shift = 6
    ev_bounds = {}
    for story in event_lens:
        ev_bounds[story] = {'ISC':{}, 'GLM':{}}
        for script in ['social', 'location']:
            isc_timing = np.where(np.diff(event_lens[story]['GLM'][script].squeeze()))[0] + 1
            glm_timing = np.where(np.diff(event_lens[story]['GLM'][script].squeeze()))[0] + HRF_shift + 1
            ev_bounds[story]['ISC'][script] = np.concatenate(([0],isc_timing))
            ev_bounds[story]['GLM'][script] = np.concatenate(([0],glm_timing))
    return ev_bounds