##########################################################################
#########                  PART 1: Utility functions             #########
#########                      Question 1                        #########
#########           NAME: Edson Nkonde  StudentID: 21810910      #########
##########################################################################
""" This module contains code for reading data from NetCDF files and
    intepreting metadata """
  
#Question 1.1
def findNearestLatIndex(nc,dataVar,latVal):
    """ Searches through latitude values for the target value,using the findLatitudeVar() in 
    netcdfUtils module and the findNearestIndex() function from the utils module, returning
    the index of the latitude value that is closest numerically to the target value. If more
    than one latitude value is equally close to the target, the index of the first value will
    be returned. If the Latitude dimension does not exit a error is raised """
    import utils
    #check if the latitude value is within the latitude range
    if latVal>90 or latVal<-90:
        raise ValueError("The value entered is ouside latitude range of values +90 to -90")
    # check if the Variable object representing the latitude axis exists in the netcdf file
    coordVar=findLatitudeVar(nc,dataVar)#returns Variable object representing latitude axis for the data variable
    if coordVar is None:
        raise ValueError("No Variable object for the latitude axis exists in the netcdf file")
    else:
    #get an array of latitude values from where to search for the given latitude value   
        latVals=coordVar[:] 
    #find the index of the given latitude value
    latIndex=utils.findNearestIndex(latVals,latVal) 
    return latIndex #latitude index value
    
#Question 1.2
def findNearestZIndex(nc,dataVar,zVal): 
    """ Searches through vertical axis values for the target value,using the findVerticalVar() 
    in netcdfUtils module and the findNearestIndex() function from the utils module, returning 
    the index of the vertical axis value that is closest numerically to the target value. If 
    more than one latitude value is equally close to the target, the index of the first value 
    will be returned.If the vertical dimension does not exit an error is raised """
    import utils  
    # check if the Variable object representing the vertical axis exists in the netcdf file
    coordVal=findVerticalVar(nc,dataVar)#returns Variable object representing vertical axis for the data variable
    if coordVal is None:
        raise ValueError("No Variable object for the vertical axis exists in the netcdf file")
    else:
    #get an array of vertical values from where to search for the given vertical value  
        zVals=coordVal[:]
    #check if the vertical value given is within the vertical axis range of values    
    if zVal<zVals[0] or zVal>max(zVals):
      raise ValueError("The value entered is ouside vertical coordinate range of values")
   #find the index of the given vertical axis value
    zIndex=utils.findNearestIndex(zVals,zVal)
    #return the index of the vertical value
    return zIndex    
    
#Question 1.4
def findNearestLonIndex(nc,dataVar,lonval):
    """ Searches through longitude values for the target value, returning the index
    of the longitude value that is closest numerically to the target value.
    If more than one longitude value is equally close to the target, the index
    of the first value will be returned. """
    import utils
    import netcdfUtils
    # map the longitutude value from range (-180 to 180) onto (0 to 360) in the data file
    coordval=netcdfUtils.findLongitudeVar(nc,dataVar)
    if min(coordval[:])>=0:
        #check if the latitude value is within the latitude range
       if lonval<=0:
           lonval=lonval+180
       else:
           lonval=lonval+180  
    # check if the Variable object representing the latitude axis exists in the netcdf file  
    if coordval is None:
        raise ValueError("No Variable object for the longitude axis exists in the netcdf file")
    #create an array of longitude values from where to search
    lonvals=coordval[:]
    #find the index of the given longitudevalue and check if it exists
    lonIndex=utils.findNearestIndex(lonvals,lonval) 
    #if no index is found
    if lonIndex is None:
        raise ValueError("No index value found for the longitude value entered")
    #longitude index value   
    return lonIndex 
    
#######################################################################################
#######################################################################################
#######################################################################################    
          
def getAttribute(var, attName, default=None):
    """ Gets the value of the given attribute as a string.  Returns the
    given default if the attribute is not defined. This is a useful
    "helper" method, which avoids AttributeErrors being raised if the
    attribute isn't defined.  If no default is specified, this function
    returns None if the attribute is not found. """
    if attName in var.ncattrs():
        return var.getncattr(attName)
    else:
        return default

def getTitle(var):
    """ Returns a title for a variable in the form "name (units)"
    The name is taken from the standard_name if it is provided, but
    if it is not provided, it is taken from the id of the variable
    (i.e. var._name).  If the units are not provided, the string
    "no units" is used instead. """
    standardName = getAttribute(var, 'standard_name', var._name)
    units        = getAttribute(var, 'units',         'no units')
    return "%s (%s)" % (standardName, units)

#######################################################################################
#####  The following functions test to see if coordinate variables represent geographic
#####  or time axes
#######################################################################################

def isLongitudeVar(coordVar):
    """ Given a coordinate variable (i.e. a NetCDF Variable object), this returns
    True if the variable holds values of longitude, False otherwise """
    # In the Climate and Forecast conventions, longitude variables are indicated
    # by their units (not by their names)
    units = getAttribute(coordVar, 'units')
    # There are many possible options for valid longitude units
    if units in ['degrees_east', 'degree_east', 'degree_E', 'degrees_E', 'degreeE', 'degreesE']:
        return True
    else:
        return False
    
