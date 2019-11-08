import freesteam
import matplotlib
matplotlib.use('gtkcairo')
from pylab import *
import math

figure()
hold(1)
n = 400
TT = [273.15 + (freesteam.TCRIT - 273.15)*x/n for x in range(n+1)]

hf = [freesteam.region4_Tx(T,0).h/1e3 for T in TT]
hg = [freesteam.region4_Tx(T,1).h/1e3 for T in TT]
plot(hf,TT,'b-')
plot(hg,TT,'r-')

pp = logspace(-3,3)*1e5

# these are the pressures we're interested in here
pp = [freesteam.psat_T(50+273.15), 3e6, 12e6,  165e5, 300e5]

print "low p =",pp[0]

hh = arange(50.,4500.,100)*1e3

hh1 = arange(50.,4500.,20)*1e3


x = []
y = []
u = []
v = []
for p in pp:
	plot(hh1/1e3,[freesteam.steam_ph(p,h).T for h in hh1],alpha=0.8)
	if 0:
		for h in hh:
			try:
				S = freesteam.steam_ph(p,h)
				x += [S.h/1.e3]
				y += [S.T]
				dy = freesteam.freesteam_deriv(S,'T','h','p')
				dx = 0.0005
				m = math.sqrt(dx**2 + dy**2)
				u += [dx/m]
				v += [dy/m]
			except:
				pass

plot([0,4500],[550+273.15,550+273.15],'b--')

s = freesteam.steam_pT(12e6, 550+273.15).s
pp = linspace(3e6,12e6)
hh = [freesteam.steam_ps(p,s).h/1e3 for p in pp]
TT = [freesteam.steam_ps(p,s).T for p in pp]
plot(hh,TT,'g--')

if 1:
	s = freesteam.steam_pT(3e6, 550+273.15).s
	pp = linspace(0.1e5,3e6)
	hh = [freesteam.steam_ps(p,s).h/1e3 for p in pp]
	TT = [freesteam.steam_ps(p,s).T for p in pp]
	plot(hh,TT,'g--')

quiver(x,y,u,v,alpha=1)
axis([0,4500,273.15,1073.15])
xlabel('h / [kJ/kg]')
ylabel('T / [K]')
show()
