#!/usr/bin/python
# vim: set fileencoding=utf-8 :

# tables - a script that produces the data for Steam Tables using
# freesteam the GPL steam table library

## Copyright 2009 Grant Ingram, this program is distributed under the
## terms of the GNU General Public License
## Author e-mail: g.l.ingram@durham.ac.uk

##     This program is free software; you can redistribute it and/or
##     modify it under the terms of the GNU General Public License as
##     published by the Free Software Foundation; either version 2 of
##     the License, or (at your option) any later version.

##     This program is distributed in the hope that it will be useful,
##     but WITHOUT ANY WARRANTY; without even the implied warranty of
##     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##     GNU General Public License for more details.

##     You should have received a copy of the GNU General Public
##     License along with this program; if not, write to the Free
##     Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
##     Boston, MA 02110-1301, USA.

# Note if you have installed freesteam but get errors saying it can't
# find the library the following might help:
# LD_LIBRARY_PATH=/usr/local/lib
# export LD_LIBRARY_PATH

from freesteam import *
from pylab import *

Ttriple = 0.01 # Ideally this would be freesteam.TTRIPLE ?
ptriple = 0.00611

def temperature_table(T_range,caption,fout):

    fout.write(r"""\begin{landscape}
    \begin{table}
    \renewcommand{\tabcolsep}{0.6cm}
    \small
    \centering
    \begin{tabular}{ c c c c c c c c c c c }
      & & \multicolumn{2}{c}{Density} & \multicolumn{2}{c}{Internal energy} & \multicolumn{2}{c}{Specific enthalpy} & \multicolumn{2}{c}{Specific entropy}\\
      & & \multicolumn{2}{c}{$\unit{kg/m^3}$} & \multicolumn{2}{c}{$\unit{kJ/kg}$} & \multicolumn{2}{c}{$\unit{kJ/kg}$} & \multicolumn{2}{c}{$\unit{kJ/kg K}$} \\ \cline{3-4} 
      % & & \multicolumn{2}{c}{$\underline{\hphantom{aaaaaaaaa}}$}\\
    temp & pressure & Water & Steam \\
    $T \quad \unit{^{\circ}C} $ & $p \quad \unit{bar} $ & $\rho_f$ & $\rho_g$ & $u_f$ & $u_g$ & $h_f$ & $h_g$ & $s_f$ & $s_g$ \\[2pt]
    \hline
    \\[2pt]
    """)

    for T in T_range:
        W = region4_Tx(T+273.15,0) # water
        V = region4_Tx(T+273.15,1) # vapour

        fout.write(r"%3.2f & %4.3f & %4.1f & %4.3f & %4.1f & %4.1f & %4.1f & %4.1f & %4.3f & %4.3f \\" \
                   % (T,V.p/1e5,W.rho,V.rho,W.u/1000,V.u/1000,W.h/1000,V.h/1000,W.s/1000,V.s/1000))
        fout.write("\n")
        
    fout.write(r"\\[3pt]\hline")
    fout.write(r"\end{tabular}")
    fout.write("\n")
    fout.write(r"\caption{%s}" % caption)
    fout.write("\n")
    fout.write("""\end{table}
    \end{landscape}""")

def pressure_table(p_range,caption,fout):
    fout.write(r"""\begin{landscape}
    \begin{table}
    \centering
    \begin{tabular}{ c c c c c c c c c c c }
    $p$ & $T$ & $\rho_f$ & $\rho_g$ & $u_f$ & $u_g$ & $h_f$ & $h_g$ & $s_f$ & $s_g$ \\
    $[\unit{bar}]$ & $[\unit{^\circ C}]$ & $[\unit{kg/m^3}]$ & $[\unit{kg/m^3}]$ & $[\unit{kJ/kg}]$ & $[\unit{kJ/kg}]$ & $[\unit{kJ/kg}]$ & $[\unit{kJ/kg}]$ & $[\unit{kJ/kg K}]$ & $[\unit{kJ/kg K}]$ \\
    \hline
    """)
    for p in p_range:
        T = Tsat_p(p*1e5)
        T = T - 273.15
        W = region4_Tx(T+273.15,0) # water
        V = region4_Tx(T+273.15,1) # vapour

        fout.write(r"%4.3f & %3.2f & %4.1f & %4.3f & %4.1f & %4.1f & %4.1f & %4.1f & %4.3f & %4.3f \\" \
                   % (V.p/1e5,T,W.rho,V.rho,W.u/1000,V.u/1000,W.h/1000,V.h/1000,W.s/1000,V.s/1000))
        fout.write("\n")
        

    fout.write(r"\end{tabular}")
    fout.write("\n")
    fout.write(r"\caption{%s}" % caption)
    fout.write("\n")
    fout.write("""\end{table}
    \end{landscape}""")

