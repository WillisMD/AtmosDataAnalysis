# -*- coding: utf-8 -*-
"""
A function to bin aircraft data by altitude for embedding in another python script
Created on January 10, 2016
@author: meganwillis
"""

##########
import numpy as np
import pandas as pd
##########

####################################################
######-------- Function Definitions--------#########
####################################################

def BinbyAltitude(Data, nbins): #Data is the input dataframe for a particular flight
    #create altitude bins    
    maxAlt = Data['Altitude'].max()
    minAlt = Data['Altitude'].min()
    step = (maxAlt-minAlt)/(nbins+1)
    binedges = np.arange(minAlt, maxAlt, step) 
    #loop to create an array of bin-centered altitudes
    bincenters = np.zeros(nbins)
    it = np.nditer(bincenters, flags = ['c_index'], op_flags = ['readwrite']) #there is probably a vectorized way to do this
    for i in it:
        bincenters[it.index]=binedges[it.index]+((binedges[it.index+1]-binedges[it.index])/2)
    
    Binned = Data.groupby(pd.cut(Data['Altitude'], binedges)).describe(percentiles = [0.05,0.20,0.5,0.80,0.95]).unstack() #index is intervals
    Binned.drop('Altitude', axis=1)
    Data_bin= Binned.set_index(bincenters) #index is bin centers
    return Data_bin #returns a data frame with number of columns = nbins, index is altitude of bin center


