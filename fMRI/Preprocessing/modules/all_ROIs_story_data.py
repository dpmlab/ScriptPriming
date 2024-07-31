import numpy as np
import h5py

# Loading ROIs
ROIs = ['Ang', 'Aud', 'mPFC', 'PHC', 'PMC', 'SFG', 'STS']
masks = dict()
for i in range(len(ROIs)):
    with h5py.File('SchemaROIs/' + ROIs[i] + '_verts.h5', "r") as f:
        masks[ROIs[i]] = {'L': list(f['left']), 'R':list(f['right'])}

def all_ROIs_story_data(subs, residuals, listen_order, timing, story_lens):
    nSubj = len(subs)
    story_data = dict()
    
    for ROI in ROIs:
        print('Processing this ROI...', ROI)
        nVox = len(masks[ROI]['L'])+len(masks[ROI]['R'])
        story_data[ROI] = dict()
        for story in story_lens:
            story_data[ROI][story] = np.full((nSubj, nVox, story_lens[story]['ISC']['L'].shape[1]), np.nan)

        for count, sub in enumerate(timing):
            for run in timing[sub]:
                run_data = np.row_stack((residuals[sub][run]['L'][masks[ROI]['L']],residuals[sub][run]['R'][masks[ROI]['R']]))
                for i in timing[sub][run]:
                    start_time = timing[sub][run][i]['ISC_start']
                    story = int(listen_order[sub][run][listen_order[sub][run][:,0]==i,1])
                    #subj_i = int(sub[-2:])-1
                    story_data[ROI][story][count,:] = run_data[:,start_time:(start_time+story_lens[story]['ISC']['L'].shape[1])]
    
    return story_data