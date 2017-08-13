# pseudo-mass = E(j1)*E(j2)*deltaR(j1,j2)
# j1 and j2 ---> two highest pt constituents
# to calculate the jet observable and plot the distribution of it using many parton shower events
# Anni Xiong
#import MC_pregraph3D_ as mp3
import MC_3d_saving_ as mcs
import MC_pregraph3D_ as mp3
import antikt as ak
from ROOT import TLorentzVector
import importlib as imp
import matplotlib.pyplot as plt
import numpy as np

events = 100
p = -1
R = 1

'''calculating the pseudo mass for one event'''
def pseudo_mass(v,jets,pt):
    jet_v = {}  #{jetn(c1,c2,c3,...):  sum of v's}
    jet_E = {}  #{jetn(c1,c2,c3,...):  jetEn}
    for i in jets:
        jet_vv = TLorentzVector()
        for c in i:
            c = c,
            jet_vv += v[c]
        jet_v[i] = jet_vv
        jet_E[i] = jet_vv[3] # to get the energy
    max_energy = max(list(jet_E.values()))
    revE = {v:k for k,v in jet_E.items()}  # {jetEn: jet}
    # pick out the jet with the largest energy
    max_index = revE[max_energy] 
    if len(max_index) == 1:
        pse_mass = np.nan
    else:
        const_pt = {k:pt[k,] for k in max_index}
        sorted_pt = sorted(list(const_pt.values()), reverse = True)
        rev_const_pt = {pt[k,]:k for k in max_index}
        j1 = rev_const_pt[sorted_pt[0]]  
        j2 = rev_const_pt[sorted_pt[1]]
        deltar = v[j1,].DeltaR(v[j2,])
        pse_mass = v[j1,][3] * v[j2,][3] * deltar   
    return pse_mass

def distribution_plot(events, p, R):
    m = []
    for i in range(events):
        
        final3 = mcs.final3
        t3 = mcs.t3
        jets= ak.main(p, R, final3, t3, mp3, mcs)
        pt = ak.pt
        v = ak.v
        mass = pseudo_mass(v, jets, pt)
        m.append(mass)
    m = np.asarray(m)
    xnan = m[~np.isnan(m)]
    return xnan
    print('pseudo mass',m)


# plotting the pseudo mass distribution by reloading the data each time
fig, ax = plt.subplots()
fig.set_size_inches(11,8.5) 
xnan = distribution_plot(events, p, R)
minE = mcs.Minenergy
bin_max = max(xnan)
bin_min = min(xnan)
bins = np.linspace(bin_min, bin_max, 20)
plt.style.use('classic')
ax.hist(xnan, bins ,color='blue', alpha=0.8, histtype='step', label = 'min_E ='+ str(minE) +', '+str(events)+' events')
ax.legend(loc='upper right')
ax.set_xlabel('Pseudo mass')
ax.set_title('Pseudo mass distribution')
fig.tight_layout()
#plt.show()
plt.savefig('Pseudo_mass_distribution.png')

