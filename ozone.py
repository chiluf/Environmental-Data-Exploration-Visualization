##########################################################################
#########  PART 3:Intercomparison of Model and Satellite Data    #########
#########                  Question 3.4                          #########
######### NAME: Edson Nkonde  StudentID: 21810910                #########
##########################################################################
"""   Contains code for extracting ozone data values from GlobModel    """

#GlobModel='data/GlobModel_ozone.nc'
#sciamachy='data/sciamachy.csv'
#mapProjection='cyl'

def plotDifference(GlobModel,sciamachy):
    """ Takes two arguments, the name of NetCDF file containing the GlobModel
    simulated ozone data, and the name of the csv file containing SCIAMACHY ozone 
    data. Extracts data from the  two datasets, subtracts the GlobModel data
    from the SCIAMACHY data for each point. Produces a scatter plot of the difference"""
    
    #Libraries to extract data & coordinates and plot Scatter Plot
    import globmodel
    import matplotlib.pyplot as plt
    import matplotlib.mlab as mlab
    import matplotlib as mpl
    #Extract Latitudes, longitudes and ozone satellite Data
    r=mlab.csv2rec(sciamachy)
    latvals=r.lat
    lonvals=r.lon
    satelliteData=r.o3_du
    #Extract ozone simulated data from GlobModel using lat & lon from sciamachy 
    GlobModelData=globmodel.readGlobModel(GlobModel,lonvals,latvals)
    #Substract GlobModel ozone simulated data from Sciamachy sattellite ozone data
    diff=satelliteData-GlobModelData
    #Clear previous figures
    plt.clf()
    #Generating the scatter plot, axis labels and the colorbar
    plt.title("Sciamachy-GlobModel Difference Scatter Plot")
    plt.xlabel("Longitude (degrees east)")
    plt.ylabel("Latitude (degrees north)")
    plt.scatter(lonvals, latvals, c=diff,edgecolors='none', norm=mpl.colors.SymLogNorm(linthresh=10, vmin=min(diff), vmax=max(diff)))
    plt.colorbar()
    plt.show()
    return 
    
    
###########################################################################
#########   PART 3:Intercomparison of Model and Satellite Data    #########
#########                   Question 3.5                          #########
#########      NAME: Edson Nkonde  StudentID: 21810910            #########
###########################################################################

