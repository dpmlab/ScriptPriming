import numpy as np

def storyactionstring_get_array(this_string):
    this_part = this_string.split("[")[1]
    this_part = this_part.split("]")[0]
    this_array = np.fromstring(this_part, dtype=int, sep=' ')
    
    return this_array