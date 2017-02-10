# Anni Xiong
#
# This program gets information from two pregraph files, put them in tables then save into files
# the last row of final state particle is for checking the energy conservation

import MC_pregraph2D_ as mp2
import MC_pregraph3D_ as mp3
from astropy.table import Table, Column, QTable
import numpy as np

# extracting data from 2 pregraghes
energy = mp2.Zd
energy3d = mp3.Zd

min_energy2d = mp2.MinEnergy
min_energy3d = mp3.MinEnergy


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

final = []
final3 = []

nonfinal_table_index = []
nonfinal3_table_index = []

# filling the momentum lists by components
for v2 in momentum.values():
	px.append(v2[0])
	py.append(v2[1])

for v3 in momentum3d.values():
	px3.append(v3[0])
	py3.append(v3[1])
	pz3.append(v3[2])

i = list(energy.keys())
e = list(energy.values())
t = list(angle.values())

ii = list(energy3d.keys())
ee = list(energy3d.values())
tt = list(angle3d.values())

# constructing the tables which include information of energy and momentum of each particle
# the data(except for index number) is rounded to be 32 bits of floating number(f4)
# 'i 'means integer
t2 = QTable([i, e, t, px , py], names=('index', 'energy', 'angle','px','py'), 
								dtype = ('i', 'f4', 'f4','f4','f4'))
t2.sort(['index'])
t2.pprint(max_width = -1, max_lines = -1)
datafile2 = open('data2d.txt','w')                                        
datafile2.write('2d version\n' + 'MinEnergy  ' + str(min_energy2d) + '\n' + str(t2) + '\n')

# 2D : picking out the particle and table index for final state particles in 2D case
for i , k in enumerate(t2['index']):
	k2 = (k*2) + 1 
	if not k2 in energy:
		final.append(k)
	else:
		nonfinal_table_index.append(i)
# 2D : removing the rows that don't belong to final state particles
t2.remove_rows(nonfinal_table_index)
t2.add_row([0, t2['energy'].sum(), 0 , t2['px'].sum(), t2['py'].sum()])
datafile2.write ('final state particle index' + str(final) + '\n' + str(t2))

datafile2.close()
print (t2)

# -----------------------------------------------------------------------------------------#

# 3D : particle data
t3 = QTable([ii, ee, tt, px3 , py3, pz3], names=('index', 'energy', 'angle','px','py','pz'), 
								dtype = ('i', 'f4', 'f4','f4','f4','f4'))
t3.sort(['index'])
t3.pprint(max_width = -1, max_lines = -1)
datafile3 = open('data3d.txt','w')                                        
datafile3 .write('3d version\n' + 'MinEnergy  ' + str(min_energy3d) + '\n' + str(t3) + '\n' )

# picking out the particle and table index for final state particles in 3D case
for i, k in enumerate(t3['index']):
	k3 = (k*2) + 1
	if not k3 in energy3d:
		final3.append(k)
	else:
		nonfinal3_table_index.append(i)
# 3D removing the rows that don't belong to final state particles
t3.remove_rows(nonfinal3_table_index)
t3.add_row([0, t3['energy'].sum(), 0 , t3['px'].sum(), t3['py'].sum(), t3['pz'].sum()])
datafile3 .write('final state particle index' + str(final3) + '\n' + str(t3))
datafile3 .close()
print(t3)
								