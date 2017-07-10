# Anni Xiong
#
# This program produces a 3D decay chain which is stopped when energy is below min energy

import matplotlib.pyplot as plt
import numpy as np
import collections

startE = 1 # the starting enrgy of 0 particle
#MinEnergy = float(input("enter your MinEnergy for 3D version here (> 0 and <1): ")) 
MinEnergy = 0.05
# beam axis in z

Zd = {0: startE}
Thetad = {0: [0, 0]}
momentum = {0:[0,0,1]}

p_component = {0: [0,0,1]}
Ztemporary = {0: startE}
Thetatemporary = {0: [0,0]}

def main():
	global Minenrgy
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
		#print ('Ztemporary', Ztemporary)
		# get randomly genrated Zs from calling get_random_Z()
		E_percent = get_random_Z(vn)
		#print ('E_percent: ',E_percent)
		
		# get the other half of Z from calculation and index them
		Ztemp = vertexZ(E_percent, Ztemporary)
		#print ('Ztemp', Ztemp)
		theta_list = get_random_theta(vn,Ztemp)
		#print ('theta list', theta_list)
		sec_angle = get_random_phi(vn,Ztemp)
		#print ('sec_angle', sec_angle)
		#print('p_component', p_component)
		#print ('----')
		Pcomponent = vertexTheta1(theta_list, Ztemp, p_component, sec_angle)
		#print ('Pcomponent',Pcomponent)
		# this call should return a complete version of theta which will later be appended to Thetatemporary
		thetaTemp = vertexTheta2(Pcomponent, theta_list, Thetatemporary,sec_angle)
		#print ('thetaTemp', thetaTemp)
		#print('')
		Zd.update(Ztemp)
		Thetad.update(thetaTemp)
		momentum.update(Pcomponent)
		
		Ztemporary = Ztemp
		p_component = Pcomponent
		Thetatemporary = thetaTemp
	
		
	'''print ("Total energy3d", Zd, 'length :', len(Zd))
				print ("Theta & phi", Thetad, 'length :', len(Thetad))
				print('momentum xyz', momentum)
				print('Zdd',Zd)'''

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
		ns = np.random.uniform( 1/((np.pi/2)+0.1) ,10 )
		x = np.random.uniform(0, np.pi/2)
		f_t = 1/(x + 0.1)
		if ns < f_t:
			theta.append (x)
		if len(theta) == vn:
			break
	# to put keys on the random theta
	sorted_odd_keys = sorted([k for k in Ztemp.keys() if k%2])
	Theta = dict(zip(sorted_odd_keys, theta))
	return Theta

""" To get the third angle required by a 3D plot"""
def get_random_phi(vn, Ztemp):
	phi = []
	for i in range(vn*2):
		x = np.random.uniform(0, 2*np.pi)
		phi.append(x)
	keys = sorted(Ztemp.keys())
	Phi = dict(zip(keys, phi))
	return Phi

# theta_list is the randomly generated theta
# Ztemp : the list of Z for each particle in one layer
# thetatemporary is the list of complete theta generated last time running the main
""" This method is to calculate the x, y and z momentum component for each particle """
def vertexTheta1 (theta_list, Ztemp, p_component, sec_angle):
	PP_component = {}
	#Ztemp = collections.OrderedDict(sorted(Ztemp.items()))
	Ztempsortedkeys = sorted(list(Ztemp.keys()))
	for k in Ztempsortedkeys:
		if k%2 != 0:
			px1 = Ztemp[k] * np.sin(theta_list[k]) * np.cos(sec_angle[k])
			py1 = Ztemp[k] * np.sin(sec_angle[k]) * np.sin(theta_list[k])
			pz1 = Ztemp[k] * np.cos(theta_list[k])
			p1 = [px1, py1, pz1]
			PP_component[k] = p1
		elif k%2 == 0:
			p_parent = p_component[(k-2)/2]
			p_odd= PP_component[k-1]
			px2 = p_parent[0] - p_odd[0]
			py2 = p_parent[1] - p_odd[1]
			pz2 = p_parent[2] - p_odd[2]
			p2 = [px2, py2, pz2]
			PP_component[k] = p2 
	return PP_component

"""This method is to calculate the angle of the even numbered particle according to the odd numbered particle"""
# Pcomponent is the same thing as PP_component
def vertexTheta2 (Pcomponent, theta_list, Thetatemporary, sec_angle):
	Thetat = {}
	Pcomponentsortedkeys = sorted(list(Pcomponent.keys()))
	for k in Pcomponentsortedkeys:
		phi = sec_angle[k]
		if k%2 != 0:
			theta = theta_list[k]
		elif k%2 == 0:
			Pcomponentxy = Pcomponent[k]
			theta = np.arctan(Pcomponentxy[1]/Pcomponentxy[0])
			Thetat[k] = theta 
		Thetat[k] = [theta,phi]
	return Thetat
main()

# printing out the final state particle
final = []
for i ,k in momentum.items():
	k2 = (i*2) + 1 
	if not k2 in momentum:
		final.append(i)
final.sort()
#print('final state particles',final)

# summing up the momentum components directly from the dictionary
'''summx = 0
summy = 0
summz = 0
print('------momentum sum----------')
for i in final:
	ppp = momentum[i]
	summx = summx + ppp[0]
	summy = summy + ppp[1]
	summz = summz + ppp[2]
	
print ('sum from x momentum', summx)
print ('sum from y momentum', summy)
print ('sum from z momentum', summz)'''
