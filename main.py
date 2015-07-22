import netCDF4
import extract
import plotting
import netcdfUtils
import numpy as np
#import datetime
#from mpl_toolkits.basemap import Basemap, shiftgrid
vfile=("C:/Users/Developer202/Desktop/MWR/Data/Reanalysis/Surface/vwnd.mon.mean.nc")
ufile=("C:/Users/Developer202/Desktop/MWR/Data/Reanalysis/Surface/uwnd.mon.mean.nc")
varnameV='vwnd'
varnameU='uwnd'
tIndex=800
zIndex=0
Winds=plotMap(vfile,ufile, varnameV, varnameU, tIndex, zIndex)
Winds
def plotMap(vfile,ufile,varnameV,varnameU, tIndex, zIndex):
    """ TODO: add a docstring! """
    lonValues=[]
    ncV = netCDF4.Dataset(vfile)
    ncU = netCDF4.Dataset(ufile)
    dataVarV = ncV.variables[varnameV]
    dataVarU = ncU.variables[varnameU]
    # Extract the required data
    dataV = extract.extractMapData(ncV, dataVarV, tIndex, zIndex)
    dataU = extract.extractMapData(ncU, dataVarU, tIndex, zIndex)
    
    # Find the longitude and latitude values
    lonVar = netcdfUtils.findLongitudeVar(ncV, dataVarV)
    lonVals = lonVar[:]
    if (lonVals>180).all():
        lonValues.append(lonVals-360)
    lonValues.append(lonVals)
    latVar = netcdfUtils.findLatitudeVar(ncV, dataVarV)
    latVals = latVar[:]
    
    
    
    #title = "Plot of %s" % netcdfUtils.getTitle(dataVarV)
    
    #plotting.displayMapPlot(dataV, lonVals, latVals, title)
    plotting.displayWindMapPlot(dataV,dataU, lonVals, latVals)
    
##########################################################################
#########                  PART 2:Non-Map Plots                  #########
#########                      Question 2.1                      #########
#########           NAME: Edson Nkonde  StudentID: 21810910      #########
##########################################################################

def plotVerticalSection(filename,varIdentifier,vertSection,coordVal,tIndex):
    """Takes five aruguments i.e. a string representing location of NetCDF file,
    variable identifier, string indicating whether vertical section is 
    North-South (NS) or East-West (EW), the value of latitude/longitude depending
    on EW or NS, and the index along the time axis for which to get the data. Uses 
    the extractVerticalSection() function from the extract module to extract data.
    Plots using the displayVertSectionPlot() function from the plotting module."""
    import netCDF4
    import netcdfUtils
    import plotting
    nc=netCDF4.Dataset(filename) #A netCDF4 dataset Object
    dataVar=nc.variables[varIdentifier] # A varible object representing a data variable ('lat' or 'latitude')
    # Check that longitude,latitude, vertical and time variables are present
    lonVar = netcdfUtils.findLongitudeVar(nc, dataVar)
    latVar = netcdfUtils.findLatitudeVar(nc, dataVar)
    zVar=netcdfUtils.findVerticalVar(nc,dataVar)
    #check if string that indicate vertical section is EW or NS else raise error
    if vertSection!='NS'and vertSection!='EW':
        raise ValueError("Only NS or EW can be used to indicate Vertical section") 
    # if the vertical section identifier is North-South get latitudes
    if vertSection=='NS':
        #check if the slicing longitude is within the range of values
        if coordVal<-180 or coordVal>180:
            raise ValueError("The  Longitude values range from -180(180W) to 180(180E)") 
        #get the latitude values for the x axis   
        coordValues=latVar[:]
    # if the vertical section identifier is East-West get longitudes    
    elif vertSection=='EW':
        #check if the slicing latitude is within the range of values
        if coordVal<-90 or coordVal>90:
            raise ValueError("The Latitude values range from -90(90S) to +90(90N)") 
        #get the longitude values for the x axis    
        coordValues=lonVar[:]
    #check if the latitude, longitude and vertical dimesions are present in file    
    if lonVar is None or latVar is None :
        raise ValueError("Cannot extract map data if longitude and latitude are not present")
    if zVar is None:
        raise ValueError("Cannot extract map data if Vertical dimension is not present") 
    #extract data as well as the vertical and longitude/latitude coordinates      
    data=extract.extractVerticalSection(nc,dataVar,vertSection,tIndex,coordVal) 
    #get the title of the plot
    title=netcdfUtils.getTitle(dataVar)
    #plot the exrated data using the displayVertSectionPlot() from plotting module
    plotting.displayVertSectionPlot(data,zVar,coordValues,title,vertSection,coordVal)
    return  
##########################################################################
#########                  PART 2:Non-Map Plots                  #########
#########                      Question 2.2                      #########
#########           NAME: Edson Nkonde  StudentID: 21810910      #########
##########################################################################

def plotTimeseries(filename,varIdentifier,lonVal,latVal,zVal):
    """Takes five aruguments i.e. a string representing location of NetCDF file,
    variable identifier, the longitude and latitude values in degress as well as
    the value of the vertical axis in the units used in the data file
    (this is ignored if the data variable has no vertical dimension). Uses
    the extractTimeseries() function in the extract module and plot using the 
    displayTimeseriesPlot() function in the plotting module."""
    import netcdfUtils
    import netCDF4 
    import plotting
    #A netCDF4 dataset Object
    nc=netCDF4.Dataset(filename) 
    # A varible object representing a data variable (e.g. sst)
    dataVar=nc.variables[varIdentifier] 
    # Check that longitude,latitude, vertical and time variables are present
    lonVar = netcdfUtils.findLongitudeVar(nc, dataVar)
    latVar = netcdfUtils.findLatitudeVar(nc, dataVar)
    timeVar=netcdfUtils.findTimeVar(nc,dataVar)
    
    #check if the file has latitude, longitude and time dimensions
    if lonVar is None or latVar is None or timeVar is None:
        raise ValueError("Cannot extract map data if longitude, latitude & time are abscent")
   
    #extract data as well as the vertical and longitude/latitude coordinates      
    data=extract.extractTimeseries(nc,dataVar,lonVal,latVal,zVal) 
    # get the title of the plot
    title=netcdfUtils.getTitle(dataVar)
    #plot the data against time
    plotting.displayTimeseriesPlot(nc,dataVar,data[0],data[1],title)
       
    return
#### Here are some test functions.
#### Simply run this script to run them.

#if __name__ == '__main__':
    #plotMap("POLCOMS.nc", "POT", 0,0)
     #plotMap("C:/Users/Developer202/Desktop/MWR/Data/Reanalysis/Surface/vwnd.mon.mean.nc","vwnd",800,0)
     #plotMap("C:/Users/Developer202/Desktop/MWR/Data/Reanalysis/Surface/uwnd.mon.mean.nc","uwnd",800,0)
    #plotMap("GlobModel_temp.nc", "ta", 0,5)
    #plotMap("GlobModel_ozone.nc", "colo3", 0,5)
    #plotMap("rfe2015_02_seas_anom.nc","rfe",0,5)
    #plotMap("sst.day.mean.2014.v2.nc","sst",0,5)
    #plotMap("FOAM_Natl.nc", "ssh", 0,0)
    #plotMap("HadCEM.nc", "salinity", 0,10)
    # The OSTIA dataset is large, so this test can be slow.  Uncomment
    # this line to run it
    #plotMap("OSTIA.nc", "analysed_sst", 0,0)
    