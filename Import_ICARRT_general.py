# -*- coding: utf-8 -*-
"""
This script imports ICARRT format data into a pandas dataframe with a DateTimeIndex and saves a csv
Based on ICARRT format V1.1 (https://www-air.larc.nasa.gov/missions/etc/IcarttDataFormat.htm)
Created on Mon Jan 16 , 2017
@author: meganwillis

To run this script:
Import_ICARRT_general.py YYYYMMDD year month day fname TimeName Instrument Fnum
"""

################################
import numpy as np  
import pandas as pd 
import datetime                          
import sys 
import csv                       
#################################

#########################
####-EXTERNAL INPUT:#####
#########################

if len(sys.argv) == 9: #these are mostly for builidng file names, change to suite your file names
    date  = int(sys.argv[1]) #YYYYMMDD
    year  = int(sys.argv[2])
    month  = int(sys.argv[3]) # month and day without leading zeros
    day  = int(sys.argv[4])
    fname = str(sys.argv[5]) # e.g., "AIMMS_Polar6_20140705_R1.ict"
    TimeName = str(sys.argv[6]) #e.g., time, TimeWave, Time_UTC whatever is in the file
    Instrument = str(sys.argv[7])#string for output file name
    Fnum = str(sys.argv[8]) # flight number for 2015 data since we had many flights on the same day
  
else:
    print('You forgot the input arguements!')
    
#########################
####-INPUT PATHS:########
#########################
# base path   
path0 = '/Users/meganwillis/Documents/Data/NETCARE2015/AuxData_ICARRT_R1/' #put your path here!
# full path
ICARRTpath = path0 + fname

####################################################
######----------------MAIN-----------------#########
####################################################
#get some information on the iCARRT file
with open(ICARRTpath, 'r') as f:
    first_line = f.readline().strip()
    np_header = int(first_line[0:2]) - 1 #[0:2] for most, [0:3] for files >100 lines
    reader = csv.reader(f)
    csvlist = list(reader)
    missVallist = csvlist[10] #grab this missing value flags, put in a list
    columnlist = csvlist[np_header-1] #grab the names of the columns, put them in a list
    del(csvlist)
 
#open the ICARRT file and put it into a dataframe with a DatetimeIndex 
df = pd.read_csv(ICARRTpath, header = np_header, na_values = ['nan', ' nan'], low_memory=False)
epoch_time = (datetime.datetime(year, month, day) - datetime.datetime(1970, 1, 1)).total_seconds()
tempdf = df.set_index(pd.DatetimeIndex(pd.to_datetime(df[TimeName]+epoch_time, unit='s')))
output = tempdf.drop(tempdf.columns[[0]], axis = 1)
del(df, tempdf)

#fix the spaces preceding all column names from the ICARRT file
newcolumn = columnlist
for i in range(len(columnlist)):
    newcolumn[i] = columnlist[i].replace(" ", "")
del(newcolumn[0])
output.columns = newcolumn


#replace missing values with np.nan
for column in output: #column is a string
    missVal = float(missVallist[output.columns.get_loc(column)]) #integer index of the column to use for missingVal list lookup
    output[column].replace(missVal, np.nan, inplace = True)

#save output
outfile = path0 + Instrument+"_R2_"+str(date)+"_pd.csv"
print('*** Saving to :'+ outfile)
output.to_csv(outfile)
















