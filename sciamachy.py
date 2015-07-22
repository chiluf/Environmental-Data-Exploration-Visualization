
##########################################################################
#########  PART 3:Intercomparison of Model and Satellite Data    #########
#########                  Question 3.1                          #########
######### NAME: Edson Nkonde  StudentID: 21810910                #########
##########################################################################
""" Contains code for producing Sciamachy data scatter plot """

def plotSciamachy(sciamachy):
    """ Takes only one argument, the name of the SCIAMACHY data file, extracts the 
    data from the file, producing a scatter plot of the data"""
    #Libraries to extract data & coordinates from the Sciamachy file and plot Scatter Plot
    import matplotlib.pyplot as plt
    import matplotlib.mlab as mlab
    import matplotlib as mpl
    #Extract Latitudes, longitudes and ozone Data
    r=mlab.csv2rec(sciamachy)
    latvals=r.lat #array of latitude values 
    lonvals=r.lon #array of longitude values
    data=r.o3_du #array of sciamachy ozone data values
    #Clear previous plots
    plt.clf() 
    #Generating the scatter plot, axis labels and the colorbar
    plt.title("Sciamachy Scatter Plot")
    plt.xlabel("Longitude (degrees east)")
    plt.ylabel("Latitude (degrees north)")
    plt.scatter(lonvals, latvals, c=data,edgecolors='none', norm=mpl.colors.SymLogNorm(linthresh=10, vmin=min(data), vmax=max(data)))
    plt.colorbar()
    plt.show()
    
