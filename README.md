# 2D-3D-Jet
it consists of scripts of creating, plotting, and saving the data for 2D and 3D parton shower.
Minimum energy can be adjusted to influence the number of partons been produced

# Indexing:
particle indexing is in the follwing manner:

       / 3 ...
      1
     / \ 4 ...
    0  
     \ / 5 ...
      2
       \ 6 ...
   
so that every particle index times 2 then plus 1 or 2 will give the index of its daughter particle

# Assumptions:
1.The script assumes conservation of energy and momentum. And because the masses of particles are very small compared to the total energy, the momentum is set to equal to the energy, zero particle has energy 1.
2. Beam axis is in z for the 3d version
3.This program is a simplified simulation and it assumes all particle being produced are the same type.

# Saving part
In the MC_saving.py, make sure that you have installed astropy package in order for it to work, here is a quick way to install it

    pip install --no-deps astropy

two data files for 2D and 3D version will be created in your current directory and note that for the 3D
version, 2 angles are put in one column, first corresponds to thata and the second phi in the spherical coordinate.

# antikt
The module that performs antikt clusttering algorithm for final state partons following this reference

[antikt clusttering algorithm](https://arxiv.org/abs/0802.1189)

Equations used for defining angular distance between two pseudo jets

(https://github.com/AnniXiong/2D-3D-Jet/blob/master/equations.png)

TLorentzVector from ROOT is used in this program

# Hit position
plots where partons might hit on the detector assuming a 2D flat screen
will produce a png file in the same directory 

# plotting antikt
either gives a single jet or plots out the distribution of number of jets from multiple p_R pairs
will produce a png file in the same directory 

# jet observable
Plots the pseudo mass distribution from many parton shower events
will produce a png file in the same directory 
