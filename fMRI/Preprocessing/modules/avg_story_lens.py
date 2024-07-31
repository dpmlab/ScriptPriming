import numpy as np

def avg_story_lens(story_dict, timing):
    
    story_list = [11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34, 41,42, 43,44]
    
    avg_lens = {}
    
    for story in story_list:
        avg_lens[story] = {}
    
    for story in story_list:
        ISC_ts = np.array([])
        GLM_ts = np.array([])
        for sub in story_dict.keys():
            for run in story_dict[sub].keys():
                for i in range(story_dict[sub][run].shape[0]):
                    this_story = story_dict[sub][run][i][1]
                    if this_story == story:
                        this_count = story_dict[sub][run][i][0]
                        ISC_ts = np.append(ISC_ts, timing[sub][run][this_count]['t_ISC'])
                        GLM_ts = np.append(GLM_ts, timing[sub][run][this_count]['t_GLM'])
                        
        avg_len_ISC = round(np.mean(ISC_ts))
        avg_len_GLM = round(np.mean(GLM_ts))
        avg_lens[story]['ISC'] = {'L':np.zeros((40962, avg_len_ISC, 0)), 'R':np.zeros((40962, avg_len_ISC, 0))}
        avg_lens[story]['GLM'] = {'L':np.zeros((40962, avg_len_GLM, 0)), 'R':np.zeros((40962, avg_len_GLM, 0))}
        
    
    return avg_lens