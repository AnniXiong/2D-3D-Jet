# Anni Xiong
#
# This program produces a 2D decay chain which is stoped when energy is below min energy
import matplotlib.pyplot as plt
import numpy as np
import math
import collections
from astropy.table import Table, Column
from astropy.table import QTable

startE = 1 # the starting enrgy of 0 particle
MinEnergy = 0.4
pi = math.pi

Zd = {0: startE}
Thetad = {0: 0}
momentum = {0:[1,0]}

p_component = {0: [1,0]}
Ztemporary = {0: startE}
Thetatemporary = {0: 0}

def main():
	while 1:
		global Ztemporary
		global Thetatemporary
		global p_component
		# at this point, you should have a complete dictionary of Z values at disposal
		# checking if each vertex has enough energy to go on
		#print ('Ztemporary', Ztemporary)
		for k, v in list(Ztemporary.items()):
			if v < MinEnergy:
				del Ztemporary[k]
		vn = len(Ztemporary)
		if not vn:
			break
		# get randomly genrated Zs from calling get_random_Z()
		E_percent = get_random_Z(vn)
		#print ('E_percent: ',E_percent)
		
		# get the other half of Z from calculation and index them
		Ztemp = vertexZ(E_percent, Ztemporary)
		#print ('Ztemp', Ztemp)
		theta_list = get_random_theta(vn,Ztemp)
		#print ('theta list', theta_list)
		#print ('p_component',p_component)
		Pcomponent = vertexTheta1(theta_list, Ztemp, p_component)
		# this call should return a complete version of theta which will later be appended to Thetatemporary
		thetaTemp = vertexTheta2(Pcomponent, theta_list, Thetatemporary)

		Zd.update(Ztemp)
		Thetad.update(thetaTemp)
		momentum.update(Pcomponent)
		
		Ztemporary = Ztemp
		p_component = Pcomponent
		Thetatemporary = thetaTemp
	
		#print (Zd, 'length :', len(Zd))
		#print (Thetad, 'length :', len(Thetad))
		print ('momentum', momentum)
""" this function should return the randomly generated Z values in a list according to what n is """
def get_random_Z (vn):
	z = []
	while 1:
		n = np.random.uniform(0.25, 0.75)
		nc = np.random.uniform(1.176, 2.858)
		fx = 1/(n + 0.1)
		if nc < fx:
			z.append (n)	
		if len(z) == vn:
			break
	return z

""" this function should return the Ztemporary dictionary for each layer of decay """
# E_percent/z is the list of newly generated random Z and Ztemporary contains the parent information
# Zt here is a temporary place holder which represents the list of Z information gnerated everytime the main while loop runs
def vertexZ (E_percent, Ztemporary):
	Zt = {}
	for i, k in enumerate(Ztemporary.keys()):
		Zt[(k*2)+1] = Ztemporary[k] *E_percent[i]
		Zt[(k*2)+2] = Ztemporary[k]*(1-E_percent[i])
	return Zt

""" this function should produce the randomly generated theta """
def get_random_theta (vn, Ztemp):
	theta = []
	while 1:
		ns = np.random.uniform( 1/((pi/2)+0.1) ,10 )
		x = np.random.uniform(0, pi/2)
		f_t = 1/(x + 0.1)
		if ns < f_t:
			theta.append (x)
		if len(theta) == vn:
			break
	# to put keys on the random theta
	sorted_odd_keys = sorted([k for k in Ztemp.keys() if k%2])
	Theta = dict(zip(sorted_odd_keys, theta))
	return Theta

# theta_list is the randomly generated theta
# Ztemp : the list of Z for each particle in one layer
# thetatemporary is the list of complete theta generated last time running the main
""" This method is to calculate the x and y momentum component for each particle """
def vertexTheta1 (theta_list, Ztemp, p_component):
	PP_component = {}
	Ztemp = collections.OrderedDict(sorted(Ztemp.items()))
	for k in Ztemp.keys():
		if k%2 != 0:
			py1 = Ztemp[k] * math.sin(theta_list[k])
			px1 = Ztemp[k] * math.cos(theta_list[k])
			p1 = [px1, py1]
			PP_component[k] = p1
		elif k%2 == 0:
			p_parent = p_component[(k-2)/2]
			p_odd= PP_component[k-1]
			px2 = p_parent[0] - p_odd[0]
			py2 = p_parent[1] - p_odd[1]
			p2 = [px2, py2]
			PP_component[k] = p2
	return PP_component

"""This method is to calculate the angle of the even numbered particle according to the odd numbered particle"""
# Pcomponent is the same thing as PP_component
def vertexTheta2 (Pcomponent, theta_list, Thetatemporary ):
	Thetat = {}
	for k in Pcomponent.keys():
		if k%2 != 0:
			Thetat[k] = theta_list[k] 
		elif k%2 == 0:
			Pcomponentxy = Pcomponent[k]
			theta = math.atan(Pcomponentxy[1]/Pcomponentxy[0])
			Thetat[k] = theta 
	return Thetat
main()