def superheat_table(caption,variable,fout,p_range,t_range):
    fout.write(r"""\begin{landscape}
    \begin{table}
    \centering
    \begin{tabular}{ c c c c c c c c c c c c c c c c c c c c }
    """)

    # Do pressure header 
    fout.write(r"$p$ / [$bar$] ")
    for i in p_range:
        fout.write(r"& %4.1f " % i )
    fout.write(r"\\")

    fout.write("\n")
    # Do saturate temp header
    fout.write(r"$T_{sat}$ / [$^\circ C$] ")
    for i in p_range:
        fout.write(r"& %4.1f " % (Tsat_p(i*1e5) - 273.15) )
    fout.write(r"\\")
    fout.write("\n")
    fout.write(r"\hline")

    # Temperature header line
    if variable == "enthalpy":
        variable_label = r"Specific Enthalpy / [$\unit{kJ/kg}$]"
    elif variable == "entropy":
        variable_label = r"Specific Entropy / [$\unit{kJ/kg K}$]"
    elif variable == "density":
        variable_label = r"Density / [$\unit{kg/m^3}$]"
    elif variable == "internal":
        variable_label = r"Specific Internal Energy / [$\unit{kJ/kg}$]"
    else:
        print "Option not recognised"
        raise SystemExit
    fout.write(r"$T$/[$^\circ C$] & \multicolumn{%d}{c}{%s} \\" % ((len(p_range)-1),variable_label))
    fout.write("\n")
    
    for i in t_range:
        fout.write(r" %3.0f " % i)
        for j in p_range:
            S = steam_pT(j*1e5,i+273.15)
            if variable == "enthalpy":
                data = round((S.h / 1000),2)
                fout.write(r"& %4.4g " %  data)
            elif variable == "entropy":
                data = round((S.s / 1000),3)
                fout.write(r"& %4.4g " %  data)
            elif variable == "density":
                data = round(S.rho,3)
                fout.write(r"& %4.4g " %  data)
            elif variable == "internal":
                data = round((S.u / 1000),2)
                fout.write(r"& %4.4g " %  data)
            else:
                print "Option not recognised"
                raise SystemExit

        fout.write(r"\\")
        fout.write("\n")


    fout.write(r"\end{tabular}")
    fout.write("\n")
    fout.write(r"\caption{%s}" % caption)
    fout.write("\n")
    fout.write("""\end{table}
    \end{landscape}""")
    
#    $p$ & $T$ & $\rho_f$ & $\rho_g$ & $u_f$ & $u_g$ & $h_f$ & $h_g$ & $s_f$ & $s_g$ \\
#    $[bar]$ & $[^\circ C]$ & $[kg/m^3]$ & $[kg/m^3]$ & $[kJ/kg]$ & $[kJ/kg]$ & $[kJ/kg]$ & $[kJ/kg]$ & $[kJ/kg K]$ & $[kJ/kg K]$ \\
#    \hline
#    """)

def thermophys_table(caption, T_range):

	fout.write(r"""
	\begin{table}
	\centering
	\begin{tabular}{ c              c             c            c              c           c }
		             $T$          & $c_p$       & $\rho$     & $\mu$        & $k$       & $\mathrm{Pr}$ \\
		             $\mathrm{[^\circ C]}$ & $\mathrm{[kJ/kg \cdot K]}$ & $\mathrm{[kg/m^3]}$ & $\mathrm{[Pa \cdot s]}$ & $\mathrm{[W/m \cdot K]}$ & $$ \\
	\hline
	""")

	for T in T_range:
		S = steam_Tx(T + 273.15, 0)
	
		k = S.k
		mu = S.mu
		cp = S.cp
		Pr = cp * mu / k
		fout.write(r"%3.2f & %4.3f & %4.1f & %4.3e & %4.3f & %4.3f \\" \
			% (T, cp/1e3, S.rho, mu, k, Pr)
		)
		fout.write("\n")
		

	fout.write(r"\end{tabular}")
	fout.write("\n")
	fout.write(r"\caption{%s}" % caption)
	fout.write("\n")
	fout.write("""\end{table}\n""")

print "tables.py - script to get data for Steam Tables"

