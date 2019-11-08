import freesteam
import matplotlib
matplotlib.use('gtkcairo')
from pylab import *
import math

figure()
hold(1)

# SATURATION CURVE

n = 400
TT0 = [273.15 + (freesteam.TCRIT - 273.15)*x/n for x in range(n+1)]
psat = [freesteam.psat_T(T)/1e6 for T in TT0]

# REGION MAP

Tmin = 273.15
Tmax = 1073.15
DT = Tmax - Tmin
pmin = 1e-3*1e5
pmax = 1e3*1e5
DP = pmax - pmin
pp = arange(pmin,pmax,DP/400)
#pp = logspace(-3,3)*1.e5
TT = arange(Tmin,Tmax,DT/500)
im = zeros((len(pp),len(TT)))
x = 0
for p in pp:
	#print "p = %f MPa" % (p/1e6)
	y = 0
	for T in TT:
		S = freesteam.steam_pT(p,T)
		#print "p = %f, T = %f" % (p,T)
		r = S.region
		#print "p = %f MPa, T = %f K, region[%d,%d] = %d" % (p/1e6,T,x,y,r)
		im[x,y] = float(r) / 4.
		y += 1
	x += 1

imshow(im,extent=[Tmin,Tmax,pmin/1e6,pmax/1e6],origin='lower',aspect='auto',interpolation='nearest',alpha=0.6)

# LINES OF CONSTANT ENTHALPY

hh = arange(100,4500,200)*1e3
for h in hh:
	TT2 = [freesteam.steam_ph(p,h).T for p in pp]
	plot(TT2,pp/1e6,'g-')

plot(TT0,psat,'b-')
axis([Tmin,Tmax,pmin/1e6,pmax/1e6])
#quiver(x,y,u,v,alpha=0.6)

# LINES OF CONSTANT ENTROPY

ss = arange(0,12,1./3)*1e3
for s in ss:
	TT2 = [freesteam.steam_ps(p,s).T for p in pp]
	plot(TT2,pp/1e6,'r:')

plot(TT0,psat,'b-')
axis([Tmin,Tmax,pmin/1e6,pmax/1e6])
#quiver(x,y,u,v,alpha=0.6)


xlabel('T / [K]')
ylabel('p / [MPa]')
show()


