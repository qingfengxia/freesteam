#!/usr/bin/python
# mollier - plot a Mollier diagram using freesteam libraries
# Copyright 2008,2009 Grant Ingram
# Copyright 2009 John Pye
##     This program is free software: you can redistribute it and/or modify
##     it under the terms of the GNU General Public License as published by
##     the Free Software Foundation, either version 3 of the License, or
##     (at your option) any later version.

##     This program is distributed in the hope that it will be useful,
##     but WITHOUT ANY WARRANTY; without even the implied warranty of
##     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##     GNU General Public License for more details.

##     You should have received a copy of the GNU General Public License
##     along with this program.  If not, see <http://www.gnu.org/licenses/>

from freesteam import *
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']))
rc('text', usetex=True)
from pylab import *
from math import *

from matplotlib.ticker import MultipleLocator, FormatStrFormatter

# Diagram Ranges - it would be nice to do this automagically but for
# the moment this will have to do..
smin = 6; smax = 9;
hmin = 2000; hmax = 4500;
tmin =  6.96963241256; tmax = 800;
pressure_range = [0.01,0.025,0.05,0.10,0.25,0.5,1,2,3,5,7.5,10,15,20,25,30,40,50,60,80,100,125,150,200]
pmax = 500; pmin = 0.01;
twophase_x_range = [0.74,0.76,0.78,0.80,0.82,0.84,0.86,0.88,0.90,0.92,0.94,0.96,0.98,1.0]
const_T_range = [25,50,75,100,125,150,175,200,225,250,275,300,325,350,375,400,425,450,475,500,525,550,575,600,625,650,675,700,725,750,775,800]
xy_ratio = float(hmax - hmin) / float(smax - smin)

# This makes the picture A4 matplotlib accepts dimensions in inches...
figure(figsize = (8.26771654,11.6929134))
paper_ratio = 11.6929134 / 8.26771654



# supercritical region
print "Supercritical region..."

supcrit_p = [250,300,400,500]
supcrit_T = linspace(tmin,tmax,50)

for i in supcrit_p:
    x = []; y = [];
    p = i * 1e5 #bar
    for j in supcrit_T:
        T = j+273.15 # K
        S = steam_pT(p,T)
        y.append(S.h/1000)
        x.append(S.s/1000)
    plot(x,y,'b-')
    text(x[-1]-0.05,y[-1]+10,r'%3.0f bar' % i,color="blue",rotation='vertical')

# lines of constant pressure

print "Lines of constant pressure..."

for i in pressure_range:
    p = i * 1e5 #bar
    #print "p = %f bar"%p
    S = region4_Tx(Tsat_p(p),1)
    saturation_T = (S.T-273.15)
    superheat_T_range = linspace(saturation_T,tmax,50)
    
    x = []; y = []; 
    T = saturation_T + 273.15 # K
    twophase_x_range_fine = linspace(min(twophase_x_range),max(twophase_x_range),50)
    for j in twophase_x_range_fine:
        S = region4_Tx(T,j)
        x.append(S.s/1000)
        y.append(S.h/1000)

    for j in superheat_T_range:
        T = j+273.15 # K
        #print "p = %f, T = %f" %(p,T)
        S = steam_pT(p,T)
        if S.T > Tsat_p(S.p):
            x.append(S.s/1000)
            y.append(S.h/1000)
    plot(x,y,'b-')

    if x[-1] < smax:
        text(x[-1]-0.05,y[-1]+10,r'%3.0f bar' % i,color="blue",rotation='vertical')
    else:
        for k in range(len(x)): # find index which the line crosses smax
            if x[k] > smax: # we've gone past the limit
                angle = atan(paper_ratio * ( ((y[k-8]-y[k-7]) /(x[k-8]-x[k-7])) / xy_ratio) )
                text_x_move = 0.15 * sin (angle) 
                text_y_move = 0.15 * cos (angle) * paper_ratio / xy_ratio
                angle = angle * 180.0 / pi
                text(x[k-8]-text_x_move,y[k-8]-text_y_move,r'%3.2f bar' % i,color="blue",rotation=angle)
                break
                
# lines of constant dryness fraction

print "Lines of dryness fraction (quality)..."

twophase_T = linspace(tmin,373,20)

for i in twophase_x_range:
    x = []; y = [];
    for j in twophase_T:
        T = j+273.15 # K
        S = region4_Tx(T,i)
        y.append(S.h/1000)
        x.append(S.s/1000)
    plot(x,y,'r-')
    if y[0] > hmin:
        text(x[0]+0.12,y[0]-5,r'%0.2f' % i,color="red")

# lines of constant temperature

print "Lines of constant temperature..."

for i in const_T_range:
    T = i + 273.15 # K
    #print "T = %f" % T
    if T < TCRIT: # temperature is below the critical point
        S = region4_Tx(T,1)
        saturation_p = float(S.p / 1e5)        
        p_range = linspace(pmin,saturation_p,50)
    else:
        p_range = linspace(pmin,pmax,50)

    x = []; y = []; 

    for j in p_range:
        p = j * 1e5 # bar
        S = steam_pT(p,T)
        if S.T > Tsat_p(p):
            x.append(S.s/1000)
            y.append(S.h/1000)                

    if len(x):
        plot(x,y,'g-')
        text(smax+0.1,max(y)-10,r'%3.0f $^\circ$ C' % i,color="green")



figtext(0.15,0.85,\
        "Calculated with freesteam v%s \n IAPWS-IF97 Industrial Formulation" % FREESTEAM_VERSION,bbox=dict(facecolor='white', alpha=0.75))

# work-around for non-helvetica default axes
# in theory this shouldn't be required
ylabels = []
ytickloc = arange(hmin,hmax+100,100)
for i in ytickloc: ylabels.append(str(i))
xlabels = []
xtickloc = arange(smin,smax+0.25,0.25)
for i in xtickloc: xlabels.append(str(i))

# Axes details: Quite a lot of work to get minor grids working - there
# may be simpler ways of doing it!
#for the minor ticks, use no labels; default NullFormatter
gca().xaxis.set_minor_locator(MultipleLocator(0.05))
gca().xaxis.grid(True, which='minor',linewidth=0.25,linestyle='solid',color='0.75')  
gca().yaxis.set_minor_locator(MultipleLocator(10))
gca().yaxis.grid(True, which='minor',linewidth=0.25,linestyle='solid',color='0.75') 

# Major grids should be thicker
gca().xaxis.grid(True,'major',linewidth=0.5,linestyle='solid',color='0.1')
gca().yaxis.grid(True,'major',linewidth=0.5,linestyle='solid',color='0.1')
gca().set_axisbelow(True)

title('Mollier Diagram')
ylabel('Specific Enthalpy, kJ / kg')
xlabel('Specific Entropy, kJ / kg K')
xticks(xtickloc,xlabels)
yticks(ytickloc,ylabels)
xlim( smin,smax )
ylim( hmin,hmax )

print "Exporting PDF file to current directory..."
savefig('mollier.pdf')

#print "Exporting EPS file to current directory..."
#savefig('mollier.ps',dpi = 600)

#show()

