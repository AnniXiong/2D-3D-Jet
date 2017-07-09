import MC_pregraph2D_ as mp2
from astropy.table import Table, Column, QTable
import numpy as np

energy = mp2.Zd
min_energy2d = mp2.MinEnergy
angle = mp2.Thetad
momentum2d = mp2.momentum

final = []
nonfinal_table_index = []

# 2d table data
i = sorted(list(energy.keys()))
e = []
t = []
px = []
py = []

for k in i:
	m = momentum2d[k]
	e.append(energy[k])
	t.append(angle[k])
	px.append(m[0])
	py.append(m[1])

# constructing the tables which include information of energy and momentum of each particle
# the data(except for index number) is rounded to be 32 bits of floating number(f4)
# 'i 'means integer
t2 = QTable([i, e, t, px , py], names=('index', 'energy', 'angle','px','py'), 
								dtype = ('i', 'f8', 'f8','f8','f8'))
t2.sort(['index'])
# table for the full length 2d data
#t2.pprint(max_width = -1, max_lines = -1)
datafile2 = open('data2d.txt','w')                                        
datafile2.write('2d version\n' + 'MinEnergy  ' + str(min_energy2d) + '\n' + str(t2) + '\n')

# 2D : picking out the particle and table index for final state particles in 2D case
for i , k in enumerate(t2['index']):
	k2 = (k*2) + 1 
	if not k2 in energy:
		final.append(k)
	else:
		nonfinal_table_index.append(i)
final.sort()
# 2D : removing the rows that don't belong to final state particles
t2.remove_rows(nonfinal_table_index)
t2.add_row([0, t2['energy'].sum(), 0 , t2['px'].sum(), t2['py'].sum()])
datafile2.write ('final state particle index' + str(final) + '\n' + str(t2))

datafile2.close()
# table for only the final state particle
#t2.pprint(max_width = -1, max_lines = -1)