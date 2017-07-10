# Anni Xiong
#
#This program plots out the 2d version of the particle shower

import MC_pregraph2D_ as mp
import matplotlib.pyplot as plt
from matplotlib import collections as mc
import numpy as np
import pylab as pl
import collections

mpt = mp.Thetad  # the defledted angle information from MC_pregraph2D_.py
line_length = 1  # the length of the trajectory
Coordinate = {-1:[0,0]} # x and y coordinates of each particle without accumulation from the previous particle coordinates
Coordinate_list = [] # x and y coordinates including accumulation from prrevious particles

energy = mp.Zd

# calculate x and y corrdinate for each particle and put in a dictionary
for i, v in mpt.items():
	x = line_length * np.cos(v)
	y = line_length * np.sin(v)
	Coordinate[i] = [x,y]

Coordinate = collections.OrderedDict(sorted(Coordinate.items()))
print(Coordinate)

# find the parent particle for each one and generate the new coordinate to be plotted so to string everything together 
for i in Coordinate.keys():
	particle = Coordinate[i]
	#print(particle)
	if i == -1:
		parent_particle = [0, 0]
	elif i%2 == 0:
		parent_particle = Coordinate[(i-2)/2]
	else:
		parent_particle = Coordinate[(i-1)/2]
	
	particle_add = [(particle[0]+parent_particle[0]),(particle[1]+parent_particle[1])]
	Coordinate[i] = particle_add
	Coordinate_list.extend([parent_particle,particle_add])
	

column = (len(Coordinate_list))/2
#print('coordinate: ', Coordinate)
print ('Coordinate_list: ', Coordinate_list, 'len: ', column)

# Plotting part
cood= np.array(Coordinate_list)
coor_array= np.reshape(cood,(int(column),2,2))
print("** All final coordinates **\n", coor_array)
lc = mc.LineCollection(coor_array,colors='k',linewidths=0.5)
fig, ax = pl.subplots()
ax.add_collection(lc)
ax.autoscale()
plt.show()
