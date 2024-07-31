import matplotlib.pyplot as plt
import pickle
import numpy as np
import joblib
import h5py
import joblib
from tqdm import tqdm

print('Loading Data...')
story_dict =  joblib.load('Preprocessing/pickle/roi_storydict_ISC_36.sav')
story_dict_hipp = joblib.load('Preprocessing/pickle/hipp_storydict_ISC_36_80.sav')

story_lens = pickle.load(open('Preprocessing/pickle/story_lens36.pickle', 'rb'))
event_lens = pickle.load(open('Preprocessing/pickle/event_lens36.pickle', 'rb'))
ev_bounds = pickle.load(open('Preprocessing/pickle/ev_bounds36.pickle', 'rb'))
listen_order = pickle.load(open('Preprocessing/pickle/listen_order36.pickle', 'rb'))
timing = pickle.load(open('Preprocessing/pickle/timing36.pickle', 'rb'))

# Loading ROIs
ROIs = ['Ang', 'Aud', 'mPFC', 'PHC', 'PMC', 'SFG', 'STS']
masks = dict()
for i in range(len(ROIs)):
    with h5py.File('/data/ListEvents/SchemaROIs/' + ROIs[i] + '_verts.h5', "r") as f:
        masks[ROIs[i]] = {'L': list(f['left']), 'R':list(f['right'])}
        
boolean_masks = dict()
for roi in masks:
    boolean_masks[roi] = {'L':np.zeros((40962), dtype = bool), 'R':np.zeros((40962), dtype = bool)}
    for hem in ['L', 'R']:
        for i in range(0, len(masks[roi][hem])):
            boolean_masks[roi][hem][masks[roi][hem][i]] = 1

nperms = 1001
            
# Plotting
nSubj = story_dict['Ang'][11].shape[0]

# Create 16x16 masks describing the relationships between the 16 stories
story_id = np.array([int(k) for k in ev_bounds.keys()])
same_story = story_id[:,np.newaxis] == story_id[np.newaxis,:]
loc_script = story_id % 10
same_loc = (loc_script[:,np.newaxis] == loc_script[np.newaxis,:])*(np.logical_not(same_story))
social_script = story_id // 10
same_social = (social_script[:,np.newaxis] == social_script[np.newaxis,:])*(np.logical_not(same_story))
other = np.logical_not(same_story + same_loc + same_social)

