
""" Contains code for displaying data """

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np

def displayWindMapPlot(vdata,udata, lons, lats,):
    """ TODO add a docstring! """
    #plt.clf()
    #pc = plt.contourf(lons, lats, data, 20)
    #plt.colorbar(pc, orientation='horizontal')
    #plt.title(title)
    #plt.xlabel("longitude (degrees east)")
    #plt.ylabel("latitude (degrees north)")
    #plt.show()
    fig, ax = plt.subplots()
    # Do the plot code
    # make orthographic basemap.
    m = Basemap(projection='cyl',llcrnrlat=-40,urcrnrlat=0,\
            llcrnrlon=-20,urcrnrlon=60,resolution='l')

    X,Y=np.meshgrid(lons, lats)
    x,y=m(X,Y) #Convert to map coordinates
    #m.barbs(x,y,vdata,udata,20)
    m.quiver(x,y,vdata,udata,10)
    plt.streamplot(x,y,vdata,udata,10)
    #plt.colorbar(pc,orientation='horizontal')
    m.drawmapboundary()
    m.drawcountries()
    
    m.drawcoastlines(linewidth=1.5)
    
    fig.savefig('myimage.svg', format='svg', dpi=1200)
    plt.show()
    #m.drawparallels(parallels)
    #m.drawmeridians(meridians)
    
    
    """ Contains code for displaying data """

import matplotlib.pyplot as plt

def displayMapPlot(data, lons, lats, title):
    """ TODO add a docstring! """
    plt.clf()
    pc = plt.contourf(lons, lats, data, 20)
    plt.colorbar(pc, orientation='horizontal')
    plt.title(title)
    plt.xlabel("longitude (degrees east)")
    plt.ylabel("latitude (degrees north)")
    plt.show()
##########################################################################
#########                  PART 2:Non-Map Plots                  #########
#########                      Question 2.1                      #########
#########           NAME: Edson Nkonde  StudentID: 21810910      #########
##########################################################################    
def displayVertSectionPlot(data,zVar,coordValues,title,vertSection,coordVal):
    """ Take 6 arguments. Data values, vertical coordinate, latitude/longitude
    values,title of the plot, string indicating whether vertical section is from
    North-South or East-West, and a latitude/longitude value where the section is
    done. Plots the vertical section with title, labels and colorbar. """
    import netcdfUtils
    if vertSection=='NS':
         deg='Degress Longitude' 
    else:
        deg='Degress Latitude'
       #convert the longitude values so that they range from -180 to 180 
        coordValues=coordValues-180
    #clear the prevoius figure     
    plt.clf()
    #get the vertical coordinate name and units
    zVals=zVar[:]
    zAxisUnits=zVar.units
    zAxisName=zVar._name
    #If vertical axis increses downwards reverse the axis
    if netcdfUtils.isPositiveUp(zVar) is False:
        plt.gca().invert_yaxis()
    #plot the latitude or longitude against the vertical coordinate    
    pc = plt.contourf(coordValues,zVals,data, 20)
    plt.colorbar(pc, orientation='vertical')
    plt.title("%s Section of %s at %.1f %s" % (vertSection,title,coordVal,deg))
    if vertSection=='NS':
        plt.xlabel("latitude (degrees north)")
    else:
        plt.xlabel("longitude (degrees east)")   
    plt.ylabel("%s (%s)" % (zAxisName,zAxisUnits))
    plt.show()
    
##########################################################################
#########                  PART 2:Non-Map Plots                  #########
#########                      Question 2.2                      #########
#########           NAME: Edson Nkonde  StudentID: 21810910      #########
##########################################################################    
def displayTimeseriesPlot(nc,dataVar,data,timeVal,title):
    """ Takes NetCDF dataset, the variable data object, the data values, the 
    time values and the title of the plot. Plots time series of the data values """
    
    import datetime as dt
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    import netcdfUtils
    
    dayLocator    = mdates.DayLocator()
    hourLocator   = mdates.HourLocator()
    dateFmt = mdates.DateFormatter('%Y-%m-%d')
    # get the datum and delta from reading time units of the file
    timeVar=netcdfUtils.findTimeVar(nc,dataVar)
    year=timeVar.units[14:18]
    month=timeVar.units[19:21]
    day=timeVar.units[22:24]
    datum = dt.datetime(int(year), int(month),int(day))
    delta = dt.timedelta(seconds=1)
    # Convert the time values to datetime objects
    times = []
    for t in timeVal:
        times.append(datum + int(t) * delta)
   # Plot SST against the datetime objects
    plt.plot(times,data)
    plt.title("Sea surface temperature Timeseries")
    plt.ylabel("SST (" + dataVar.units + ")")
    plt.xlabel("Time")
    # format the ticks
    ax = plt.gca()
    ax.xaxis.set_major_locator(dayLocator)
    ax.xaxis.set_major_formatter(dateFmt)
    ax.xaxis.set_minor_locator(hourLocator)
    plt.show()