def plotDifferenceBasemap(GlobModel,sciamachy,mapProjection): 
    """ Takes three arguments, the name of NetCDF file containing the GlobModel
    simulated ozone data, the name of the csv file containing SCIAMACHY ozone 
    data and a string representing the Map projection to use. Uses the
    readGlobModel() function from the globmodel module to extract data from 
    the  GlobModel NetCDFdata, subtracts it from the SCIAMACHY data at 
    each point.Produces a scatter plot of the difference on the selected map projection """
    #Libraries to extract data & coordinates and plot on map projection
    import matplotlib.pyplot as plt
    import matplotlib.mlab as mlab
    import matplotlib as mpl
    import globmodel
    import numpy as np
    from mpl_toolkits.basemap import Basemap
    #Extract Latitudes, longitudes and ozone Data from the sciamachy
    r=mlab.csv2rec(sciamachy)
    latvals=r.lat #array of latitude values 
    lonvals=r.lon #array of longitude values
    satelliteData=r.o3_du #array of sciamachy ozone data values
    #Extract ozone simulated data from GlobModel using lat & lon from sciamachy 
    GlobModelData=globmodel.readGlobModel(GlobModel,lonvals,latvals)
    #Substract GlobModel ozone simulated data from Sciamachy sattellite ozone data
    diff=satelliteData-GlobModelData
    #Plotting using different map projections 
    #North-Polar-Stereographic (npstere),South-Polar-Stereographic (spstere) & 
    #Equidistant- Cylindrical Projections (cyl)
    
    #North-Polar-Stereographic (npstere)
    if mapProjection=='npstere': 
        #Clear previous figures
        plt.clf()
        # Setup north polar stereographic basemap. The longitude lon_0 is at 
        #6-o'clock, and the latitude circle boundinglat is tangent to the edge 
        #of the map at lon_0. Default value of lat_ts (latitude of true scale) is pole.
        m = Basemap(projection='npstere',boundinglat=10,lon_0=270,resolution='l')
        m.drawcoastlines()
        m.fillcontinents(color='none',lake_color='none')
        # Convert latitude & longitude to map projection coordinates
        nlonvals,nlatvals= m(lonvals,latvals)
        # Draw parallels and meridians.
        m.drawparallels(np.arange(-80.,81.,20.),labels=[False,True,True,False])
        m.drawmeridians(np.arange(-180.,181.,20.),labels=[True,False,False,True])
        # Draw continental boundaries
        m.drawmapboundary(fill_color='none')
        #Generate scatter Plots and colorbar on the North Polar Stereographic Projection 
        m.scatter(nlonvals, nlatvals, c=diff,edgecolors='none', norm=mpl.colors.SymLogNorm(linthresh=10, vmin=min(diff), vmax=max(diff)))
        plt.colorbar() 
        plt.title("Sciamachy-GlobModel Difference Scatter Plot""\n""North Polar Stereographic Projection")
        plt.show()
    #South-Polar-Stereographic (spstere)
    if mapProjection=='spstere':
        #Clear previous figures
        plt.clf()
        # setup north polar stereographic basemap. The longitude lon_0 is at 
        #6-o'clock, and the latitude circle boundinglat is tangent to the edge
        # of the map at lon_0. Default value of lat_ts (latitude of true scale) is pole.
        m = Basemap(projection='spstere',boundinglat=-10,lon_0=90,resolution='c')
        m.drawcoastlines()
        m.fillcontinents(color='none',lake_color='none')
        # Convert latitude & longitude to map projection coordinates
        nlonvals,nlatvals= m(lonvals,latvals)
        # draw parallels and meridians.
        m.drawparallels(np.arange(-80.,81.,20.),labels=[False,True,True,False])
        m.drawmeridians(np.arange(-180.,181.,20.),labels=[True,False,False,True])
        # Draw continental boundaries
        m.drawmapboundary(fill_color='none')
        #Generate scatter Plots and colorbar on the South Polar Stereographic Projection 
        m.scatter(nlonvals, nlatvals, c=diff,edgecolors='none', norm=mpl.colors.SymLogNorm(linthresh=10, vmin=min(diff), vmax=max(diff)))
        m.colorbar()
        plt.title("Sciamachy-GlobModel Difference Scatter Plot""\n""South Polar Stereographic Projection")
        plt.show()
        
    #Equidistant- Cylindrical Projections (cyl)                    
    if mapProjection=='cyl':
        #Clear previous figures
        plt.clf()
        # llcrnrlat,llcrnrlon,urcrnrlat,urcrnrlon
        # are the lat/lon values of the lower left and upper right corners of the map.
        # resolution = 'c' means use crude resolution coastlines.
        m = Basemap(projection='cyl',llcrnrlat=latvals[min(latvals)],urcrnrlat=latvals[max(latvals)],llcrnrlon=-180,urcrnrlon=180,resolution='c')
        m.drawcoastlines()
        # Convert latitude & longitude to map projection coordinates
        nlonvals,nlatvals= m(lonvals,latvals)
        # draw parallels and meridians.
        m.drawparallels(np.arange(-90.,91.,30.),labels=[False,True,True,False])
        m.drawmeridians(np.arange(-180.,181.,60.),labels=[True,False,False,True])
        # Draw continental boundaries and fill colors
        m.fillcontinents(color='none',lake_color='none')
        m.drawmapboundary(fill_color='none')
        #Generate scatter Plots and colorbar on the Equidistant Cylindrical Projection 
        plt.scatter(nlonvals, nlatvals, c=diff, edgecolors='none', norm=mpl.colors.SymLogNorm(linthresh=10, vmin=min(diff), vmax=max(diff)))
        plt.colorbar(orientation="horizontal")
        plt.title("Sciamachy-GlobModel Difference Scatter Plot""\n""Equidistant Cylindrical Projection")
        plt.xlabel('longitude')
        plt.show()
    return 
    
    
    
#diffb=plotDifferenceBasemap(GlobModel,sciamachy,mapProjection)
#diff=plotDifference(GlobModel,sciamachy)
