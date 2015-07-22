""" Contains code for extracting data from NetCDF files """

import netcdfUtils
import utils

def extractMapData(nc, dataVar, tIndex, zIndex):
    """ TODO: add a docstring! """
    # Find the number of dimensions for the data variable
    numDims = len(dataVar.dimensions)
    if numDims < 2 or numDims > 4:
        raise ValueError("Cannot extract data from variable with %d dimensions" % numDims)
    
    # Check that longitude and latitude variables are present
    lonVar = netcdfUtils.findLongitudeVar(nc, dataVar)
    latVar = netcdfUtils.findLatitudeVar(nc, dataVar)
    if lonVar is None or latVar is None:
        raise ValueError("Cannot extract map data if longitude and latitude are not present")
    
    # If this is a four-dimensional variable, assume that there are t,z,y,x axes, in this order
    if numDims == 4:
        return dataVar[tIndex,zIndex]
    elif numDims == 3:
        # We don't know if the first dimension is t or z
        tVar = netcdfUtils.findTimeVar(nc, dataVar)
        if tVar is None:
            # We assume the first dimension is z
            return dataVar[zIndex]
        else:
            # We assume the first dimension is t
            return dataVar[tIndex]
    else:
        # numDims must be 2
        return dataVar[:]
        
############################################################################
#########                    PART 2:Non-Map Plots                  #########
#########              Question 2.1 Extrcting Vertical Data        #########
#########             NAME: Edson Nkonde  StudentID: 21810910      #########
############################################################################
def extractVerticalSection(nc,dataVar,vertSection,tIndex,coordVal):
    """ Takes five arguments; the NetCDF dataset, the variable object, the 
    string reprenting verticle setion, the index along the time axis and the 
    index along the latitude/longitude. Using the arguments it extracts returns
    the data, from a NetCDF file"""
    
    import netcdfUtils
    # Find the number of dimensions for the data variable
    numDims = len(dataVar.dimensions)
    
    # check number of dimensions and raise error if they are not 2,or 3,or 4  
    if numDims < 3 or numDims > 4:
        raise ValueError("Cannot extract data from variable with %d dimensions" % numDims)
    # Check if the longitude, latitude and vertical dimensions are present
    lonVar = netcdfUtils.findLongitudeVar(nc, dataVar)
    latVar = netcdfUtils.findLatitudeVar(nc, dataVar)
    zVar=netcdfUtils.findVerticalVar(nc,dataVar)
    #raise error if the longitude, latitude and vertical dimensions are abscent
    if lonVar is None or latVar is None or zVar is None:
        raise ValueError("Cannot extract map data if longitude, latitude and Vertical dimensios are abscent")
    # change longitutude value from range (-180 to 180) into (0 to 360)
    if vertSection=='NS':
        #Map the slicing longitude from -180-to-180 to 0-360
        if min(lonVar[:])>=0:
            if coordVal<=0:
                coordVal=coordVal+180
            else:
                coordVal=coordVal+180        
     #the dimensions present are time, vertical, latitude or longitude
    if vertSection=='NS'and numDims == 4:
        coordVar=netcdfUtils.findLongitudeVar(nc, dataVar) 
        coordIndex=utils.findNearestIndex(coordVar,coordVal)
        return dataVar[tIndex,:,:,coordIndex]
    # the dimensions present must be vertical, latitude or longitude
    elif vertSection=='NS'and numDims == 3: 
        coordVar=netcdfUtils.findLongitudeVar(nc, dataVar) 
        coordIndex=utils.findNearestIndex(coordVar,coordVal)          
        return dataVar[:,:,coordIndex]
    # the dimensions present are time, vertical, latitude & longitude in that order
    if vertSection=='EW'and numDims == 4:
        coordVar=netcdfUtils.findLatitudeVar(nc, dataVar) 
        coordIndex=utils.findNearestIndex(coordVar,coordVal)       
        return dataVar[tIndex,:,coordIndex,:]
    # the dimensions present must be vertical, latitude & longitude in that order
    elif vertSection=='EW'and numDims == 3:
        coordVar=netcdfUtils.findLatitudeVar(nc, dataVar) 
        coordIndex=utils.findNearestIndex(coordVar,coordVal)  
        return dataVar[:,coordIndex,:]

##########################################################################
#########                  PART 2:Non-Map Plots                  #########
#########           Question 2.2 Extrcting TimeSeries Data       #########
#########          NAME: Edson Nkonde  StudentID: 21810910       #########
##########################################################################
def extractTimeseries(nc,dataVar,lonVal,latVal,zVal):
    """ Takes five arguments; the NetCDF dataset, the variable object, the 
    longitude value, the latitude value and the vertical value and use them to 
    extracts data and time values at the point described. It returns the data of 
    the  and variable represented by the variable object the time values for 
    each point described by the longitude, latitude and vertical values in the
    NetCDF file"""
    # Find the number of dimensions for the data variable
    numDims = len(dataVar.dimensions)
    
    # Check if the number of dimensions and raise error if they are not 3 or 4  
    if numDims < 3 or numDims > 4:
        raise ValueError("Cannot extract data from variable with %d dimensions" % numDims)
    # Check if longitude, latitude and vertical dimensions are present
    lonVar = netcdfUtils.findLongitudeVar(nc, dataVar)
    latVar = netcdfUtils.findLatitudeVar(nc, dataVar)
    timeVar=netcdfUtils.findTimeVar(nc,dataVar)
    zVar=netcdfUtils.findVerticalVar(nc,dataVar)
    timeVal=timeVar[:]
    # check if the longitude, latitude or the time dimension is abscent and raise error
    if lonVar is None or latVar is None or timeVar is None:
        raise ValueError("Cannot extract map data if longitude, latitude and time dimensios are abscent")
    
   # map the longitutude value from range (-180 to 180) onto (0 to 360) in the data file
    #lonVal=lonVal+180 
    if min(lonVar[:])>=0:
        if lonVal<0:
            lonVal=lonVal+180
    # if the dimensions are 4 i.e. time,vertical,latitude and longitude 
    if numDims == 4:
         #get the vertical,longitude and latitude indices
        lonIndex=utils.findNearestIndex(lonVar,lonVal)
        latIndex=utils.findNearestIndex(latVar,latVal)
        zIndex=utils.findNearestIndex(zVar,zVal)
        return dataVar[:,zIndex,latIndex,lonIndex],timeVal
    # if the dimensions are 3 ie time, latitude and longitude
    elif numDims == 3: 
        #get the longitude and latitude indices
        lonIndex=utils.findNearestIndex(lonVar,lonVal)
        latIndex=utils.findNearestIndex(latVar,latVal)         
        return dataVar[:,latIndex,lonIndex],timeVal