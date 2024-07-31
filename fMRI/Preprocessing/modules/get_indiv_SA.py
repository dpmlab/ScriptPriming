import numpy as np
import pandas as pd

def get_indiv_SA(file_dict, story_order, priming_order):
    
    indiv_SA = dict()

    for sub in story_order:
        this_behav_file = pd.read_csv(file_dict[sub])
        this_df = pd.DataFrame(columns=['sub','story','prime','Q1', 'A1', 'Q2','A2','Q3','A3','Q4','A4','Q5','A5','Q6',
                                       'A6','Q7','A7','Q8','A8'])
        for i in range(16):
            if priming_order[sub][i] != 3:
                # Getting the schema order
                schema_order = this_behav_file['order of question'].values[this_behav_file['count']==i][0]
                schema_order = schema_order.split("[")[1]
                schema_order = schema_order.split("]")[0]
                schema_order = np.fromstring(schema_order, dtype=int, sep=',')
                # Extracting SA
                answer1 = this_behav_file['question1_answer'].values[this_behav_file['count']==i][0]
                answer2 = this_behav_file['question2_answer'].values[this_behav_file['count']==i][0]
                answer3 = this_behav_file['question3_answer'].values[this_behav_file['count']==i][0]
                answer4 = this_behav_file['question4_answer'].values[this_behav_file['count']==i][0]
                answer5 = this_behav_file['question5_answer'].values[this_behav_file['count']==i][0]
                answer6 = this_behav_file['question6_answer'].values[this_behav_file['count']==i][0]
                answer7 = this_behav_file['question7_answer'].values[this_behav_file['count']==i][0]
                answer8 = this_behav_file['question8_answer'].values[this_behav_file['count']==i][0]
                # Ordering and storing SA
                # 1 means that social questions were first 
                if schema_order[0] == 1:
                    q1 = answer5
                    q2 = answer6
                    q3 = answer7
                    q4 = answer8
                    q5 = answer1
                    q6 = answer2
                    q7 = answer3
                    q8 = answer4
                else:
                    q1 = answer1
                    q2 = answer2
                    q3 = answer3
                    q4 = answer4
                    q5 = answer5
                    q6 = answer6
                    q7 = answer7
                    q8 = answer8
                this_df.loc[len(this_df.index)] = [sub, story_order[sub][i], priming_order[sub][i], q1, '', q2, '',
                                                  q3, '', q4, '', q5,'', q6,'', q7,'', q8, ''] 
        indiv_SA[sub] = this_df
        
    return indiv_SA