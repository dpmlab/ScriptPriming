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
import joblib
from tqdm import tqdm

# import uniform hippo mask
hippo_mask =  joblib.load('pickle/hippo_mask_uniform.sav')

def create_encoding_hipp_residuals_indiv(sub, fmripreppath):
    
    res_dict = dict()
    
    runs = ['run-1', 'run-2', 'run-3', 'run-4']
    
    for run in runs:
        fname = os.path.join(fmripreppath + sub + '/func/' + \
          sub + '_task-listen_' + run + '_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz')
        if os.path.exists(fname):
            print('run:',run)
            print('      Loading ', fname)
            gi = nib.load(fname)
            D = gi.get_fdata()
            
            # extract hippocampus 
            hippo_D = D[hippo_mask]

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
            regr = linear_model.LinearRegression()
            regr.fit(reg, hippo_D.T)
            hippo_D = hippo_D - np.dot(regr.coef_, reg.T) - regr.intercept_[:, np.newaxis]
            # Note 8% of values on cortical surface are NaNs, and the following will therefore throw an error
            hippo_D = stats.zscore(hippo_D, axis=1)
            res_dict[run] = hippo_D
            
    return res_dict