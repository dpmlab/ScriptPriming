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

def do_motion_assessment(subs, fmripreppath, residuals, recall_residuals, df):

    #create dict structure
    motion_assessment = {}

    for sub in subs:
        # encoding
        runs = ['run-1', 'run-2', 'run-3', 'run-4']
        t_encoding = 0
        mo_encoding = 0
        for run in runs:
            file_name = os.path.join(fmripreppath + sub + '/func/' + \
                          sub + '_task-listen_' + run + '_desc-confounds_regressors.tsv')
            if os.path.exists(file_name):
                t_encoding += residuals[sub][run]['L'].shape[1]
                # number of motion outliers
                conf = np.genfromtxt(os.path.join(fmripreppath + sub + '/func/' + \
                              sub + '_task-listen_' + run + '_desc-confounds_regressors.tsv'), names=True)

                mo_encoding += np.column_stack([conf[k] for k in conf.dtype.names if ('motion_outlier' in k)]).shape[1] 

        motion_assessment[sub] = {'t_encoding':t_encoding, 'mo_encoding': mo_encoding}

        # recall
        runs = ["1", "2", "3", "4", "5", "6"]
        t_recall= 0
        mo_recall = 0

        for count_run, run in enumerate(runs):
            this_col = 'recall' + run
            text = df.loc[df['participant'] == sub, this_col].iloc[0]
            if isinstance(text, str):
                run_string = 'run-' + str(run)
                t_recall += recall_residuals[sub][run_string]['L'].shape[1]
                conf = np.genfromtxt(os.path.join(fmripreppath + sub + '/func/' + \
                          sub + '_task-recall_run-' + run + '_desc-confounds_regressors.tsv'), names=True)
                mo_recall += np.column_stack([conf[k] for k in conf.dtype.names if ('motion_outlier' in k)]).shape[1] 

        motion_assessment[sub]['t_recall'] = t_recall
        motion_assessment[sub]['mo_recall'] = mo_recall

    print('done! and pickled')
    with open('/data/topdown/scripts/AR/Preprocessing/pickle/motion_assessment.pickle', 'wb') as handle:
        pickle.dump(motion_assessment, handle)
