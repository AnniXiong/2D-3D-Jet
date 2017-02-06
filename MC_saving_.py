# Anni Xiong
#
# This program gets information from two pregraph files, put them in tables then save into files

import MC_pregraph2D as mp2
import MC_pregraph3D as mp3
from astropy.table import Table, Column, QTable
import numpy as np

# extracting data from 2 pregraghes
energy = mp2.Zd
energy3d = mp3.Zd

angle = mp2.Thetad
angle3d = mp3.Thetad

momentum = mp2.momentum
momentum3d = mp3.momentum

#creating seperate lists for momentum by x, y, (z) components
px = []
py = []

px3 = []
py3 = []
pz3 = []

# filling the momentum lists by components
for v in momentum.values():
	px.append(v[0])
	py.append(v[1])

for v3 in momentum3d.values():
	px3.append(v3[0])
	py3.append(v3[1])
	pz3.append(v3[2])

'''print('x-component3', px3)
print('y-component3', py3)
print('z-component3', pz3)
'''
i = list(energy.keys())
e = list(energy.values())
t = list(angle.values())

ii = list(energy3d.keys())
ee = list(energy3d.values())
tt = list(angle3d.values())

# constructing the table which includes information about energy and momentum of each particle
t2 = QTable([i, e, t, px , py], names=('index', 'energy', 'angle','px','py'), 
								dtype = ('S1', 'f4', 'f4','f4','f4'))
t3 = QTable([ii, ee, tt, px3 , py3, pz3], names=('index', 'energy', 'angle','px','py','pz'), 
										   dtype = ('S1', 'f4', 'f4','f4','f4','f4'))

'''print(t2)
print(t3)'''

# write the two tables into two newly created (in the current directory) files 
fileObject2 = open('data2.txt','w')                                        
fileObject2.write('2d version\n')
fileObject2.write(str(t2))
fileObject2.close()

fileObject3 = open('data3d.txt','w')                                        
fileObject3.write('3d version\n')
fileObject3.write(str(t3))
fileObject3.close()

