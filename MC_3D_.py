# Anni Xiong
#
# This program plot out the 3d version of the particle shower

import MC_pregraph3D_ as mp
import matplotlib.pyplot as plt
from matplotlib import collections as mc
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import collections
from mpl_toolkits.mplot3d.art3d import Line3DCollection

energy = mp.Zd # the total energy generated
mpt = mp.Thetad # angle of every particle
line_length = 1.0 # length of trajectory
Coordinate = {-1:[0,0,0]} # coordinate of each particle without accounting for accumulation from previous particles
Coordinate_list = []  # coordinates accounting for accumulations
width = [0]  # the line width in order to vary the line width along decaying process

# calculate x and y corrdinate for each particle assuming a fixed trajectory length and put in a dictionary
for i, v in mpt.items():
	# v has two elements here the first theta, the second phi
	z = line_length * np.sin(v[0]) * np.cos(v[1])
	y = line_length * np.sin(v[0]) * np.sin(v[1])
	x = line_length * np.cos(v[0])
	Coordinate[i] = [x,y,z]
Coordinate = collections.OrderedDict(sorted(Coordinate.items()))

# find the parent particle for each one and generate the new coordinate to be plotted so to string 
# everything together 
for i in Coordinate.keys():
	particle = Coordinate[i]
	#print(particle)
	if i == -1:
		parent_particle = [0, 0, 0]
	elif i%2 == 0:
		parent_particle = Coordinate[(i-2)/2]
	else:
		parent_particle = Coordinate[(i-1)/2]
	
	particle_add = [(particle[0]+parent_particle[0]),(particle[1]+parent_particle[1]),(particle[2]+parent_particle[2])]
	Coordinate[i] = particle_add
	Coordinate_list.extend([parent_particle,particle_add])
	
# varying the line width according to the total energy of very particle
energy = collections.OrderedDict(sorted(energy.items())) # the total energy generated
for w in energy.values():
	W = w * 4
	width.append(W)
print('width', width)
column = (len(Coordinate_list))/2


#arranging the coordinates into the column * 2 * 3 array so it can be used in line collection plotting
cood= np.array(Coordinate_list)
coor_array= np.reshape(cood,(int(column),2,3))

print("** All final coordinates **\n" , coor_array)

# plotting the arranged array 
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.add_collection3d(Line3DCollection(coor_array, colors='k', linewidths=width))
ax.autoscale()
ax.set_xlim(-2, 8)
ax.set_ylim(-5, 5)
ax.set_zlim(-5, 5)
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')
ax.set_aspect('auto')
plt.show()
