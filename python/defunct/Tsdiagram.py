import freesteam
import matplotlib
matplotlib.use('gtkcairo')
from pylab import *
import math

figure()
hold(1)
n = 400
TT = [273.15 + (freesteam.TCRIT - 273.15)*x/n for x in range(n+1)]

# REGION MAP

Tmin = 273.15
Tmax = 1073.15
DT = Tmax - Tmin
smin = 0e3
smax = 10e3
Ds = smax - smin
ss = arange(smin,smax,Ds/100)
TT = arange(Tmin,Tmax,DT/100)
im = zeros((len(TT),len(ss)))
x = 0
for T in TT:
	print "T = %f K" % (T)
	y = 0
	for s in ss:
		#if freesteam.bounds_Ts(T,s,0):
		#	continue
		r = freesteam.region_Ts(T,s)
		#print "T = %f K, s = %f kg/kgK, region[%d,%d] = %d" % (T,s/1e3,x,y,r)
		im[x,y] = float(r) / 4.
		y += 1
	x += 1

imshow(im,extent=[smin/1e3,smax/1e3,Tmin,Tmax],origin='lower',aspect='auto',interpolation='nearest',alpha=0.6)

# SATURATION CURVES

Tmin = 273.15
Tmax = freesteam.TCRIT
n = 1000
DT = (Tmax - Tmin)/n
TT0 = 273.15 + DT*array(range(n+1))
psat = array([freesteam.psat_T(T)/1e6 for T in TT0])
sf = [freesteam.region4_Tx(T,0).s/1e3 for T in TT0]
sg = [freesteam.region4_Tx(T,1).s/1e3 for T in TT0]
plot(sf,TT0,'b-')
plot(sg,TT0,'r-')

# LINES OF CONSTANT PRESSURE

pp = logspace(-3,3,50)*1e5
ss = arange(0.,10.,0.1)*1e3

for p in pp:
	TT = []
	for s in ss:
		T = None
		if not freesteam.bounds_ps(p,s,0):
			try: 
				T = freesteam.steam_ps(p,s).T
			except:
				pass
		TT += [T]
	plot(ss/1e3,TT,alpha=0.4)
	#sys.exit(1)

# QUIVER SHOWING PARTIAL DERVIATIVE (dT/ds)p

ss1 = arange(0.,10.,0.5)*1e3

x = []
y = []
u = []
v = []
for p in pp:
	for s in ss1:
		if freesteam.bounds_ps(p,s,0):
			continue
		S = freesteam.steam_ps(p,s)
		assert(fabs(S.s - s) < 1e-5)
		dy = freesteam.freesteam_deriv(S,"Tsp")
		dx = 1
		m = math.sqrt(dx**2 + dy**2)
		x += [s/1.e3]
		y += [S.T]
		u += [dx/m]
		v += [dy/m]

quiver(x,y,u,v,alpha=0.6)
axis([0,10,273.15,1073.15])
#axis([2,6,573.15,1073.15])
xlabel('s / [kJ/kgK]')
ylabel('T / [K]')
show()
