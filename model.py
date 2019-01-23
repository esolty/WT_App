from pandas import DataFrame
import pandas as pd
import numpy as np
from shutil import copyfile

# for reading and dataframing dbfs
from dbfread import DBF
# for writing to dbfs
import dbf

import os.path
from pathlib import Path

# Functions for use in Processing Pipeline

# time it!!
from timeit import default_timer as time

# function for comparing GW WTs to GW WTs standard sizes
# to be used while iterating over rows in references table

def auto_select_checkboxes(pipe_wall_thickness=3):

    if pipe_wall_thickness == 3:
        return([3.2 , 3.4 , 3.6 , 4.0 , 4.4 , 4.8 , 5.2 , 5.6 , 6.4 , 7.1])

    if pipe_wall_thickness > 3:
        return([9.53, 10.31, 11.13, 11.91, 12.7,14.27,15.88,17.48,19.05,20.62,22.23,23.83,25.40, 26.97, 28.58, 30.18, 31.75])

        
    #pipe_WT_TBD = [3.2 , 3.4 , 3.6 , 4.0 , 4.4 , 4.8 , 5.2 , 5.6 , 6.4 , 7.1] # WTs for 06 pipe - full
    #pipe_WT_TBD = [3.2 , 3.6 ,  4.4 ,  5.2 , 6.4 , 7.1] # WTs for 06 pipe - edited
    #pipe_WT_TBD = [6.4,7.1,7.9,8.7,9.53, 10.31, 11.13, 11.91, 12.7] # WTs for 16 pipe

    #pipe_WT_TBD = [5.6,6.4,7.1,7.8,8.7,9.3,11.1, 12.7] # WTs for 10 pipe edited
    #pipe_WT_TBD = [6.4,7.1,7.9,9.5, 10.3, 11.1, 11.9, 12.7] # WTs for 16 pipe edited
    #pipe_WT_TBD = [9.53, 10.31, 11.13, 11.91, 12.7] # WTs for 20 pipe
    #pipe_WT_TBD = [9.53, 10.31, 11.13, 11.91, 12.7] # WTs for 24 pipe
    #pipe_WT_TBD = [9.53, 10.31, 11.13, 11.91, 12.7,14.27,15.88,17.48,19.05,20.62,22.23,23.83,25.40, 26.97, 28.58, 30.18, 31.75] # WTs for 36 pipe




def compare_GW_WTs(pipe_WT_TBD,GW_WT_Cal_section):

    # if no pipe WT list provided just return selection
    if not pipe_WT_TBD:  
        return GW_WT_Cal_section
    
    else:
        # retrn WT closest to calculated WT
        closest_pipe_WT = pipe_WT_TBD[len(pipe_WT_TBD)-1]
        # starting smallest difference set high to be replaced
        smallest_difference = pipe_WT_TBD[len(pipe_WT_TBD)-1]+100
            
        for i in pipe_WT_TBD:
            check = abs(i - GW_WT_Cal_section)
            
            if check < smallest_difference:

                smallest_difference = check
                closest_pipe_WT = i
            
    return closest_pipe_WT  

# copy dbf
def make_dbf_copy(path):
    
    table_copy = path[:-4]+"_copy"+path[-4:]
    count = 0
    
    while Path(table_copy).exists():
        count += 1
        table_copy = path[:-4]+"_copy"+str(count)+path[-4:]
        
    copyfile(path, table_copy)
    
    return table_copy

def write_to_table(dbf_path,references_dataFrame, fields = ['WT_ASS','TYPE']):
    count = 0
    
    table = dbf.Table(dbf_path)    
    table.open()
    for record in table:
        with record as r:  
            
            if 'WT_ASS' in fields:
                r.wt_ass = references_dataFrame.iloc[count]['WT_ASS']                
            if 'TYPE' in fields:
                r.type = references_dataFrame.iloc[count]['TYPE']

                
            count += 1         
    table.close()

# selecting Gw_ups and GW_downs
# Go through GWs and if they are close to next  value in list

