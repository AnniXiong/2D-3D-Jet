# this program is to plot the number of jets per event with the 15 different pairs of p and R
# Anni Xiong
#%matplotlib inline
import MC_pregraph3D_ as mp3
import MC_3d_saving_ as mcs
import antikt as ak
import matplotlib.pyplot as plt
import itertools 
import numpy as np
import random
c = ['g', 'b', 'r', 'c','y','k']
def pr_plotting(jetnumber,c):
    plt.style.use('seaborn-poster')
    fig = plt.figure()
    plt.axis([-0.2, 1.2, -1.2, 1.2])
    for k in jetnumber.keys():
        #k[p, r]
        x = k[1]
        y = k[0]
        number = jetnumber[k]
        colors = random.choice(c)
        plt.text(x, y, str(number) , color = colors  ,fontsize = '10')
    plt.xlabel('R value')
    plt.ylabel('p value')
    plt.title('Number of jets, Min_energy:'+ str(mp3.MinEnergy))
    plt.show()

def plot_single_event(angular_v, jet,c):
    fig,ax = plt.subplots(1,1)   
    fig.set_size_inches(11,8.5) 
    for v in jet: 
        length = len(v)
        area = []
        eta = []
        phi = []
        colors = random.choice(c)
        for i in v:
            i = i,
            area.append(angular_v[i][0])
            eta.append(angular_v[i][1])
            phi.append(angular_v[i][2])
        a = [x * 1000 for x in area]    
        plt.scatter(eta, phi,s = a,  color=colors, alpha=0.5)
    ax.set_aspect('auto')
    plt.xlabel('eta')
    plt.ylabel('phi')
    plt.title('Jet Distribution')
    plt.show()
    
# the part respnsible for the interactive mode
print('choose s to see jets from one event, choose m to see distribution of #jets')
print('from 15 different combinations of p and r')
print('(multiple pR:p = [-1,0,1],R = [0.01, 0.05, 0.1, 0.5, 1]')
a1 = str(input('single p_R pair or multiple p_R(s/m)?'))

if a1 == 'm':
    multiplepr_jets = {}
    jetnumber = {}
    p = [-1,0,1]
    R = [0.01, 0.05, 0.1, 0.5, 1]
    pR_pair = list(itertools.product(p,R))                    
    for i,pr in enumerate(pR_pair):
        p = pr[0]
        R = pr[1]
        final3 = mcs.final3
        t3 = mcs.t3
        
        jet = ak.main(p, R, final3, t3, mp3, mcs)   
        multiplepr_jets[i] = jet
        jetnumber[pr] = len(jet)
    print('multiple pr jets', multiplepr_jets)
    print('number of jets', jetnumber)
    pr_plotting(jetnumber, c)
elif a1 == 's':
    a1R = float(input("input the R value here:"))
    a1p = float(input('input the p value here:'))
    print('single pr jet')
    final3 = mcs.final3
    t3 = mcs.t3
    jet = ak.main(a1R, a1p, final3, t3, mp3, mcs) 
    print(jet)
    angular_v = ak.v_ang
    #plot_single_event(angular_v, jet,c)

