# -*- coding: utf-8 -*-
"""
Created on Fri Feb 09 10:21:14 2018

@author: jmo115
"""

from astropy.io import fits
from astropy.io import ascii
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

#import xlsxwriter

def circle(array, x,y,radius):
    cx, cy = x,y #
    y,x = np.ogrid[-radius: radius, -radius: radius]
    index = x**2 + y**2 <= radius**2
    return array[cy-radius:cy+radius, cx-radius:cx+radius][index]
    #array[cy-radius:cy+radius, cx-radius:cx+radius][index] =0
    
def resolve_galaxy(array, x,y,radius):
    cx, cy = x,y #
    y,x = np.ogrid[-radius: radius, -radius: radius]
    index = x**2 + y**2 <= radius**2
    array[cy-radius:cy+radius, cx-radius:cx+radius][index] = 0
    
def numberOfNonNans(data):
    count = 0
    for i in data:
        if not np.isnan(i):
            count += 1
    return count 
    
hdulist = fits.open("mosaic.fit")
header = hdulist[0].header
zeropoint=header['MAGZPT']

hdulist = fits.open('mosaic_masked7.fits')
data = hdulist[0].data
data1=data
#catalogue=np.array
catalogue=['x','y','r','size','maximum','background','flux','mag']
#catalogue=np.vstack((catalogue,cataloguetitle))

#data_nan=data
data=data.astype(float)
data[data==0]=np.nan
n=1
#for n in range(0,500):
while True:

    data1=data1.astype(float)
    data1[data1==0]=np.nan
    maximum=np.nanmax(data1)
    maxlocation_data=np.where(data1 == maximum)
    
    y0=maxlocation_data[0][0]
    x0=maxlocation_data[1][0]
    x=x0
    y=y0
    i=data[y0,x0]
   # print 'x,y=',x0,y0
    
    #galaxy=circle(data,x0,y0,6)
    minus_x=150
    plus_x=150
    minus_y=150
    plus_y=150
    if x0<150:
        minus_x=x0
    if x0>2420:
        plus_x=2570-x0
    if y0<150:
        minus_y=y0
    if y0>4460:
        plus_y=4610-y0
    
    background=np.nanmedian(data[y0-minus_y:y0+plus_y,x0-minus_x:x0+plus_x])
    diff=maximum-background
    #print diff
    #print background
    #print diff
    #print 'background=',background
    if diff<20:
        print 'x0=',x0,'y0=',y0,'max=',maximum
        break
    while (i > background and i != 'nan'):
        x+=1        
        i=data[y,x]
            
    r1=x
    
    x=x0
    y=y0   
    i=data[y,x]
    #print x,y
    while (i > background and i != 'nan'):
        y+=1        
        i=data[y,x]
    
    r2=y
    
    x=x0
    y=y0   
    i=data[y,x]
    
    while (i > background and i != 'nan'):
        x-=1
        i=data[y,x]

        
    r3=x
    
    x=x0
    y=y0   
    i=data[y,x]
    
    while (i > background and i != 'nan'):
        y-=1
        i=data[y,x]

    r4=y
    #radii=[r1-x0,r2-y0,x0-r3,y0-r4]
    
    r=np.median([r1-x0,r2-y0,x0-r3,y0-r4])
    r=np.floor(r)
    if (r <= 3):
        resolve_galaxy(data1,x0,y0,r)
    else:
        if r < 6 :
            r = 6
        elif r > 80 :
            r = 80
        #print 'radius=',r
        galaxy = circle(data1,x0,y0,r)
        #print galaxy
        
        #size=np.isnan(galaxy)[np.isnan(galaxy) == False].size
        size= numberOfNonNans(galaxy)
        flux = np.nansum(galaxy)-size*background
        #print 'flux=',flux
        m=zeropoint-2.5*np.log10(flux)
        #print 'mag=',m
        
        galaxy_row=[x0, y0, r, size, maximum, background, flux, m]    
        catalogue=np.vstack((catalogue, galaxy_row))
        
        resolve_galaxy(data1,x0,y0,r)
    #print '.'
    print n,diff,r
    n+=1

    
#print catalogue
#table={'x':catalogue[0],'y':catalogue[1],'r':catalogue[2],'size':catalogue[3],'maximum':catalogue[4],'background':catalogue[5],'flux':catalogue[6],'mag':catalogue[7]}
ascii.write(catalogue, 'galaxies_all_test1.dat', delimiter='\t' )


data[data==np.nan]=0
hdu = fits.PrimaryHDU(data1)
hdul = fits.HDUList([hdu])
hdul.writeto('all_galaxies_test_diff20.fits')    
hdulist.close()

