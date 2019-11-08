import freesteam
import matplotlib
matplotlib.use('gtkcairo')
from pylab import *
import math, sys

figure()
hold(1)

# SATURATION CURVE

Tmin = 273.15
Tmax = freesteam.TCRIT
n = 1000
DT = (Tmax - Tmin)/n
TT0 = 273.15 + DT*array(range(n+1))
psat = array([freesteam.psat_T(T)/1e6 for T in TT0])
uf = [freesteam.region4_Tx(T,0).u/1e3 for T in TT0]
ug = [freesteam.region4_Tx(T,1).u/1e3 for T in TT0]

# REGION MAP

umin = 0
umax = 3800e3
Du = umax -umin
pmin = 1.e-3*1e5
pmax = 1.e3*1e5
DP = pmax - pmin
pp = arange(pmin,pmax,DP/100)
uu = arange(umin,umax,Du/100)
im = zeros((len(pp),len(uu)))
x = 0
for p in pp:
	#print "p = %f MPa" % (p/1e6)
	y = 0
	for u in uu:
		S = freesteam.steam_pu(p,u)
		#print "p = %f, T = %f" % (p,T)
		r = ord(S.region)
		#print "p = %f MPa, h = %f kJ/kg, region[%d,%d] = %d, T = %f" % (p/1e6,h/1e3,x,y,r,S.T)
		im[x,y] = float(r) / 4.
		y += 1
	x += 1

imshow(im,extent=[umin/1e3,umax/1e3,pmin/1e6,pmax/1e6],origin='lower',aspect='auto',interpolation='nearest',alpha=0.6)

# LINES OF CONSTANT TEMPERATURE

if 1:
	TT = logspace(math.log10(273.15),math.log10(1073.15),30)
	for T in TT:
		print "T =",T
		smin = freesteam.bound_pmax_T(T).s + 0.1 
		smax = freesteam.region2_pT(1,T).s - 0.1
		ss = linspace(smin,smax,1000)
		uu = []
		pp = []
		for s in ss:
			if freesteam.bounds_Ts(T,s,0):
				continue
			S = freesteam.steam_Ts(T,s)
			uu += [S.u/1e3]	
			pp += [S.p/1e6]
		plot(uu,pp,'g-')

# LINES OF CONSTANT ENTROPY

sgpmin = freesteam.region4_Tx(freesteam.Tsat_p(freesteam.PTRIPLE),1.).s
print sgpmin

ss = logspace(math.log10(1e3),math.log10(12e3),30)
for s in ss:
	print "s =",s
	Tmax = freesteam.steam_ps(100e6,s).T
	if s<sgpmin:
		Tmin = freesteam.TMIN
	else:
		Tmin = freesteam.steam_ps(freesteam.PTRIPLE,s).T
	print "Tmin = %f, Tmax = %f" %(Tmin,Tmax)
	TT = linspace(Tmin,Tmax,1000)
	uu = []
	pp = []
	for T in TT:
		#print T
		if freesteam.bounds_Ts(T,s,0):
			continue
		S = freesteam.steam_Ts(T,s)
		uu += [S.u/1e3]	
		pp += [S.p/1e6]
	plot(uu,pp,'r-')


# plot the sat curve
plot(uf,psat,'b-')
plot(ug,psat,'r-')

xlabel('u / [kJ/kg]')
ylabel('p / [MPa]')
show()