# Create a latex file
fout = open("steamtable.tex","w")
fout.write(r"""\documentclass[a4paper,11pt]{article}
\usepackage{graphicx}
\usepackage{lscape}
%\usepackage[scaled=.92]{helvet}
\usepackage[hang, small, bf]{caption}
\usepackage{amssymb}
\usepackage{units}
\renewcommand{\familydefault}{\sfdefault}
\author{Scripted by Grant Ingram and John Pye}
\title{Steam Tables calculated using freesteam http://freesteam.sf.net}
\date{\today}
\begin{document}
\maketitle
""")

version_string = "Calculated with freesteam v%s using the IAPWS-IF97 Industrial Formulation \n \listoftables \n \listoffigures" % FREESTEAM_VERSION

fout.write(version_string)

print "Creating Table 7..."
# Equivalent to Table 7 in Haywood Steam Tables: Saturated Water and
# Steam by Temperature from Triple Point to 100 deg C
# Actually we split into two tables 7a and 7b so as to make typesetting easier

#Table 7A
T_range = [Ttriple] + range(2,51,2) # Range of table in deg C
caption = r"Saturated Water and Steam (Triple Point to 50$\unit{^\circ C}$)"
temperature_table(T_range,caption,fout)

#Table 7B
T_range = range(50,101,2) # Range of table in deg C
caption = r"Saturated Water and Steam (50 to 100 $\unit{^\circ C}$)"
temperature_table(T_range,caption,fout)

print "Creating Table 8..."
#Table 8 - values by pressure all the way up to the crtical point....

# Given the non-uniform spacing here sometimes the manual way is the best...
p_range = (ptriple,0.008,0.01,0.012,0.014,0.016,0.018,0.020,0.022,0.024,0.026,0.028,0.030,0.035,0.040,0.045, \
           0.050,0.06,0.07,0.08,0.09,0.1,0.12,0.13,0.14,0.15)
caption = r"Saturated Water and Steam (0.00611 to 0.15 $\unit{bar}$)"
pressure_table(p_range,caption,fout)

#Table 8B
p_range = (0.16,0.18,0.20,0.22,0.24,0.26,0.28,0.30,0.35,0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.90,0.95,1.00)
caption = r"Saturated Water and Steam (0.16 to 1 $\unit{bar}$)"
pressure_table(p_range,caption,fout)

#Table 8C
p_range = (1,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2,2.2,2.4,2.6,2.8,3,3.2,3.4,3.6,3.8,4,4.2,4.4,4.6,4.8,5,5.5,6,6.5,7)
caption = r"Saturated Water and Steam (1 to 7 $\unit{bar}$)"
pressure_table(p_range,caption,fout)

#Table 8D
p_range = (7.5,8,8.5,9,9.5,10,10.5,11,11.5,12,12.5,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30)
caption = r"Saturated Water and Steam (7.5 to 30 $\unit{bar}$)"
pressure_table(p_range,caption,fout)

#Table 8D
p_range = (30,32,34,36,38,40,42,44,46,48,50,52,54,56,58,60,62,64,66,68,70,72,74,76,78,80,82,84,86,88)
caption = r"Saturated Water and Steam (30 to 88 $\unit{bar}$)"
pressure_table(p_range,caption,fout)

#Table 8D
p_range = (90,92,94,96,98,100,105,110,115,120,125,130,135,140,145,150,155,160,165,170,175,180,185,190,195,200,205,210,215,220)
caption = r"Saturated Water and Steam (90 to 220 $\unit{bar}$)"
pressure_table(p_range,caption,fout)

print "Creating Table 9,10,11 and 12"
p_range = [0.1,0.5,1,5,10,20,40,60,80,100,150,200,250,300,400,500]
t_range = [0,25,50,75,100,125,150,175,200,225,250,275,300,350,400,450,500,550,600,650,700,750,800]
superheat_table("Enthalpy of Water and Steam","enthalpy",fout,p_range,t_range)
superheat_table("Entropy of Water and Steam","entropy",fout,p_range,t_range)
superheat_table("Density of Water and Steam","density",fout,p_range,t_range)
superheat_table("Internal Energy of Water and Steam","internal",fout,p_range,t_range)

print "Creating thermophysical properties table"
t_range = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,110,120,130,140,150,160,180,200,220,240,260,280,300,320,340,360, 370]
thermophys_table("Transport properties of water (saturated liquid)",t_range)

print "including hsdiagram"
fout.write(r"""

\begin{figure}
\centering
\includegraphics[width=1.00\textwidth]{mollier}
\caption{Enthalpy-Entropy Diagram}
\label{fig:hsdiag}
\end{figure}

""")

fout.write("\end{document}")
fout.close
