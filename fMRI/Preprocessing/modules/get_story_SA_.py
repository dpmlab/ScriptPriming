import numpy as np
import pandas as pd

def get_story_SA_(indiv_SA):
    stories = [11,12,13,14,21,22,23,24,31,32,33,34,41,42,43,44]
    
    story_SA = dict()
    
    for story in stories:
        story_SA[story] = pd.DataFrame(columns=['sub','story','prime','Q1', 'A1', 'Q2','A2','Q3','A3','Q4','A4','Q5','A5','Q6',
                                       'A6','Q7','A7','Q8','A8'])
    
    for sub in indiv_SA:
        for i in range(12):
            this_story = indiv_SA[sub]['story'].iloc[i]
            story_SA[this_story].loc[len(story_SA[this_story].index)] = indiv_SA[sub].iloc[i]
            
    return story_SA
        