""" Useful helper methods and utility functions """

def findNearestIndex(vals, target):
    """ Searches through vals for the target value, returning the index
    of the value in vals that is closest numerically to the target value.
    If more than one value in vals is equally close to the target, the index
    of the first value will be returned. """
    minIndex = -1
    minDiff = None
    # Loop over all the values in the given list
    for i in range(len(vals)):
        # Find the absolute difference between this value and the target
        diff = abs(vals[i] - target)
        # If this is the first time, or if the difference is smaller than
        # the smallest difference found so far, remember the difference and
        # the index
        if minDiff is None or diff < minDiff:
            minDiff = diff
            minIndex = i
    return minIndex
    
### Test functions for findNearestIndex
### Simply run this script to run the tests
### Note that these tests are very basic.  A full set of tests would be much
### longer and more comprehensive!
if __name__ == '__main__':
    arr = range(0,100) # creates a set of values from 0 to 99 inclusive
    ni = findNearestIndex(arr, -0.1)
    print "ni = %s, should be 0" % ni
    ni = findNearestIndex(arr, 0.1)
    print "ni = %s, should be 0" % ni
    ni = findNearestIndex(arr, 23.1)
    print "ni = %s, should be 23" % ni
    ni = findNearestIndex(arr, 23.8)
    print "ni = %s, should be 24" % ni
    ni = findNearestIndex(arr, 98.9)
    print "ni = %s, should be 99" % ni
    ni = findNearestIndex(arr, 100)
    print "ni = %s, should be 99" % ni