# Anni Xiong
#
# This program produces data of a 2d parton shower, which is stoped when energy is below energy threshold
import numpy as np

startE = 1 # the starting enrgy of 0 particle

Zd = {0: startE}
Thetad = {0: 0}
momentum = {0:[1,0]}

def main(MinEnergy):
	p_component = {0: [1,0]}
	Ztemporary = {0: startE}
	Thetatemporary = {0: 0}
	while 1:
		for k, v in list(Ztemporary.items()):                    # check if have enough energy to continue
			if v < MinEnergy:
				del Ztemporary[k]
		vn = len(Ztemporary)
		if not vn:
			break
		E_percent = get_random_Z(vn)
		Ztemp = vertexZ(E_percent, Ztemporary)
		theta_list = get_random_theta(vn,Ztemp)
		Pcomponent = vertexTheta1(theta_list, Ztemp, p_component)
		thetaTemp = vertexTheta2(Pcomponent, theta_list, Thetatemporary)
		
		Zd.update(Ztemp)
		Thetad.update(thetaTemp)
		momentum.update(Pcomponent)
		
		Ztemporary = Ztemp
		p_component = Pcomponent
		Thetatemporary = thetaTemp
	
	'''print ("Total energy",Zd, 'length :', len(Zd))
				print ("Deflected angle", Thetad, 'length :', len(Thetad))
				print ('momentum', momentum)
				print ('')'''

""" return the randomly generated Z values in a list according to n"""
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

""" return the Ztemporary dictionary for each layer of decay """
def vertexZ (E_percent, Ztemporary):
	Zt = {}
	for i, k in enumerate(Ztemporary.keys()):
		Zt[(k*2)+1] = Ztemporary[k] *E_percent[i]
		Zt[(k*2)+2] = Ztemporary[k]*(1-E_percent[i])
	return Zt

""" produce the randomly generated theta """
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

""" calculate the x and y momentum component for each particle """
def vertexTheta1 (theta_list, Ztemp, p_component):
	PP_component = {}
	Ztempsortedkeys = sorted(list(Ztemp.keys()))
	for k in Ztempsortedkeys:
		if k%2 != 0:
			py1 = Ztemp[k] * np.sin(theta_list[k])
			px1 = Ztemp[k] * np.cos(theta_list[k])
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

""" calculate the angle of the even numbered parton according to the odd numbered particle"""
# Pcomponent = PP_component
def vertexTheta2 (Pcomponent, theta_list, Thetatemporary ):
	Thetat = {}
	Pcomponentsortedkeys = sorted(list(Pcomponent.keys()))
	for k in Pcomponentsortedkeys:
		if k%2 != 0:
			Thetat[k] = theta_list[k] 
		elif k%2 == 0:
			Pcomponentxy = Pcomponent[k]
			theta = np.arctan(Pcomponentxy[1]/Pcomponentxy[0])
			Thetat[k] = theta 
	return Thetat

#main(0.1)

# printing out the final state particle
'''final = []
for i ,k in momentum.items():
	k2 = (i*2) + 1 
	if not k2 in momentum:
		final.append(i)
final.sort()
#print('final',final)

# summing up the momentum components directly from the dictionary
summx = 0
summy = 0
for i in final:
	ppp = momentum[i]
	summx = summx + ppp[0]
	summy = summy + ppp[1]
print ('sum from x momentum', summx)
print ('sum from y momentum', summy)'''
		



