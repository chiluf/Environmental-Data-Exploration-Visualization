# -*- coding: utf-8 -*-
"""
Created on Sun May 25 03:26:05 2014

@author: Edson
"""
import netCDF4
import numpy as np
import netcdfUtils
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib as mpl

#Extract Latitudes, longitudes and the Stations
coordinates=mlab.csv2rec("data/coordinates.csv")
latvals=coordinates.lat #array of latitude values for the stations
lonvals=coordinates.lon #array of longitude values for the stations
stationID=coordinates.station #Rain Gauge Stations
months=np.array(["01","02","03","04","05","06","07","08","09","10","11","12"])
days=np.array(["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"])

    
    
for month in range(months):
    for day in range(days):
        nc=netCDF4.Dataset('data\1983\rfe1983_'+repr(day)+'_'+repr(month)+'.nc','w')
        lonIndex=np.zeros(len(lonvals))
        latIndex=np.zeros(len(latvals))
        rfe=nc.variables['colo3'] #varible holding ozone data from GlobModel
        #Setting the time index where data should be extracted
        ozoneVals=ozoneVar[0] 
        #Initialize and set the length of the extracted data array
        datavals=np.zeros(len(lonvals))
        for i in range(len(lonvals)):
            #Get the index of each latitude & longitude  
            latIndex[i]=netcdfUtils.findNearestLatIndex(nc,ozoneVar,latvals[i])
            lonIndex[i]=netcdfUtils.findNearestLonIndex(nc,ozoneVar,lonvals[i])
            #Extract the data based on the indeces of the latitude & longitude          
            datavals[i]=ozoneVals[latIndex[i],lonIndex[i]]
    
    
    
    
    
def extractTamsatRFE(filename,lonvals,latvals):
    """ Takes three arguments,file name of GlobModel data and two arrays one of 
    latitude and the other holding longitude values. These define the points 
    where the data is extracted from the GlobModel NetCDF file. The arrays of the 
    latitude & latitude must be of equal length. Returns extracted GlobModel data 
    in Dobson units (1Dobson=2.1414e-5 kg/m2)"""
    
    #Initialize and set the length of the latitude & longitude indices
    lonIndex=np.zeros(len(lonvals))
    latIndex=np.zeros(len(latvals))
    
    nc=netCDF4.Dataset(filename) #A netCDF4 dataset Object
    ozoneVar=nc.variables['colo3'] #varible holding ozone data from GlobModel
    #Setting the time index where data should be extracted
    ozoneVals=ozoneVar[0] 
    #Initialize and set the length of the extracted data array
    datavals=np.zeros(len(lonvals))
   
    for i in range(len(lonvals)):
         #Get the index of each latitude & longitude  
         latIndex[i]=netcdfUtils.findNearestLatIndex(nc,ozoneVar,latvals[i])
         lonIndex[i]=netcdfUtils.findNearestLonIndex(nc,ozoneVar,lonvals[i])
         #Extract the data based on the indeces of the latitude & longitude          
         datavals[i]=ozoneVals[latIndex[i],lonIndex[i]]
         
         #convert the extracted data from kg/m2 to Dobson units
         
         
    return data
 