import pandas as pd
import numpy as np
from modules.storyactionstring_get_array import storyactionstring_get_array


def get_listenorder(behav_files):
    # Structure output dict
    story_dict = {}
    
    # Sub level
    for sub in behav_files.keys():
        story_dict[sub] = {}
        
    # Run level
    for sub in behav_files.keys():
        for run in behav_files[sub].keys():
            story_dict[sub][run] = {}
            
    for sub in behav_files.keys():
        for run in behav_files[sub].keys():
            this_pd = pd.read_csv(behav_files[sub][run])
            if run == 'run-1' or run == 'run-3':
                raw_story_list = this_pd['story_list_block1'].iloc[0]
                raw_action_list = this_pd['action_list_block1'].iloc[0]
            else:
                raw_story_list = this_pd['story_list_block2'].iloc[0]
                raw_action_list = this_pd['action_list_block2'].iloc[0]
            story_list = storyactionstring_get_array(raw_story_list)
            action_list = storyactionstring_get_array(raw_action_list)
            # Array to go in story_dict
            # First column is count, second column is story, third column is priming
            count = 0
            n_stories = sum([count + 1 for x in action_list if x != 3])
            this_array = np.zeros((n_stories,3))
            count = 0
            for i in range(len(story_list)):
                if action_list[i] == 3:
                    pass
                else:
                    # determine the count
                    this_array[count][0] = i
                    # determine the story
                    this_array[count][1] = story_list[i]
                    # determine the priming
                    if action_list[i] == 4:
                        this_array[count][2] = 0
                    else:
                        this_array[count][2] = action_list[i]
                    count += 1
            story_dict[sub][run] = this_array
    
    return story_dict