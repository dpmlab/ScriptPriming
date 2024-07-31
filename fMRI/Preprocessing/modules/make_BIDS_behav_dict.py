import numpy as np

def make_BIDS_behav_dict(list_bids):
    print(list_bids)
    original_dict = { 
        'sub-01': {'run-1': 'Logs/021020/021020_bk1_listening_fmri.csv', 'run-2':'Logs/021020/021020_bk2_listening_fmri.csv'},
        'sub-02': {'run-1': 'Logs/022420/022420_bk1_listening_fmri.csv', 'run-2':'Logs/022420/022420_bk2_listening_fmri.csv'},
        'sub-03': {'run-1': 'Logs/101520/101520_bk1_listening_fmri.csv', 'run-2':'Logs/101520/101520_bk2_listening_fmri.csv'},
        'sub-04': {'run-1': 'Logs/112020/112020_bk1_listening_fmri.csv', 'run-2':'Logs/112020/112020_bk2_listening_fmri.csv'},
        'sub-05': {'run-1': 'Logs/011721/011721_bk1_listening_fmri.csv', 'run-2':'Logs/011721/011721_bk2_listening_fmri.csv'},
        'sub-06': {'run-1': 'Logs/013021/013021_bk1_listening_fmri.csv', 'run-2':'Logs/013021/013021_bk2_listening_fmri.csv'},
        'sub-07': {'run-1': 'Logs/022021/022021_bk1_listening_fmri.csv', 'run-2':'Logs/022021/022021_bk2_listening_fmri.csv'},
        'sub-08': {'run-1': 'Logs/031321/031321_bk1_listening_fmri.csv', 'run-2':'Logs/031321/031321_bk2_listening_fmri.csv'},
        'sub-09': {'run-1': 'Logs/041421/041421_bk1_listening_fmri.csv', 'run-2':'Logs/041421/041421_bk2_listening_fmri.csv'},
        'sub-10': {'run-1': 'Logs/072821/072821_bk1_listening_fmri.csv', 'run-2':'Logs/072821/072821_bk2_listening_fmri.csv'},
        'sub-11': {'run-1': 'Logs/073021/073021_bk1_listening_fmri.csv', 'run-2':'Logs/073021/073021_bk2_listening_fmri.csv'},
        'sub-12': {'run-1': 'Logs/082021/082021_bk1_listening_fmri.csv', 'run-2':'Logs/082021/082021_bk2_listening_fmri.csv'},
        'sub-13': {'run-1': 'Logs/090321/090321_bk1_listening_fmri.csv', 'run-2':'Logs/090321/090321_bk2_listening_fmri.csv'},
        'sub-14': {'run-1':'Logs/091621/091621_listen1_file.csv', 'run-2':'Logs/091621/091621_bk2_listening_fmri.csv', 'run-3':'Logs/091621/091621_listen3_file.csv'},
        'sub-15': {'run-1': 'Logs/092021/092021_bk1_listening_fmri.csv', 'run-2':'Logs/092021/092021_bk2_listening_fmri.csv'},
        'sub-16': {'run-1': 'Logs/092821/092821_bk1_listening_fmri.csv', 'run-2':'Logs/092821/092821_bk2_listening_fmri.csv'},
        'sub-17': {'run-1': 'Logs/100621/100621_bk1_listening_fmri.csv', 'run-2':'Logs/100621/100621_bk2_listening_fmri.csv'},
        'sub-18': {'run-1': 'Logs/100721/100721_bk1_listening_fmri.csv', 'run-2':'Logs/100721/100721_bk2_listening_fmri.csv'},
        'sub-19': {'run-1': 'Logs/101221/101221_bk1_listening_fmri.csv', 'run-2':'Logs/101221/101221_bk2_listening_fmri.csv'},
        'sub-20': {'run-1': 'Logs/101821/101821_bk1_listening_fmri.csv', 'run-2':'Logs/101821/101821_bk2_listening_fmri.csv'},
        'sub-21': {'run-1': 'Logs/102121/102121_bk1_listening_fmri.csv', 'run-2':'Logs/102121/102121_bk2_listening_fmri.csv'},
        'sub-22': {'run-1': 'Logs/102221/102221_bk1_listening_fmri.csv', 'run-2':'Logs/102221/102221_bk2_listening_fmri.csv'},
        'sub-23': {'run-1': 'Logs/102921/102921_bk1_listening_fmri.csv', 'run-2':'Logs/102921/102921_bk2_listening_fmri.csv'},
        'sub-24': {'run-1': 'Logs/110521/110521_bk1_listening_fmri.csv', 'run-2':'Logs/110521/110521_listen2_file.csv', 'run-4':'Logs/110521/110521_listen4_file.csv'},
        'sub-25': {'run-1': 'Logs/110621/110621_bk1_listening_fmri.csv', 'run-2':'Logs/110621/110621_bk2_listening_fmri.csv'},
        'sub-26': {'run-1': 'Logs/110821/110821_bk1_listening_fmri.csv', 'run-2':'Logs/110821/110821_bk2_listening_fmri.csv'},
        'sub-27': {'run-1': 'Logs/111221/111221_bk1_listening_fmri.csv', 'run-2':'Logs/111221/111221_bk2_listening_fmri.csv'},
        'sub-28': {'run-1': 'Logs/111721/111721_bk1_listening_fmri.csv', 'run-2':'Logs/111721/111721_bk2_listening_fmri.csv'},
        'sub-29': {'run-1': 'Logs/011821/011821_bk1_listening_fmri.csv', 'run-2':'Logs/011821/011821_bk2_listening_fmri.csv'},
        'sub-30': {'run-1': 'Logs/012122/012122_bk1_listening_fmri.csv', 'run-2':'Logs/012122/012122_bk2_listening_fmri.csv'},
        'sub-31': {'run-1': 'Logs/021822/021822_bk1_listening_fmri.csv', 'run-2':'Logs/021822/021822_bk2_listening_fmri.csv'},
        'sub-32': {'run-1': 'Logs/022122/022122_bk1_listening_fmri.csv', 'run-2':'Logs/022122/022122_bk2_listening_fmri.csv'},
        'sub-33': {'run-1': 'Logs/022222/022222_bk1_listening_fmri.csv', 'run-2':'Logs/022222/022222_bk2_listening_fmri.csv'},
        'sub-34': {'run-1': 'Logs/030422/030422_bk1_listening_fmri.csv', 'run-2':'Logs/030422/030422_bk2_listening_fmri.csv'},
        'sub-35': {'run-1': 'Logs/030722/030722_bk1_listening_fmri.csv', 'run-2':'Logs/030722/030722_bk2_listening_fmri.csv'},
        'sub-36': {'run-1': 'Logs/031722/031722_bk1_listening_fmri.csv', 'run-2':'Logs/031722/031722_bk2_listening_fmri.csv'},
        'sub-37': {'run-1': 'Logs/032822/032822_bk1_listening_fmri.csv', 'run-2':'Logs/032822/032822_bk2_listening_fmri.csv'},
        'sub-38': {'run-1': 'Logs/040122/040122_bk1_listening_fmri.csv', 'run-2':'Logs/040122/040122_bk2_listening_fmri.csv'}
    }
    
    
    #instantiating new dict
    new_dict = {}
    
    n = len(list_bids)
    for i in range(0, n):
        this_subj = list_bids[i]
        new_dict[this_subj] = original_dict[this_subj]
        
    return new_dict