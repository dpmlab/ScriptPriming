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

story_lens = pickle.load(open('pickle/story_lens36.pickle', 'rb'))
timing = pickle.load(open('pickle/timing36.pickle', 'rb'))
listen_order = pickle.load(open('pickle/listen_order36.pickle', 'rb'))

def create_sub_encoding_hipp_storydict_ISC(sub):
    # get encoding residuals for this sub
    residuals_dict =  joblib.load('pickle/subs_residuals/encoding_hipp_80/' + sub + '_encoding_hipp_residuals_80.sav')
    
    indiv_storydict = {}

    for this_run in residuals_dict:
        n_stories = listen_order[sub][this_run].shape[0]
        for i in range(n_stories):
            this_count = listen_order[sub][this_run][i,0]
            this_story = int(listen_order[sub][this_run][i,1])
            start_time = timing[sub][this_run][this_count]['ISC_start']
            stop_time = start_time + story_lens[this_story]['ISC']['L'].shape[1]
            indiv_storydict[this_story] = residuals_dict[this_run][:, start_time:stop_time]
            
    return indiv_storydict