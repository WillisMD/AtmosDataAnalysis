# -*- coding: utf-8 -*-
"""
A general time matching code for data with irregular time stamps
Matchdf has the time stamp we want, INdf is the data we want to time match
The code will average the data from INdf over a user-specified time range to produce a time series with timestamps from Matchdf
Make sure to change/check I/O for INdf, Matchdf and OUTdf

Created on Thu Nov 10, 2016
@author: meganwillis

To run this script:
TimeMatch.py dt
"""

################################
import numpy as np  
import pandas as pd 
import datetime
import sys                        
#################################

#########################
####-EXTERNAL INPUT:#####
#########################

if len(sys.argv) == 2:
    dt  = float(sys.argv[1]) # time range in minutesm, this is the time range you want to average INdf over to generate data for each time point in Matchdf
    
else:
    print('You forgot the input arguements!')

#########################
####-INPUT PATHS:########
#########################
#put your paths here
Matchfile = 'path to file' #data with the time stamp you want

INfile = 'path to file' #data to change the time stamp for

####################################################
######-------- Function Definitions--------#########
####################################################
def getIgor_csv(pfilex):
    ''' Deals with tim stamps from Igor '''
    epochDelta = 2082844800 #number of seconds between Jan 1 1904 and Jan 1 1970 to convert form Igor time to Epoch time
    df = pd.read_csv(pfilex) 
    tempdf = df.set_index(pd.DatetimeIndex(pd.to_datetime(df['tseries']-epochDelta, unit = 's')))
    output = tempdf.drop('tseries', axis = 1)
    del(df,tempdf)
    return output
    
####################################################
######----------------MAIN:-----------------########
####################################################

###############################################################################
#########################--- get dataframes:---################################
###############################################################################
INdf = pd.read_csv(INfile, parse_dates=True, index_col = 'tseries')
Ncol = len(INdf.columns)

Matchdf = pd.read_csv(Matchfile, parse_dates=True, index_col = 't_series')
OUTdf = pd.DataFrame(index = pd.DatetimeIndex(Matchdf.index), columns = INdf.columns) #this initializes an output data frame filled with NaN

###############################################################################
#########################--- match the time:---################################
###############################################################################

for row in OUTdf.itertuples(): #iterator contains the df.index by default
    lowtime = row[0] - pd.Timedelta(minutes = dt/2)#find the beginning and end of the section of time we want to average over
    #print("lowtime = " + str(lowtime))
    hightime = row[0] + pd.Timedelta(minutes = dt/2)
    #print("hightime = " + str(hightime))
    
    #subset the dataframe for the time range we want
    tempdf = INdf[(INdf.index >= lowtime) & (INdf.index <= hightime)] #could also use pd.query here but not sure if this only takes columns of indices of the dataframe
    #print(tempdf) #this is sometimes an empty dataframe if there are no timestamps in AMSdf - i.e., when there are chunks of missing data
    #print("\n")
    
    if tempdf.empty: # go to the next iteration of the loop if we have an empty dataframe
        continue
    else:  #otherwise loop through each column, then loop through each row in the column and take the average of points that are not NaN
        for i in range(1,Ncol+1): #looping through columns
            ColName = INdf.columns[i-1] #this looks a bit confusing because we need to use i to index both the dataframe and the tuple pulled out in the next loop
            #print(ColName)
            count = 0 #initialize at zero
            total = 0
            for row1 in tempdf.itertuples(): #looping through rows - have to pull out the tuple each time
                #print(np.isnan(row1[i]))
                if np.isnan(row1[i]) == False: #check if there is data
                    count += 1
                    #print(count)
                    total += row1[i]
                    #print(total)
            if count != 0: #if we are not dividing by zero
                OUTdf.loc[row[0], ColName] = total/count
            else: #if dividing by zero, contine to the next iteration
                continue
        
###############################################################################
#########################--- save some output:---##############################
###############################################################################
outfile = 'path to output file' #put your path here
print('*** Saving to :'+ outfile)
OUTdf.to_csv(outfile)