roi_vals = {}
roi_vals_mismatch = {}
for roi in ['Ang', 'Aud', 'STS', 'SFG', 'mPFC', 'Hipp', 'PHC', 'PMC']:
    print(roi)
    np.random.seed(0)
    if roi == 'Hipp':
        story_data = story_dict_hipp
    else:
        story_data = story_dict[roi]
    nVox = story_data[11].shape[1]
    # Schema pattern ISC
    ISCmat = dict()
    ISCmat['location'] = np.full((nSubj,16,16,4), np.nan)
    ISCmat['social'] = np.full((nSubj,16,16,4), np.nan)

    ISCmat_mismatch = dict()
    ISCmat_mismatch['location'] = np.full((nSubj,16,16,4), np.nan)
    ISCmat_mismatch['social'] = np.full((nSubj,16,16,4), np.nan)
    np.seterr(all='raise')
    print('  Computing ccs')
    for script in ['location', 'social']:
        print('     ',script)
        for loo_i in tqdm(range(nSubj)):
            # Compute all event patterns for all 16 stories
            group_pat = np.zeros((16, nVox, 4))
            loo_pat = np.full((16, nVox, 4), np.nan)
            for story_i, story in enumerate(ev_bounds):
                group_allTRs = np.nanmean(story_data[story][np.arange(nSubj)!=loo_i],0)
                for ev in range(4):
                    TRs = ev_bounds[story]['ISC'][script][ev:(ev+2)]
                    group_pat[story_i,:,ev] = group_allTRs[:,TRs[0]:TRs[1]].mean(1)
                    if not np.any(np.isnan(story_data[story][loo_i,:,:])):
                        loo_pat[story_i,:,ev] = story_data[story][loo_i,:,TRs[0]:TRs[1]].mean(1)

            for story_loo in range(16):
                if np.any(np.isnan(loo_pat[story_loo,:,:])):
                    continue
                for story_group in range(16):
                    # For each story pair, compute normalized correlations for each event
                    # A: the indexing I'm not understanding
                    cc = np.corrcoef(group_pat[story_group].T, loo_pat[story_loo].T)[0:4,4:]
                    for ev in range(4):
                        ISCmat_mismatch[script][loo_i,story_loo,story_group,ev] = cc[np.arange(4)!=ev,ev].mean() + cc[ev,np.arange(4)!=ev].mean()
                        ISCmat[script][loo_i,story_loo,story_group,ev] = cc[ev,ev] - ISCmat_mismatch[script][loo_i,story_loo,story_group,ev]


        ISCmat[script] = np.nanmean(ISCmat[script], 0)
        ISCmat[script] = (ISCmat[script] + np.swapaxes(ISCmat[script],0,1))/2

        ISCmat_mismatch[script] = np.nanmean(ISCmat_mismatch[script], 0)
        ISCmat_mismatch[script] = (ISCmat_mismatch[script] + np.swapaxes(ISCmat_mismatch[script],0,1))/2

    roi_vals[roi] = {'story_location': np.zeros((nperms)),
            'schema_location': np.zeros((nperms)),
            'story_social': np.zeros((nperms)),
            'schema_social': np.zeros((nperms))}
    roi_vals_mismatch[roi] = {'story_location': np.zeros((nperms)),
            'schema_location': np.zeros((nperms)),
            'story_social': np.zeros((nperms)),
            'schema_social': np.zeros((nperms))}

    print('  Running perms')
    #perms here
    for this_perm in tqdm(range(nperms)):
        this_order = np.arange(16)
        if this_perm > 0:
            np.random.shuffle(this_order)
        # reorder story matrices
        reordered = {}
        reordered_mismatch = {}
        for script in ['location', 'social']:
            reordered[script] = ISCmat[script][this_order,:,:]
            reordered[script] = reordered[script][:,this_order,:]

            reordered_mismatch[script] = ISCmat_mismatch[script][this_order,:,:]
            reordered_mismatch[script] = reordered_mismatch[script][:,this_order,:]

        # Use masks to compute summaries for each condition
        ISC_story_locbounds = np.zeros(4)
        ISC_story_socbounds = np.zeros(4)
        ISC_location = np.zeros(4)
        ISC_social = np.zeros(4)
        ISC_other_locbounds = np.zeros(4)
        ISC_other_socbounds = np.zeros(4)
        for ev in range(4):
            ISC_story_locbounds[ev] = reordered['location'][:,:,ev][same_story].mean()
            ISC_story_socbounds[ev] = reordered['social'][:,:,ev][same_story].mean()
            ISC_location[ev] = reordered['location'][:,:,ev][same_loc].mean()
            ISC_social[ev] = reordered['social'][:,:,ev][same_social].mean()
            ISC_other_locbounds[ev] = reordered['location'][:,:,ev][other].mean()
            ISC_other_socbounds[ev] = reordered['social'][:,:,ev][other].mean()

        # Add average ROI vals
        roi_vals[roi]['story_location'][this_perm] = np.mean(ISC_story_locbounds-ISC_location)
        roi_vals[roi]['schema_location'][this_perm] = np.mean(ISC_location-ISC_other_locbounds)
        roi_vals[roi]['story_social'][this_perm] = np.mean(ISC_story_socbounds-ISC_social)
        roi_vals[roi]['schema_social'][this_perm] = np.mean(ISC_social-ISC_other_socbounds)


        ISC_story_locbounds_mismatch = np.zeros(4)
        ISC_story_socbounds_mismatch = np.zeros(4)
        ISC_location_mismatch = np.zeros(4)
        ISC_social_mismatch = np.zeros(4)
        ISC_other_locbounds_mismatch = np.zeros(4)
        ISC_other_socbounds_mismatch = np.zeros(4)
        for ev in range(4):
            ISC_story_locbounds_mismatch[ev] = reordered_mismatch['location'][:,:,ev][same_story].mean()
            ISC_story_socbounds_mismatch[ev] = reordered_mismatch['social'][:,:,ev][same_story].mean()
            ISC_location_mismatch[ev] = reordered_mismatch['location'][:,:,ev][same_loc].mean()
            ISC_social_mismatch[ev] = reordered_mismatch['social'][:,:,ev][same_social].mean()
            ISC_other_locbounds_mismatch[ev] = reordered_mismatch['location'][:,:,ev][other].mean()
            ISC_other_socbounds_mismatch[ev] = reordered_mismatch['social'][:,:,ev][other].mean()

        # Add average ROI vals
        roi_vals_mismatch[roi]['story_location'][this_perm] = np.mean(ISC_story_locbounds_mismatch-ISC_location_mismatch)
        roi_vals_mismatch[roi]['schema_location'][this_perm] = np.mean(ISC_location_mismatch-ISC_other_locbounds_mismatch)
        roi_vals_mismatch[roi]['story_social'][this_perm] = np.mean(ISC_story_socbounds_mismatch-ISC_social_mismatch)
        roi_vals_mismatch[roi]['schema_social'][this_perm] = np.mean(ISC_social_mismatch-ISC_other_socbounds_mismatch)


# Export roi_vals
filename = 'StoryComparison_roi_vals_perms'
with open(filename, 'wb') as handle:
    pickle.dump(roi_vals, handle)

filename = 'StoryComparison_roi_vals_mismatch_perms'
with open(filename, 'wb') as handle:
    pickle.dump(roi_vals_mismatch, handle)
