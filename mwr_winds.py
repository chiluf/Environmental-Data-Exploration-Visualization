import numpy as np
import matplotlib.pyplot as plt
import datetime
from mpl_toolkits.basemap import Basemap, shiftgrid
from netCDF4 import Dataset
# specify date to plot.
yyyy=2014; mm=10; dd=14; hh=00
date = datetime.datetime(yyyy,mm,dd,hh)
# set OpenDAP server URL.

meridional='C:/Users/Developer202/Desktop/MWR/Data/Reanalysis/Surface/vwnd.mon.mean.nc'
zonal='C:/Users/Developer202/Desktop/MWR/Data/Reanalysis/Surface/uwnd.mon.mean.nc'
vdata = Dataset(meridional)
udata = Dataset(zonal)
# read lats,lons
# reverse latitudes so they go from south to north.
lats = udata.variables['lat'][::-1]
lons = udata.variables['lon'][:]
# get sea level pressure and 10-m wind data.
# mult slp by 0.01 to put in units of hPa.
#slpin = 0.01*data.variables['Pressure_msl'][:].squeeze()
u = udata.variables['uwnd'][:]
v = vdata.variables['vwnd'][:]

speed=np.sqrt(u**2+v**2)
plt.barbs(lons,lats,u,v,speed)

# add cyclic points manually (could use addcyclic function)
#slp = np.zeros((slpin.shape[0],slpin.shape[1]+1),np.float)
#slp[:,0:-1] = slpin[::-1]; slp[:,-1] = slpin[::-1,0]
#u = np.zeros((uin.shape[0],uin.shape[1]+1),np.float64)
#u[:,0:-1] = uin[::-1]; u[:,-1] = uin[::-1,0]
#v = np.zeros((vin.shape[0],vin.shape[1]+1),np.float64)
#v[:,0:-1] = vin[::-1]; v[:,-1] = vin[::-1,0]
#longitudes.append(360.); longitudes = np.array(longitudes)
# make 2-d grid of lons, lats
#lons, lats = np.meshgrid(longitudes,latitudes)
# make orthographic basemap.
m = Basemap(resolution='c',projection='ortho',lat_0=60.,lon_0=-60.)
# create figure, add axes
fig1 = plt.figure(figsize=(8,10))
ax = fig1.add_axes([0.1,0.1,0.8,0.8])
# set desired contour levels.
clevs = np.arange(960,1061,5)
# compute native x,y coordinates of grid.
#x, y = m(lons, lats)
# define parallels and meridians to draw.
##parallels = np.arange(-80.,90,20.)
##meridians = np.arange(0.,360.,20.)
# plot SLP contours.
##CS1 = m.contour(x,y,clevs,linewidths=0.5,colors='k',animated=True)
CS2 = m.contourf(longitudes,longitudes,clevs,cmap=plt.cm.RdBu_r,animated=True)
# plot wind vectors on projection grid.
# first, shift grid so it goes from -180 to 180 (instead of 0 to 360
# in longitude).  Otherwise, interpolation is messed up.
#ugrid,newlons = shiftgrid(180.,uin,longitudes,start=False)
#vgrid,newlons = shiftgrid(180.,vin,longitudes,start=False)
# transform vectors to projection grid.
#uproj,vproj,xx,yy = \
#m.transform_vector(ugrid,vgrid,newlons,latitudes,31,31,returnxy=True,masked=True)
# now plot.
#Q = m.quiver(xx,yy,uproj,vproj,scale=700)
# make quiver key.
#qk = plt.quiverkey(Q, 0.1, 0.1, 20, '20 m/s', labelpos='W')
# draw coastlines, parallels, meridians.
m.drawcoastlines(linewidth=1.5)
#m.drawparallels(parallels)
#m.drawmeridians(meridians)
# add colorbar
cb = m.colorbar(CS2,"bottom", size="5%", pad="2%")
cb.set_label('hPa')
# set plot title
ax.set_title('SLP and Wind Vectors '+str(date))
plt.show()

# create 2nd figure, add axes
fig2 = plt.figure(figsize=(8,10))
ax = fig2.add_axes([0.1,0.1,0.8,0.8])
# plot SLP contours
CS1 = m.contour(x,y,clevs,linewidths=0.5,colors='k',animated=True)
CS2 = m.contourf(x,y,clevs,cmap=plt.cm.RdBu_r,animated=True)
# plot wind barbs over map.
barbs = m.barbs(xx,yy,uproj,vproj,length=5,barbcolor='k',flagcolor='r',linewidth=0.5)
# draw coastlines, parallels, meridians.
m.drawcoastlines(linewidth=1.5)
m.drawparallels(parallels)
m.drawmeridians(meridians)
# add colorbar
cb = m.colorbar(CS2,"bottom", size="5%", pad="2%")
cb.set_label('hPa')
# set plot title.
ax.set_title('SLP and Wind Barbs '+str(date))
plt.show()