def isLatitudeVar(coordVar):
    """ Given a coordinate variable (i.e. a NetCDF Variable object), this returns
    True if the variable holds values of latitude, False otherwise """
    # In the Climate and Forecast conventions, latitude variables are indicated
    # by their units (not by their names)
    units = getAttribute(coordVar, 'units')
    # There are many possible options for valid latitude units
    if units in ['degrees_north', 'degree_north', 'degree_N', 'degrees_N', 'degreeN', 'degreesN']:
        return True
    else:
        return False
    
def isVerticalVar(coordVar):
    """ Given a coordinate variable (i.e. a NetCDF Variable object), this returns
    True if the variable represents a vertical coordinate, False otherwise """
    # In the Climate and Forecast conventions, vertical coordinates are indicated
    # by units of pressure, or by the presence of a "positive" attribute.
    units = getAttribute(coordVar, "units")
    # First we look for units of pressure.  (There may be more possible pressure units
    # than are used here.)
    if units in ['Pa', 'hPa', 'pascal', 'Pascal']:
        return True
    else:
        # We don't have units of pressure, but perhaps we have a "positive" attribute
        positive = getAttribute(coordVar, 'positive')
        if positive in ['up', 'down']:
            return True
            
    # If we've got this far, we haven't satisfied either of the conditions for a
    # valid vertical axis
    return False
    
def isTimeVar(coordVar):
    """ Given a coordinate variable (i.e. a NetCDF Variable object), this returns
    True if the variable represents a time coordinate, False otherwise """
    # In the Climate and Forecast conventions, time coordinates are indicated
    # by units that conform to the pattern "X since Y", e.g. "days since 1970-1-1 0:0:0".
    # For simplicity, we just look for the word "since" in the units.  A complete
    # implementation should check this more thoroughly.
    units = getAttribute(coordVar, 'units')
    if units is None:
        # There are no units, so this can't be a time coordinate variable
        return False
    # The "find()" function on strings returns the index of the first match of the given
    # pattern.  If no match is found, find() returns -1.
    if units.find("since") >= 0:
        return True
    else:
        return False


#######################################################################################
#####  The following functions find geographic and time coordinate axes
#####  for data variables.
#######################################################################################

# As you can see, there is a lot of repetition in these functions - they all do basically
# the same thing.  There is a way to avoid this repetition, but it involves a technique
# that you may not be familiar with (i.e. passing functions as arguments to other functions)
# - see me if you want to know more.
    
def findLongitudeVar(nc, dataVar):
    """ Given a NetCDF Dataset object and a Variable object representing a data
    variable, this function finds and returns the Variable object representing the
    longitude axis for the data variable.  If no longitude axis is found, this returns
    None. """
    # First we iterate over the dimensions of the data variable
    for dim in dataVar.dimensions:
        # We get the coordinate variable that holds the values for this dimension
        coordVar = nc.variables[dim]
        # We test to see if this is a longitude variable, if so we return it
        if isLongitudeVar(coordVar):
            return coordVar
    # If we get this far we have not found the required coordinate variable
    return None

def findLatitudeVar(nc, dataVar):
    """ Given a NetCDF Dataset object and a Variable object representing a data
    variable, this function finds and returns the Variable object representing the
    latitude axis for the data variable.  If no latitude axis is found, this returns
    None. """
    for dim in dataVar.dimensions:
        coordVar = nc.variables[dim]
        if isLatitudeVar(coordVar):
            return coordVar
    return None

def findVerticalVar(nc, dataVar):
    """ Given a NetCDF Dataset object and a Variable object representing a data
    variable, this function finds and returns the Variable object representing the
    vertical axis for the data variable.  If no vertical axis is found, this returns
    None. """
    for dim in dataVar.dimensions:
        coordVar = nc.variables[dim]
        if isVerticalVar(coordVar):
            return coordVar
    return None

def findTimeVar(nc, dataVar):
    """ Given a NetCDF Dataset object and a Variable object representing a data
    variable, this function finds and returns the Variable object representing the
    time axis for the data variable.  If no time axis is found, this returns
    None. """
    for dim in dataVar.dimensions:
        coordVar = nc.variables[dim]
        if isTimeVar(coordVar):
            return coordVar
    return None

def isPositiveUp(zVar):
    """ Given a vertical coordinate variable, this function returns true if the
    values on the vertical axis increase upwards. For vertical axes based on pressure,
    the values increase downward, so this returns False.  If the axis is not based
    on pressure, the value of the "positive" attribute (which can be "up" or "down")
    is used instead. """
    units = getAttribute(zVar, "units")
    # First we look for units of pressure.  (If we find them, this is a pressure axis
    # and the values increase downward)
    if units in ['Pa', 'hPa', 'pascal', 'Pascal']:
        return False
    else:
        # We don't have units of pressure, but perhaps we have a "positive" attribute
        positive = getAttribute(zVar, 'positive')
        if positive == 'up':
            return True
        else:
            return False











