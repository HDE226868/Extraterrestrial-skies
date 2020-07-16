#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

#Coordinates of planet
shift_ra = 0
shift_dec = 0
shift_dist = 10

ralist = []
declist = []

idlist = []
new_ralist = []
new_declist = []
new_distlist = []
new_maglist = []

#Data from the Hipparcos, Yale Bright Star and Gliese catalogs
data = open('hygdata_v3.csv', 'r').readlines()

for i in range(1, len(data)):
    #Basic proprties of stars
    line = data[i].split(',')
    id = line[0]
    hip = line[1]
    ra = float(line[7])
    dec = float(line[8])
    dist = float(line[9])
    absmag = float(line[14])
        
    #Convert to radians
    ra = (2*np.pi/24) * ra
    dec = (2*np.pi/360)* dec
    
    #Spherical to Cartesian
    x = dist*np.cos(dec)*np.cos(ra)
    y = dist*np.cos(dec)*np.sin(ra)
    z = dist*np.sin(dec)
       
    #Coordinates of target exoplanet       
    x_shift = shift_dist*np.cos(shift_dec)*np.cos(shift_ra)
    y_shift = shift_dist*np.cos(shift_dec)*np.sin(shift_ra)
    z_shift = shift_dist*np.sin(shift_dec)
     
    #Shifts coordinates based on exoplanet     
    new_x = x + x_shift
    new_y = y + y_shift
    new_z = z + z_shift
    
    #Cartesian to spherical   
    new_dist = np.sqrt((x - x_shift)**2 + (y - y_shift)**2 + (z - z_shift)**2)
    new_ra = np.arctan(new_y/new_x)
    new_dec = np.arcsin(new_z/new_dist)
    
    #Some fiddly bits to display nicely
    new_ra = 2 * (360/(2*np.pi)) * new_ra + 180
    new_dec = (360/(2*np.pi)) * new_dec

    new_ra = new_ra - 270
    if new_ra < 0:
        new_ra = new_ra + 360
    
    if new_dist != 0:
        #Size of star is related to apparent magnitude    
        appmag = absmag + 5*(np.log10(new_dist) - 1)
        lum = 50 * 10**(-appmag/1.5)

        idlist.append(id)
        new_ralist.append(new_ra)
        new_declist.append(new_dec)
        new_distlist.append(new_dist)
        new_maglist.append(lum)

fig = plt.figure(1)
ax = fig.add_subplot(111, facecolor='black')
ax.scatter(new_ralist, new_declist, s=new_maglist, color='white')
#Adjust the limits as needed
ax.set_xlim([65, 90])
ax.set_ylim([-15, 20])
ax.set_xlabel('Declination (degrees)')
ax.set_ylabel('Right ascension (degrees)')
ax.invert_xaxis()
ax.set_aspect('equal', adjustable='box')
plt.show()
        
