import numpy as np

def all_voxels_story_data(subs, residuals, listen_order, timing, story_lens):
    nSubj = len(subs)
    nVox = 40962 * 2
    story_data = dict()
    for story in story_lens:
        story_data[story] = np.full((nSubj, nVox, story_lens[story]['ISC']['L'].shape[1]), np.nan)

    for count, sub in enumerate(timing):
        print(sub)
        for run in timing[sub]:
            run_data = np.row_stack((residuals[sub]['listen'][run]['L'],residuals[sub]['listen'][run]['R']))
            for i in timing[sub][run]:
                start_time = timing[sub][run][i]['ISC_start']
                story = int(listen_order[sub][run][listen_order[sub][run][:,0]==i,1])
                story_data[story][count,:] = run_data[:,start_time:(start_time+story_lens[story]['ISC']['L'].shape[1])]
    
    return story_data