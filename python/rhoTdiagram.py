# encoding: utf-8
import freesteam
import matplotlib
matplotlib.use('gtkcairo')
from pylab import *
import math, sys

# Plot a curve of density with temperature for different pressures. We're
# especially interested here in the supercritical curves.

pp = [1e4, 5e4, 1e5, 5e5, 1e6, 5e6, 10e6, 20e6, 22e6,23e6,25e6, 30e6,50e6,100e6]

figure()
hold(1)

for p in pp:
	TT = arange(0,800,2)+273.15
	rrho  = [freesteam.steam_pT(p,T).rho for T in TT]
	plot(TT-273.15,rrho,label='%f MPa' % (p/1e6))

xlabel(u"Temperature / [°C]")
ylabel(u"Density / [kg/m³]")
legend()
show()

