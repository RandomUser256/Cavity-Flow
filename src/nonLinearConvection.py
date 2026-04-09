import numpy                 # we're importing numpy 
from matplotlib import pyplot    # and our 2D plotting library

nx = 41 # Number of grid points
grid_length = 2
dx = grid_length / (nx - 1) #  distance between any pair of adjacent grid points
nt = 20    #nt is the number of timesteps we want to calculate
dt = .025  #dt is the amount of time each timestep covers (delta t)

u = numpy.ones(nx)      #as before, we initialize u with every value equal to 1.
u[int(.5 / dx) : int(1 / dx + 1)] = 2  #then set u = 2 between 0.5 and 1 as per our I.C.s

un = numpy.ones(nx) #initialize our placeholder array un, to hold the time-stepped solution

for n in range(nt): # runs for the amount of time steps specified
    un = u.copy()
    #Calcula nuevo estado de u para cada instancia de tiempo 
    for i in range(1, nx):
        u[i] = un[i] - ( un[i] * dt / dx * (un[i] - un[i-1]) )
    #pyplot.plot(numpy.linspace(0, grid_length, nx), u);
    #pyplot.show()

pyplot.plot(numpy.linspace(0, grid_length, nx), u);
pyplot.show()