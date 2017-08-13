# Anni Xiong
#
#This program plots out the 2d version of the particle shower

import MC_pregraph2D_ as mp
import matplotlib.pyplot as plt
from matplotlib import collections as mc
import numpy as np
import pylab as pl

Minenergy = 0.01

mp.main(Minenergy)
mpt = mp.Thetad              # theta from mc_2d pregraph

line_length = 1              # decay length
Coordinate = {-1:[0,0]}      # x and y coordinates of each particle without accumulation from the previous ones
Coordinate_list = []         # x and y coordinates including accumulation from prrevious particles
energy = mp.Zd

# calculate x and y corrdinate for each particle and put in a dictionary
for i, v in mpt.items():
	x = line_length * np.cos(v)
	y = line_length * np.sin(v)
	Coordinate[i] = [x,y]

# find the parent particle for each one and generate the new coordinate
sorted_coordinate_key = sorted(list(Coordinate.keys()))
for i in sorted_coordinate_key:
	particle = Coordinate[i]
	if i == -1:
		parent_particle = [0, 0]
	elif i%2 == 0:
		parent_particle = Coordinate[(i-2)/2]
	else:
		parent_particle = Coordinate[(i-1)/2]
	
	particle_add = [(particle[0]+parent_particle[0]),(particle[1]+parent_particle[1])]
	Coordinate[i] = particle_add
	Coordinate_list.extend([parent_particle,particle_add])
	

# Plotting part
column = (len(Coordinate_list))/2
cood= np.array(Coordinate_list)
coor_array= np.reshape(cood,(int(column),2,2))
#print("** All final coordinates **\n", coor_array)
lc = mc.LineCollection(coor_array,colors='k',linewidths=0.5)
fig, ax = pl.subplots()
ax.add_collection(lc)
ax.set_title('2d parton shower' + ', energy threshold' + str(Minenergy))
ax.autoscale()
plt.show()
