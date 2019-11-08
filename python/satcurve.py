import matplotlib
# vim: fileencoding=utf-8
matplotlib.use('gtkcairo')
from pylab import *
import freesteam

n = 2000
T = [273.15 + (freesteam.TCRIT - 273.15)*x/n for x in range(n+1)]

dpdT = [freesteam.dpsatdT_T(t)/1e6 for t in T]
rhof = [freesteam.rhof_T(t) for t in T]
rhog = [freesteam.rhog_T(t) for t in T]

figure()
plot(T,dpdT,'g-')
title("Derivative ∂p/∂T along the saturation line")
xlabel("T [K]")
ylabel("∂p/∂T [bar/K]")

figure()
hold(1)
plot(T,rhof,'b-',label="liquid")
plot(T,rhog,'r-',label="vapour")
title("Saturation curves, density versus temperature")
xlabel("T [K]")
ylabel(r"$\rho$ [kg/m3]")
legend()

figure()
T = [273.15 + (freesteam.TCRIT - 273.15)*x/n for x in range(n+1)]
drhof = [freesteam.drhofdT_T(t) for t in T]
drhog = [freesteam.drhogdT_T(t) for t in T]
plot(T,drhof,'b-',label="liquid")
plot(T,drhog,'r-',label="vapour")
title("Derivatives of density with respect to temperature along the saturation line")
axis([273.15,freesteam.TCRIT,-20,+20])
xlabel("T [K]")
ylabel(r"$\partial \rho / \partial T$ [kg/m3]")

show()

