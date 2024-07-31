import numpy as np
from modules.storyactionstring_get_array import storyactionstring_get_array

def get_SA_order_priming(file_dict):
    
    story_order = {}
    priming_order = {}
    
    for sub in file_dict.keys():
        this_df = pd.read_csv(file_dict[sub])
        story_1 = storyactionstring_get_array(this_df['story_list_block1'].iloc[0])
        action_1 = storyactionstring_get_array(this_df['action_list_block1'].iloc[0])
        story_2 = storyactionstring_get_array(this_df['story_list_block2'].iloc[0])
        action_2 = storyactionstring_get_array(this_df['action_list_block2'].iloc[0])
                                               
        this_story_order = []
        this_action_order = []
        
        for i in range(story_1.shape[0]):
            this_story_order.append(story_1[i])
            if action_1[i] == 4:
                this_action_order.append(0)
            else:
                this_action_order.append(action_1[i])
            
        for i in range(story_2.shape[0]):
            this_story_order.append(story_2[i])
            if action_2[i] == 4:
                this_action_order.append(0)
            else:
                this_action_order.append(action_2[i])
        
        story_order[sub] = this_story_order
        priming_order[sub] = this_action_order
        
    return story_order, priming_order
                                