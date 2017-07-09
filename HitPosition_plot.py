# This programm should calculate the positions of the final state particles that hit on the screen
%matplotlib inline
import MC_pregraph3D_ as mp3
from MC_3d_saving_ import final3,t3
import matplotlib.pyplot as plt
import numpy as np
from astropy.table import Table, Column, QTable

plt.style.use('ggplot')
#print(t3)
t3.show_in_notebook()
#set the screen position
L = 5

#Calculate the position of the hitting point using a 2D screen
screen_hit = {}
x_pos = []
y_pos = []

for i,k in enumerate(final3):
    x = L * np.tan(t3[i]['phi'])
    x_pos.append(x)
    y = L * np.tan(t3[i]['theta'])
    y_pos.append(y)
    coor = [x,y]
    screen_hit[k] = coor

#Making the table that contains position information
position = QTable([final3, x_pos, y_pos], names=('index', 'x position','y position'), 
       dtype = ('i', 'f4', 'f4'))
print(position)  
    
#Plotting the distribution out (taking the position of the first particle as the origin)
fig,ax = plt.subplots(1,1)                   
fig.set_size_inches(11,8.5)                  
ax.plot(x_pos, y_pos, marker="o",color="b",linestyle="None",markersize=5)
ax.vlines(0, -10, 10, color='r', linewidth=2)                    
ax.hlines(0, -50, 50, color='r', linewidth=2) 
fig.tight_layout() 
print ('screen_hit',screen_hit)

