##########################################################################
#########  PART 3:Intercomparison of Model and Satellite Data    #########
#########                  Question 3.2                          #########
######### NAME: Edson Nkonde  StudentID: 21810910                #########
##########################################################################
"""   Contains code for extracting ozone data values from GlobModel    """

def readGlobModel(filename,lonvals,latvals):
    """ Takes three arguments,file name of GlobModel data and two arrays one of 
    latitude and the other holding longitude values. These define the points 
    where the data is extracted from the GlobModel NetCDF file. The arrays of the 
    latitude & latitude must be of equal length. Returns extracted GlobModel data 
    in Dobson units (1Dobson=2.1414e-5 kg/m2)"""
    
    import netCDF4
    import numpy as np
    import netcdfUtils
    #1-Dobson=2.1414e-5 kg/m2
    dobson=2.1414e-5 
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
         data=(datavals/dobson)
         
    return data
 

    
    
    
    
    