# -*- coding: utf-8 -*-
"""
Created on Fri Feb 09 10:21:14 2018

@author: jmo115
"""

from astropy.io import fits
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

def circle(array, x,y,radius):
    cx, cy = x,y #
    y,x = np.ogrid[-radius: radius, -radius: radius]
    index = x**2 + y**2 <= radius**2
    return array[cy-radius:cy+radius, cx-radius:cx+radius][index]
    #array[cy-radius:cy+radius, cx-radius:cx+radius][index] =0
    
hdulist = fits.open('mosaic_masked6.fits')

header = hdulist[0].header


data = hdulist[0].data


sector = data[852:1022,612:783]

#data1=data[100:200,150:250]
#plt.hist(np.ndarray.flatten(sector),bins=range(3330, 3600))
#plt.show()
data_nan=data
data_nan=data_nan.astype(float)
data_nan[data_nan==0]='nan'

print(np.where(sector == sector.max()))
print(sector[38,131])
maxlocation=[38,131]
maxlocation_data=[890,743]
background=np.nanmedian(data[890-50:890+50,743-50:743+50])
print(background)

x0=maxlocation_data[0]
y0=maxlocation_data[1]
x=x0
y=y0
i=data[x0,y0]

galaxy=circle(data,y0,x0,6)
print(galaxy)
print len(galaxy)
flux = sum(galaxy)-111*background
print flux

aperature=6
background_aperature=12
whole=circle(data,x0,y0,background_aperature)
background=(sum(whole)-sum(galaxy)/(len(whole)-len(galaxy))

"""
while i > background:
    i=data[x,y]
    x+=1

r1=x
i=data[x0,y0] 
x=x0
y=y0   

while i > background:
    i=data[x,y]
    y+=1
r2=y

r=max(r1-x0,r2-y0)
print(r)
galaxy = circle(data,x0,y0,r)
print galaxy
"""

hdulist.close()