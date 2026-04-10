from mpl_toolkits.mplot3d import Axes3D    ##New Library required for projected 3d plots

import numpy
from matplotlib import pyplot, cm

###variable declarations
nx = 81 # number of grid points in axis x
ny = 81 # number of grid points in axis y
nt = 100 #number of timesteps
c = 1 # wavespeed
dx = 2 / (nx - 1) #  distance between any pair of adjacent grid points in x axis
dy = 2 / (ny - 1) #  distance between any pair of adjacent grid points in y axis
sigma = .2
dt = sigma * dx # length of time per time step

x = numpy.linspace(0, 2, nx)
y = numpy.linspace(0, 2, ny)

u = numpy.ones((ny, nx)) ##create a 1xn vector of 1's
un = numpy.ones((ny, nx)) ##

###Assign initial conditions

##set hat function I.C. : u(.5<=x<=1 && .5<=y<=1 ) is 2
u[int(.5 / dy):int(1 / dy + 1),int(.5 / dx):int(1 / dx + 1)] = 2 


X, Y = numpy.meshgrid(x, y)  

"""
###Plot Initial Condition (hat function)
##the figsize parameter can be used to produce different sized images
fig = pyplot.figure(figsize=(11, 7), dpi=100)
ax = fig.add_subplot(projection='3d')                      
                          
surf = ax.plot_surface(X, Y, u[:], cmap=cm.viridis)

pyplot.show()
"""

u = numpy.ones((ny, nx))
u[int(.5 / dy):int(1 / dy + 1), int(.5 / dx):int(1 / dx + 1)] = 2

#Calculate wave behaviour in across time steps
for n in range(nt + 1): ##loop across number of time steps
    un = u.copy()
    u[1:, 1:] = (un[1:, 1:] - (c * dt / dx * (un[1:, 1:] - un[1:, :-1])) -
                              (c * dt / dy * (un[1:, 1:] - un[:-1, 1:])))
    u[0, :] = 1
    u[-1, :] = 1
    u[:, 0] = 1
    u[:, -1] = 1

fig = pyplot.figure(figsize=(11, 7), dpi=100)
ax = fig.add_subplot(projection='3d')
surf2 = ax.plot_surface(X, Y, u[:], cmap=cm.viridis)

pyplot.show()