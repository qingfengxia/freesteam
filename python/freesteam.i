/*
freesteam - IAPWS-IF97 steam tables library
Copyright (C) 2004-2009  John Pye

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
*/
%define DOCSTRING
"The freesteam module provides the ability to calculate
properties of water and steam from the IAPWS-IF97 steam
property correlations, published by the Internation
Association for the Properties of Water & Steam (IAPWS).

Freesteam is based on the IAPWS-IF97 releases, but is not
officially endorsed by IAPWS. Freesteam is written by
John Pye. Freesteam is released under the GPL license. 
You may not use it in commercially-released software."
%enddef

%feature("autodoc", "1");
%module(docstring=DOCSTRING) freesteam

%rename(SteamState) struct_SteamState_struct;

%rename(steam_ps) freesteam_set_ps;
%rename(steam_ph) freesteam_set_ph;
%rename(steam_Ts) freesteam_set_Ts;
%rename(steam_pv) freesteam_set_pv;
%rename(steam_Tx) freesteam_set_Tx;
%rename(steam_pT) freesteam_set_pT;
%rename(steam_pu) freesteam_set_pu;

%rename(bounds_ps) freesteam_bounds_ps;
%rename(bounds_ph) freesteam_bounds_ph;
%rename(bounds_Ts) freesteam_bounds_Ts;
%rename(bounds_pv) freesteam_bounds_pv;
%rename(bounds_Tx) freesteam_bounds_Tx;
%rename(bounds_pT) freesteam_bounds_pT;
%rename(bounds_pu) freesteam_bounds_pu;

%rename(region_ps) freesteam_region_ps;
%rename(region_ph) freesteam_region_ph;
%rename(region_Ts) freesteam_region_Ts;
%rename(region_pv) freesteam_region_pv;
%rename(region_Tx) freesteam_region_Tx;
%rename(region_pT) freesteam_region_pT;
%rename(region_pu) freesteam_region_pu;

%rename(bound_pmax_T) freesteam_bound_pmax_T;

%rename(solver2_region1) freesteam_solver2_region1;
%rename(solver2_region2) freesteam_solver2_region2;
%rename(solver2_region3) freesteam_solver2_region3;
%rename(solver2_region4) freesteam_solver2_region4;

%rename(region1_pT) freesteam_region1_set_pT;
%rename(region2_pT) freesteam_region2_set_pT;
%rename(region3_rhoT) freesteam_region3_set_rhoT;
%rename(region4_Tx) freesteam_region4_set_Tx;

%rename(PCRIT) IAPWS97_PCRIT;
%rename(TCRIT) IAPWS97_TCRIT;
%rename(TMIN) IAPWS97_TMIN;
%rename(RHOCRIT) IAPWS97_RHOCRIT;
%rename(PMAX) IAPWS97_PMAX;
%rename(R) IAPWS97_R;
%rename(PTRIPLE) IAPWS97_PTRIPLE;

%rename(psat_T) freesteam_region4_psat_T;
%rename(dpsatdT_T) freesteam_region4_dpsatdT_T;
%rename(Tsat_p) freesteam_region4_Tsat_p;
%rename(rhof_T) freesteam_region4_rhof_T;
%rename(rhog_T) freesteam_region4_rhog_T;
%rename(drhofdT_T) freesteam_drhofdT_T;
%rename(drhogdT_T) freesteam_drhogdT_T;
%rename(dpsatdT_T) freesteam_region4_dpsatdT_T;
%rename(surftens_T) freesteam_surftens_T;

%ignore freesteam_T;
%ignore freesteam_p;
%ignore freesteam_h;
%ignore freesteam_u;
%ignore freesteam_v;
%ignore freesteam_s;
%ignore freesteam_cp;
%ignore freesteam_cv;
%ignore freesteam_w;
%ignore freesteam_fprint;
%ignore freesteam_region;
%ignore ipow;


%{
// function prototypes for included C use -- for reading by GCC
#include "config.h"
#include "common.h"
#include "steam.h"
#include "steam_ph.h"
#include "steam_ps.h"
#include "steam_pT.h"
#include "steam_pu.h"
#include "steam_Ts.h"
#include "steam_pv.h"
#include "steam_Tx.h"
#include "region1.h"
#include "region2.h"
#include "region3.h"
#include "region4.h"
#include "derivs.h"
#include "solver2.h"
#include "bounds.h"
#include "surftens.h"
#include "viscosity.h"
%}

// steam.h

%nodefaultctor;

typedef struct{} SteamState;
SteamState freesteam_region1_set_pT(double p, double T);
SteamState freesteam_region2_set_pT(double p, double T);
SteamState freesteam_region3_set_rhoT(double rho, double T);
SteamState freesteam_region4_set_Tx(double T, double x);

%extend SteamState{
	double deriv(char *spec){
		return freesteam_deriv(*$self, spec);
	}
	%immutable;
	const int region;
	const double p;
	const double T;
	const double u;
	const double h;
	const double v;
	const double s;
	const double cp;
	const double cv;	
	const double w;
	const double rho;
	const double mu;
	const double k;
	const double x;
}

%include "config.h"
%include "common.h"

// region 4.h
double freesteam_region4_psat_T(double T);
double freesteam_region4_Tsat_p(double p);
double freesteam_region4_rhof_T(double T);
double freesteam_region4_rhog_T(double T);
double freesteam_region4_dpsatdT_T(double T);

// steam_ph.h
int freesteam_bounds_ph(double p, double h, int verbose);
int freesteam_region_ph(double p, double h);
SteamState freesteam_set_ph(double p, double h);

// steam_ps.h
int freesteam_bounds_ps(double p, double s, int verbose);
int freesteam_region_ps(double p, double s);
SteamState freesteam_set_ps(double p, double s);

// steam_pT.h
SteamState freesteam_set_pT(double p, double T);

// steam_pu.h
int freesteam_region_pu(double p, double u);
SteamState freesteam_set_pu(double p, double u);

// steam_Ts.h
int freesteam_bounds_Ts(double T, double s, int verbose);
int freesteam_region_Ts(double T, double s);
SteamState freesteam_set_Ts(double T, double s);

// steam_Tx.h
int freesteam_bounds_Tx(double T, double x, int verbose);
int freesteam_region_Tx(double T, double x);
SteamState freesteam_set_Tx(double T, double x);

// steam_pv.h
int freesteam_bounds_pv(double p, double v, int verbose);
int freesteam_region_pv(double p, double v);
SteamState freesteam_set_pv(double p, double v);

// bounds.h
SteamState freesteam_bound_pmax_T(double T);

// surftens.h
double freesteam_surftens_T(double T);

// viscosity.h
double freesteam_mu_rhoT(double rho, double T);

// derivs.h
//double freesteam_deriv(SteamState S, char xyz[3]);
%include "derivs.h"
// don't include derivs.h because we don't want all the functions taking char arguments

// NOTE: solver2 routines have been removed from the Python bindings.

%{
// implementation of getter functions

#define FNS(G,X) G(p) X G(T) X G(h) X G(u) X G(v) X G(rho) X G(x) X G(s) \
	X G(cp) X G(cv) X G(w) X G(mu) X G(k)
#define GETTER(N) \
	double SteamState_##N##_get(SteamState *state){\
		return freesteam_##N(*state);\
	}
#define SPACE
FNS(GETTER,SPACE)
#undef GETTER
#undef SPACE

int SteamState_region_get(SteamState *S){
	return (int)(S->region);
}

%}

