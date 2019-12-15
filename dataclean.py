# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 17:39:18 2019

@author: genev
"""


def cleanjobs(jobs):
    '''
    Clean the raw data from glassdoor. 
    Input: raw data of job information collected from Glassdoor.
    Output: Extract state name and delete state name with more than two letters. 
            Extract min salary and max salary without format and calculate average salary. 
            Replace None with np.nan in salary and state. 
            Delete rows with None jobTitle in the data frame. 
            Output of the function is a data frame after data cleaning.
   

    Parameters
    ----------
    jobs : TYPE
        DESCRIPTION.

    Returns
    -------
    jobs : TYPE
        DESCRIPTION.

    '''
    import numpy as np
    jobs = jobs[jobs['jobTitle'] != 'None']
    jobs['State'] = jobs['location'].str.split(", ", n = 1, expand = True).iloc[:,1]
    salaryesplit = jobs['salary'].str.split('-', n = 1, expand = True)
    salaryesplit[0] = salaryesplit[0].replace('None', np.nan)
    salaryesplit[1] = salaryesplit[0].replace('None', np.nan)
    salaryesplit = salaryesplit.replace('', np.nan)
    salaryesplit[1] = salaryesplit[1].str.split('(', n = 1, expand = True)[0]
    salaryesplit[1] = salaryesplit[1].str.replace('$','')
    salaryesplit[0] = salaryesplit[0].str.replace('$','')
    salaryesplit[1] = salaryesplit[1].str.replace('k','')
    salaryesplit[0] = salaryesplit[0].str.replace('k','')
    salaryesplit = salaryesplit[~salaryesplit[1].str.contains("Per",na=False)==True]
    jobs['Low Sal'] = salaryesplit[0].astype(float)
    jobs['High Sal'] = salaryesplit[1].astype(float)
    jobs['Average Sal'] = (jobs['Low Sal'] + jobs['High Sal'])/2
    return jobs
