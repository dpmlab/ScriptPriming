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

stories = [11,12,13,14,21,22,23,24,31,32,33,34,41,42,43,44]

#import stories files
directory_stories = '../../story_csv'

filenames_stories = glob.glob(directory_stories + '/*.csv')

dfs_stories = []
    
for filename in filenames_stories:
    dfs_stories.append(pd.read_csv(filename))

# organize in dict   
story_boundaries = dict()

#read in the location and social event values from the story files 
for s in range(16):
    this_story = int(dfs_stories[s]['story'].iloc[0])
    keys2 = dfs_stories[s]['locationEvent'].values
    keys3 = dfs_stories[s]['socialEvent'].values
    story_boundaries[this_story] = keys2[:, np.newaxis]
    story_boundaries[this_story] = np.concatenate((story_boundaries[this_story], keys3[:, np.newaxis]), axis = 1)
    
#mark the changes or boundaries from one event to another with a '1' and delete first two columns
for key in story_boundaries:
    location = story_boundaries[key][:,0]
    social = story_boundaries[key][:,1]
    for i in range(0, len(location)):  
        if location[i] > location[i-1]:
            location[i] = 7
    for i in range(0, len(location)):  
        if location[i] != 7:
            location[i] = 0
    for i in range(0, len(social)):
        if social[i] > social[i - 1]:
            social[i] = 7
    for i in range(0, len(social)):
        if social[i] != 7:
            social[i] = 0
    location[0] = 7
    social[0] = 7
    location2 = location > 1
    social2 = social > 1
    location2 = location2.astype(int)
    social2 = social2.astype(int)
    story_boundaries[key] = np.concatenate((story_boundaries[key], location2[:, np.newaxis]), axis = 1) 
    story_boundaries[key] = np.concatenate((story_boundaries[key], social2[:, np.newaxis]), axis = 1)
    story_boundaries[key] = np.delete(story_boundaries[key] ,np.s_[0:2],axis=1)
    
def det_event_lens(listen_order, story_lens, timing, behav_files):
    
    # structure output dict
    
    output = {}
    
    for story in stories:
        output[story] = {'ISC': {'location': {}, 'social':{}}, 'GLM': {'location': {}, 'social':{}}}

    for story in stories:
        story_len = story_lens[story]['GLM']['L'].shape[1]
        for schema in ['location', 'social']:
            # Get which clips start a new event
            if schema == 'location':
                event_starts = np.where(story_boundaries[story][:,0] == 1)
            else:
                event_starts = np.where(story_boundaries[story][:,1] == 1)
            # make matrix for event start times
            start_times = np.zeros((4,0))
            # iterate through all subjects in listen_order and find instances where the current story is listenened to
            for sub in listen_order.keys():
                for run in listen_order[sub].keys():
                    this_pd = pd.read_csv(behav_files[sub][run])
                    for i in range(listen_order[sub][run].shape[0]):
                        # If the story was listened to by this person in this run...
                        if listen_order[sub][run][i][1] == story:
                            this_count = listen_order[sub][run][i][0]    
                            # find the start times of all the audio clips of that story
                            starts = this_pd['clip_StartTime'].values[this_pd['count']==this_count]
                            starts = starts[~np.isnan(starts)]
                            # Get clip start times of event boundary clips
                            st_event_starts = starts[event_starts]
                            # see how far all events are from the start of the first event
                            this_subtr = st_event_starts[0]
                            grounded_event_starts = st_event_starts - this_subtr
                            # reshape
                            grounded_event_starts = grounded_event_starts.reshape(grounded_event_starts.shape[0], -1)
                            # add the subtracted event starts to start_times
                            start_times = np.hstack((start_times, grounded_event_starts))
            # average the start times across participants
            avg_st = np.mean(start_times, axis = 1)
            # round up for the TR event length
            for i in range(1,4):
                this_start, this_dec = str(avg_st[i]).split('.')
                this_start = int(this_start) + 1
                avg_st[i] = int(this_start)
            # make a vector with all TRs labeled with corresponding event
            all_events = np.zeros((story_len, 1))
            #label 1st event
            all_events[int(avg_st[0]):int(avg_st[1])] = 1
            #label 2nd event
            all_events[int(avg_st[1]):int(avg_st[2])] = 2
            #label 3rd event
            all_events[int(avg_st[2]):int(avg_st[3])] = 3
            #label 4th event
            all_events[int(avg_st[3]):-6] = 4
            
            
            # put in dict
            output[story]['GLM'][schema] = all_events
            output[story]['ISC'][schema] = all_events[:-6]
            
    return output