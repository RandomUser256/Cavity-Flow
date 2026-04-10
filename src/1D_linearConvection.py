import numpy                       #here we load numpy
from matplotlib import pyplot      #here we load matplotlib
import time, sys                   #and load some utilities
        
def linearconv(nx):
    dx = 2 / (nx - 1)  #  distance between any pair of adjacent grid points
    nt = 20    #nt is the number of timesteps we want to calculate
    c = 1  #wavespeed 
    sigma = .5
    
    #As more grid points are added, the distance between them (dx) gets smaller.
    #This means that the time step (dt) must also get smaller to satisfy the stability
    dt = sigma * dx #amount of time each timestep covers (delta t)  

    u = numpy.ones(nx)      #numpy function ones()
    u[int(.5 / dx):int(1 / dx + 1)] = 2  #setting u = 2 between 0.5 and 1 as per our I.C.s

    un = numpy.ones(nx)

    for n in range(nt):  #iterate through time
        un = u.copy() # copies original values of u in that instance of time
        for i in range(1, nx):
            u[i] = un[i] - c * dt / dx * (un[i] - un[i-1])
        
    pyplot.plot(numpy.linspace(0, 2, nx), u)
    pyplot.show()

nx = 41 # Number of grid points
linearconv(nx)