import pandas as pd
import numpy as np
from scipy.stats import zscore

# Using a behavioral file to determine the onset and offset of each story listened

def listen_timing(csv_behav_file):
    ## Reading CSV file
    this_behav_file = pd.read_csv(csv_behav_file)
                             
    ## Creating dictionary of story start, stop times, clean start, clean end, fmri start, and T
    # Dictionary to fill audio starts and stops with
    audio_timing = {}
    play_lengths = {}
    # Iterating through behavioral csv for clip audio start and end times
    for i in range(0,8):
        # Getting the clip start and stop times
        starts = this_behav_file['clip_StartTime'].values[this_behav_file['count']==i]
        stops = this_behav_file['clip_EndTime'].values[this_behav_file['count']==i]
        # Removing the nan values
        starts = starts[~np.isnan(starts)]
        stops = stops[~np.isnan(stops)]
        # Putting the first start time and the last stop time in the dictionary
        if len(starts) > 0:
                play_lengths[i] = stops-starts
                # Splitting the start time at the decimal
                this_start, start_dec = str(starts[0]).split('.')
                this_start = int(this_start) + 1
                this_stop, stop_dec = str(stops[-1]).split('.')
                this_stop = int(this_stop)
                # ISC timing, removing 5 seconds from start and adding 5 seconds to the end
                # Start: ignoring first 5 TRs
                ISC_start = this_start + 5
                # End: adding 5 seconds to the end due to the hrf
                ISC_stop = this_stop + 5
                # Length of the clip
                t_ISC = ISC_stop - ISC_start
                # GLM timing, adding 6 seconds to the end
                # End: adding 6 seconds to the end due to the hrf
                GLM_stop = this_stop + 6
                # Length of the clip
                t_GLM = GLM_stop - this_start
                # Putting variables in the dictionary
                this_story = dict(raw_start = starts[0], raw_stop = stops[-1], ISC_start = ISC_start, ISC_stop = ISC_stop, t_ISC = t_ISC, GLM_start = this_start, GLM_stop = GLM_stop, t_GLM = t_GLM)
                audio_timing[i] = this_story
      
    return audio_timing