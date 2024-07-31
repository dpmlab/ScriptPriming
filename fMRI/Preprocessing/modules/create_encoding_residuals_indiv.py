import glob
import nibabel as nib
import pandas as pd
import numpy as np
import os
from sklearn import linear_model
from scipy.stats import zscore
from scipy import stats
import matplotlib.pyplot as plt
import math
import pickle
from tqdm import tqdm

def create_encoding_residuals_indiv(sub, fmripreppath):
    
    res_dict = dict()
    
    runs = ['run-1', 'run-2', 'run-3', 'run-4']
    
    for run in runs:
        fname = os.path.join(fmripreppath + sub + '/func/' + \
          sub + '_task-listen_' + run + '_space-fsaverage6_hemi-R.func.gii')
        if os.path.exists(fname):
            print('run:',run)
            D = dict()
            for hem in ['L', 'R']:
                fname = os.path.join(fmripreppath + sub + '/func/' + \
                sub + '_task-listen_' + run + '_space-fsaverage6_hemi-' + hem + '.func.gii')
                print('      Loading ', fname)
                gi = nib.load(fname)
                D[hem] = np.column_stack([gi.darrays[t].data for t in range(len(gi.darrays))])

            # Use regressors for:
            # -CSF
            # -WhiteMatter
            # -FramewiseDisplacement
            # -All cosine bases for drift (0.008 Hz = 125s)
            # -X, Y, Z and derivatives
            # -RotX, RotY, RotZ and derivatives
            # Motion Outliers

            conf = np.genfromtxt(os.path.join(fmripreppath + sub + '/func/' + \
                      sub + '_task-listen_' + run + '_desc-confounds_regressors.tsv'), names=True)

            reg = np.column_stack((conf['trans_x'],
                  conf['trans_x_derivative1'],
                  conf['trans_y'],
                  conf['trans_y_derivative1'],
                  conf['trans_z'],
                  conf['trans_z_derivative1'],
                  conf['rot_x'],
                  conf['rot_x_derivative1'],
                  conf['rot_y'],
                  conf['rot_y_derivative1'],
                  conf['rot_z'],
                  conf['rot_z_derivative1'],
                  conf['csf'],
                  conf['white_matter'],
                  conf['framewise_displacement'],
                  np.column_stack([conf[k] for k in conf.dtype.names if ('cosine' in k) or ('motion_outlier' in k)])))

            reg = np.nan_to_num(reg)

            print('    cleaning and zscoring')
            for hem in ['L', 'R']:
                regr = linear_model.LinearRegression()
                regr.fit(reg, D[hem].T)
                D[hem] = D[hem] - np.dot(regr.coef_, reg.T) - regr.intercept_[:, np.newaxis]
                # Note 8% of values on cortical surface are NaNs, and the following will therefore throw an error
                D[hem] = stats.zscore(D[hem], axis=1)
            res_dict[run] = D
            
    return res_dict