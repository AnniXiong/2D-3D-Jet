# This program is to run the anti Kt algorithum, the goal is to get a list of jets
# the beam direction is in Z
# Anni Xiong
import MC_pregraph3D_ as mp3
import MC_3d_saving_ as mcs
import numpy as np
from ROOT import TLorentzVector
import itertools 
import importlib as imp # import the little monster

v = {}
v_ang = {}
pt = {}
def main(p, R, final3, t3, mp3, mcs):
    
    global v
    global v_ang
    global pt
    pt = {}
    packing(final3,t3,v, pt,v_ang)
    
    jets = []
    temp_entity = final3.copy()     #  making a copy so that 
    temp_v = v.copy()               # final3, v and pt are not
    temp_pt = pt.copy()             # modified along the way
    dij = {}                        # These two will be constantly updated,
    dib = {}                        # as entities are being merged to a jet
    
    di_B(temp_entity,p,pt,dib)      # calculate the diB's for the initial pool
    d_calculation(dij, temp_entity, dib, temp_v,R)  # calculate the ds for initial pool
    
    while 1:
        if not temp_entity:
            break
        decision = deci(dib, dij)
        i = decision[1]
        if decision[0]== 1:
            merging(i, temp_v, temp_entity, temp_pt,dib,p)
            dij = {}
            d_calculation(dij, temp_entity , dib, temp_v,R)
        elif decision[0] == 0:
            handle_jet(i, temp_v, temp_entity, temp_pt,dib, jets,dij)
        #print('d-calculation on each end of a run',dij)
        #print('dib on each end of a run',dib)
    imp.reload(mp3)
    imp.reload(mcs)
    #print('final state particle indices', final3)
    #print('jets',jets,'pr',p,R)
    return jets

'''packing initial data to TLorentz vectors'''
def packing (final3, t3, v, pt, v_ang):
    for i,k in enumerate(final3):
        v[k] = TLorentzVector()
        v[k].SetPxPyPzE(t3[i]['px'],t3[i]['py'],t3[i]['pz'],t3[i]['energy'])
        pt[k] = v[k].Perp()
        eta = v[k].Eta()
        v_ang[k] = TLorentzVector()
        v_ang[k].SetPtEtaPhiM(pt[k],eta,t3[i]['phi'],0.1)
        
""" calculate a dictionary containing the kt^2p for each final state particle """
# dib = {final state particles:  Kti^2p}
def di_B (temp_entity,p,pt,dib):
        for i in temp_entity:
            kti2p = (pt[i])**(2*p)
            dib[i] = kti2p

""" calculate the dij for every possible pair of final state particles """
def d_calculation(dij ,temp_entity, dib, temp_v,R):
    pair_list = list(itertools.combinations(temp_entity,2))
    for p in pair_list:
        p1 = p[0] 
        p2 = p[1]
        kti2p_pair = [dib[p1],dib[p2]]
        m = min(kti2p_pair)
        Delta_r = temp_v[p1].DeltaR(temp_v[p2])
        d = m*((Delta_r)**2)/(R**2)
        dij[p] = d
    
""" find the smallest among d's and return the index"""
def deci(dib, dij):
    dec = []  
    pool = list(dib.values()) + list(dij.values())
    smallestd = min (pool)
    if smallestd in list(dij.values()):
        dec.append(1)
        #to reverse the position of keys and values
        revD = {v:k for k,v in dij.items()}
        # to get the key
        dec.append(revD[smallestd])
    elif smallestd in list(dib.values()):
        dec.append(0) 
        revdB = {v:k for k,v in dib.items()}
        dec.append(revdB[smallestd])
        # dec = [0/1, index for the smallest d]
    return dec

''' update information about lorentz vectors, handle the merging case  '''
def merging(i, temp_v, temp_entity, temp_pt, dib, p):  
        index1 = i[0]                           # these are the
        index2 = i[1]                           # two indices to merge
        v_new = temp_v[index1] + temp_v[index2]     # the new four vector
        # merge the two indices, both tuples
        new_index = index1 + index2
        temp_v[new_index] = v_new
        temp_pt[new_index] = v_new.Perp()
        temp_entity.append(new_index)
        dib[new_index] = (temp_pt[new_index])**(2*p)
        # delete the original two entities
        for k in i:   
            del temp_v[k]
            temp_entity.remove(k)
            del temp_pt[k]
            del dib[k]

'''Update all variables if it's a jet'''        
def handle_jet(i, temp_v, temp_entity, temp_pt,dib, jets,dij): 
        jets.append(i)
        del temp_v[i]
        temp_entity.remove(i)
        del temp_pt[i]
        del dib[i]
        for k in list(dij.keys()):
            for kk in k:
                if kk == i:
                    del dij[k]
