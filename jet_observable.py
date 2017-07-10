# pseudo-mass = E(j1)*E(j2)*deltaR(j1,j2)
# this program is to calculate the jet observable and plot the distribution of it using many parton shower events
import MC_pregraph3D_ as mp3
import MC_3d_saving_ as mcs
import antikt as ak
from ROOT import TLorentzVector
import importlib as imp
import matplotlib.pyplot as plt

events = 100
p = -1
R = 1
'''calculating the pseudo mass for one event'''
def pseudo_mass(v,jets):
    jet_v = {}
    jet_E = {}
    for i in jets:
        jet_vv = TLorentzVector()
        for e in i:
            e = e,
            jet_vv += v[e]
        jet_v[i] = jet_vv
        jet_E[i] = jet_vv[3] # to get the energy
    #print(jet_v)
    max_energy = max(list(jet_E.values()))
    revE = {v:k for k,v in jet_E.items()}
    max_index = revE[max_energy]  
    const_energy = {}
    for k in max_index:
        k = k,
        const_energy[k] = v[k].E()
    s = sorted(list(const_energy.values()), reverse = True)
    revE = {v:k for k,v in const_energy.items()}
    deltar = v[revE[s[0]]].DeltaR(v[revE[s[1]]])
    pse_mass = s[0] * s[1] * deltar   # s[0] = Eji, s[1] = Ej2
    return pse_mass


# plotting the pseudo mass distribution by reloading the data each time
m = []
for i in range(events):
    final3 = mcs.final3
    t3 = mcs.t3
    v = ak.v
    jets = ak.main(p, R, final3, t3, mp3, mcs)
    print('jets',jets)
    mass = pseudo_mass(v, jets)
    m.append(mass)
print('pseudo mass',m)
num_bins = 50
fig,ax = plt.subplots(1,1) 
fig.set_size_inches(11,8.5) 
n, bins, patches = plt.hist(m, num_bins, facecolor='blue', alpha=0.5, histtype='step')
plt.xlabel('Pseudo mass')
plt.title('Distribution of Pseudo mass from parton showers, min E:'+ str(mp3.MinEnergy))
#plt.show()
plt.savefig('Pseudo_mass_distribution.png')

