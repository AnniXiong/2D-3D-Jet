# Anni Xiong
#
# This program gets information from two pregraph files, put them in tables then save into files
# the last row of final state particle is for checking the energy conservation

import MC_pregraph3D_ as mp3
from astropy.table import Table, Column, QTable
import numpy as np

# extracting data from 2 pregraghes
energy3d = mp3.Zd

min_energy3d = mp3.MinEnergy
angle3d = mp3.Thetad
momentum3d = mp3.momentum

#creating seperate lists for momentum by x, y, (z) components
final3 = []
nonfinal3_table_index = []

# 3d table data
ii = sorted(list(energy3d.keys()))
ee =[]
tt = []
pp = []
px3 = []
py3 = []
pz3 = []

for k in ii:
	m3 = momentum3d[k]
	angle = angle3d[k]
	ee.append(energy3d[k])
	
	tt.append(angle[0])
	pp.append(angle[1])
	
	px3.append(m3[0])
	py3.append(m3[1])
	pz3.append(m3[2])


# -----------------------------------------------------------------------------------------#

# 3D : particle data
t3 = QTable([ii, ee, tt, pp, px3 , py3, pz3], names=('index', 'energy', 'theta','phi','px','py','pz'), 
								dtype = ('i', 'f4', 'f8','f8','f8','f8','f8'))
t3.sort(['index'])
# table for all the particles
#t3.pprint(max_width = -1, max_lines = -1)

# writing the data file
datafile3 = open('data3d.txt','w')                                        
datafile3 .write('3d version\n' + 'MinEnergy  ' + str(min_energy3d) + '\n' + str(t3) + '\n' )

# picking out the particle and table index for final state particles in 3D case
for i, k in enumerate(t3['index']):
	k3 = (k*2) + 1
	if not k3 in energy3d:
		kk = k,
		final3.append(kk)
	else:
		nonfinal3_table_index.append(i)
final3.sort()
# 3D removing the rows that don't belong to final state particles
t3.remove_rows(nonfinal3_table_index)
#print('nonfinal3_table_index', nonfinal3_table_index)

t3.add_row([0, t3['energy'].sum(), 0 ,0 , t3['px'].sum(), t3['py'].sum(), t3['pz'].sum()])
datafile3 .write('final state particle index' + str(final3) + '\n' + str(t3))
datafile3 .close()
#table of only the final state particles
#t3.pprint(max_width = -1, max_lines = -1)

#print(final3)
#print(type(final3[10]))
								