def assign_GW_ups_downs(references_dataFrame,pipe_WT_TBD):
    
    prior_WT = 0.0
    flange = False
    
    
    for index, row in references_dataFrame.iterrows():
        
        if row['TYPE'] =='Valve':
            flange = True
        
        if row['TYPE'] =='Flange':
            flange = True
            
        
        if row['TYPE'] == "GirthWeld" or row['TYPE'] == "GW_wt_up" or row['TYPE'] == "GW_wt_dwn":
            
            
            WT = row['WT_CALC']# field WT_calc

            new_WT = compare_GW_WTs(pipe_WT_TBD,WT)

            # check if new wall thickness is different from previous one and assign new type
            
            new_text = ''
            
            if prior_WT < 0.01:
                new_text = "GirthWeld"
                
            elif new_WT > prior_WT:
                new_text = "GW_wt_up"
                    
            elif new_WT < prior_WT:
                new_text = "GW_wt_dwn"

            
            elif new_WT == prior_WT:
                new_text = "GirthWeld"
            
            #if flange present in prior don't change type or WT
            if flange:
                new_WT = prior_WT
                new_text = "GirthWeld"
                flange = False
                Valve = False
                
            index_type = references_dataFrame.columns.get_loc("TYPE")
            
            # Assign GW type
            references_dataFrame.iat[index,index_type] = new_text
                #references_dataFrame.iat[GW,5] = 55

            prior_WT = new_WT
            
    return references_dataFrame

def WT_processing_pipeline(path, pipe_WT_TBD, assign_types = False, makecopy = True):
    # copy dbf to memory in pandas dataframe
    
    tic = time()

    dbf_ref = DBF(path, ignore_missing_memofile='yes')
    references_dataFrame = DataFrame(iter(dbf_ref))
    
    if assign_types:
        references_dataFrame = assign_GW_ups_downs(references_dataFrame,pipe_WT_TBD)
    

    
    references_dataFrame['WT_ASS'] = 0.0
    #pipe_WT_TBD = []
    GW_WT_list = []
    GW_index_list = []
    sleeve = False
    assigned_value_list = []
    clamp = False

    for index, row in references_dataFrame.iterrows():

        # Check for sleeves, tees, installations  
        if row['TYPE'] == "AS_Sleeve":
            sleeve = True

        if row['TYPE'] == "AE_Sleeve":
            sleeve = False

        if row['TYPE'] == "Clamp":
            clamp = True


        # Check for end of a GWs section and apply WT
        if row['TYPE'] == "GW_wt_dwn" or row['TYPE'] == "GW_wt_up" or row['TYPE'] == "AE_Receiv":
            GW_WT_list_mean = np.mean(GW_WT_list)
            GW_WT_list_median = np.median(GW_WT_list)

            # Compare WTs to list if it exists
            assigned_value = compare_GW_WTs(pipe_WT_TBD,GW_WT_list_median)


            # track assigned values
            assigned_value_list.append(assigned_value)

            index_wta = references_dataFrame.columns.get_loc("WT_ASS")
            # Assign GW WT
            for GW in GW_index_list:

                references_dataFrame.iat[GW,index_wta] = assigned_value
                #references_dataFrame.iat[GW,5] = 55

            # start new lists
            GW_WT_list = []
            GW_index_list = []

            if row['TYPE'] != "AE_Receiv":
                # populate with last gw up or down
                GW_WT_list.append(row['WT_CALC'])
                GW_index_list.append(index)


        # Create a list of a section of GWs
        if row['TYPE'] == "GirthWeld":

            # if sleeve or present do not append the GW WT calculated value just the index position
            if sleeve or clamp:
                GW_index_list.append(index)            
                clamp = False            
            else:
                GW_WT_list.append(row['WT_CALC'])
                GW_index_list.append(index)
                
    if makecopy:
        table_copy = make_dbf_copy(path)
    else:
        # overwriting references db
        table_copy = path
        
    write_to_table(table_copy,references_dataFrame)
    
    toc = time()
    
    
    print("Task took {0:.{1}f} seconds".format(toc-tic,1))
