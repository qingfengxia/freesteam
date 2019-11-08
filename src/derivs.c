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
#define FREESTEAM_BUILDING_LIB
#include "derivs.h"

#include "region1.h"
#include "region2.h"
#include "region3.h"
#include "region4.h"

#include <stdlib.h>
#include <assert.h>
#include <math.h>

/* forward decls */

/*
The following functions basically look up the contents of Table 1 and Table 2
from the IAPWS Guideline.
*/

/*
The following are the functions

	 ⎰ ∂z ⎱   ___\   VTn
	 ⎱ ∂v ⎰T     /

etc., for each of the different regions (n).
*/

#define TV3 freesteam_region3_dAdTv
#define VT3 freesteam_region3_dAdvT
#define PT1 freesteam_region1_dAdpT
#define TP1 freesteam_region1_dAdTp
#define PT2 freesteam_region2_dAdpT
#define TP2 freesteam_region2_dAdTp
#define TX4 freesteam_region4_dAdTx
#define XT4 freesteam_region4_dAdxT

PartialDerivFn PT1, TP1, PT2, TP2, TV3, VT3, TX4, XT4;
/*------------------------------------------------------------------------------
  EXPORTED FUNCTION(S)
*/

/**
	Calculates the derivative 

	 ⎰ ∂z ⎱
	 ⎱ ∂x ⎰y

	@param S steam state, already calculated using steam_ph, etc.
	@param x in above equation, character one of 'pTvuhsgaf'.
	@param y in above equation, character one of pTvuhsgaf.
	@param z in above equation, character one of pTvuhsgaf.
	Note that Helmholtz free energy can be signified by either 'a' or 'f'.

	@NOTE that the variables ARE NOT IN ALPHABETICAL ORDER.

	@return the numerical value of the derivative (∂z/∂x)y.
*/
double freesteam_deriv(SteamState S, char xyz[3]){
	char x = xyz[0];
	char y = xyz[1];
	char z = xyz[2];

	PartialDerivFn *AB, *BA;

	//fprintf(stderr,"CALCULATING (∂%c/∂%c)%c... ",z,x,y);
	//freesteam_fprint(stderr,S);
	switch(S.region){
		case 1:	AB = PT1; BA = TP1; break;
		case 2: AB = PT2, BA = TP2; break;
		case 3: AB = VT3; BA = TV3; break;
		case 4: AB = TX4; BA = XT4; break;
		default:
			fprintf(stderr,"ERROR: %s (%s:%d) Invalid or not-implemented region '%d' while evalulating (∂%c/∂%c)%c\n"
				,__func__,__FILE__,__LINE__,S.region,z,x,y
			);
			exit(1);
	}
	double ZAB = (*AB)(z,S);
	double ZBA = (*BA)(z,S);
	double XAB = (*AB)(x,S);
	double XBA = (*BA)(x,S);
	double YAB = (*AB)(y,S);
	double YBA = (*BA)(y,S);
	double deriv = ((ZAB*YBA-ZBA*YAB)/(XAB*YBA-XBA*YAB));
	//fprintf(stderr,"Calculated (∂%c/∂%c)%c = %g\n",z,x,y,deriv);
	return deriv;
}

/*------------------------------------------------------------------------------
  REGION 3 DERIVATIVES
*/

/*
FIXME the following macros avoid calculating unneeded results eg within VT3 
but at the level of freesteam_deriv, there is wasted effort, because eg 'p' 
will be calculated several times in different calls to VT3.
*/
#define rho S.R3.rho
#define T S.R3.T
#define p freesteam_region3_p_rhoT(rho,T)
#define cv freesteam_region3_cv_rhoT(rho,T)
#define v (1./rho)
#define s freesteam_region3_s_rhoT(rho,T)
#define alphap freesteam_region3_alphap_rhoT(rho,T)
#define betap freesteam_region3_betap_rhoT(rho,T)

/**
	TODO convert char to enum for better compiler checking capability
*/
double freesteam_region3_dAdvT(FREESTEAM_CHAR x, SteamState S){
	double res;
	switch(x){
		case 'p': res = -p*betap; break;
		case 'T': res = 0; break;
		case 'v': res = 1; break;
		case 'u': res = p*(T*alphap-1.); break;
		case 'h': res = p*(T*alphap-v*betap); break;
		case 's': res = p*alphap; break;
		case 'g': res = -p*v*betap; break;
		case 'a':
		case 'f': res = -p; break;
		default:
			fprintf(stderr,"%s (%s:%d): Invalid variable '%c'\n", __func__,__FILE__,__LINE__,x);
			exit(1);
	}
	//fprintf(stderr,"(∂%c/∂v)T = %f\n",x,res);
	return res;
}

double freesteam_region3_dAdTv(FREESTEAM_CHAR x, SteamState S){
	double res;
	switch(x){
		case 'p': res = p*alphap; break;
		case 'T': res = 1; break;
		case 'v': res = 0; break;
		case 'u': res = cv; break;
		case 'h': res = cv + p*v*alphap; break;
		case 's': res = cv/T; break;
		case 'g': res = p*v*alphap - s; break;
		case 'a':
		case 'f': res = -s; break;
		default:
			fprintf(stderr,"%s (%s:%d): Invalid variable '%c'\n", __func__,__FILE__,__LINE__,x);
			exit(1);
	}
	//fprintf(stderr,"(∂%c/∂T)v = %f\n",x,res);
	return res;
}

#undef rho
#undef T
#undef p
#undef cv
#undef v
#undef s
#undef alphap
#undef betap

/*------------------------------------------------------------------------------
  REGION 1 DERIVATIVES
*/

#define p S.R1.p
#define T S.R1.T
#define cp freesteam_region1_cp_pT(p,T)
#define v freesteam_region1_v_pT(p,T)
#define s freesteam_region1_s_pT(p,T)
#define alphav freesteam_region1_alphav_pT(p,T)
#define kappaT freesteam_region1_kappaT_pT(p,T)

/**
	TODO convert char to enum for better compiler checking capability
*/
double freesteam_region1_dAdTp(FREESTEAM_CHAR x, SteamState S){
	double res;
	switch(x){
		case 'p': res = 0; break;
		case 'T': res = 1; break;
		case 'v': res = v*alphav; break;
		case 'u': res = cp-p*v*alphav; break;
		case 'h': res = cp; break;
		case 's': res = cp/T; break;
		case 'g': res = -s; break;
		case 'a':
		case 'f': res = -p*v*alphav-s; break;
		default:
			fprintf(stderr,"%s (%s:%d): Invalid character x = '%c'\n", __func__,__FILE__,__LINE__,x);
			exit(1);
	}
#if 0
	fprintf(stderr,"(∂%c/∂T)p = %g\n",x,res);
#endif
	return res;
}

double freesteam_region1_dAdpT(FREESTEAM_CHAR x, SteamState S){
	double res;
	switch(x){
		case 'p': res = 1; break;
		case 'T': res = 0; break;
		case 'v': res = -v*kappaT; break;
		case 'u': res = v*(p*kappaT-T*alphav); break;
		case 'h': res = v*(1.-T*alphav); break;
		case 's': res = -v*alphav; break;
		case 'g': res = v; break;
		case 'a':
		case 'f': res = p*v*kappaT; break;
		default:
			fprintf(stderr,"%s (%s:%d): Invalid character x = '%c'\n", __func__,__FILE__,__LINE__,x);
			exit(1);
	}
#if 0
	fprintf(stderr,"(∂%c/∂p)T = %g\n",x,res);
#endif
	return res;
}

#undef p
#undef T
#undef cp
#undef v
#undef s
#undef alphav
#undef kappaT


/*------------------------------------------------------------------------------
  REGION 2 DERIVATIVES
*/

#define p S.R2.p
#define T S.R2.T
#define cp freesteam_region2_cp_pT(p,T)
#define v freesteam_region2_v_pT(p,T)
#define s freesteam_region2_s_pT(p,T)
#define alphav freesteam_region2_alphav_pT(p,T)
#define kappaT freesteam_region2_kappaT_pT(p,T)

/**
	TODO convert char to enum for better compiler checking capability
*/
double freesteam_region2_dAdTp(FREESTEAM_CHAR x, SteamState S){
	double res;
	switch(x){
		case 'p': res = 0; break;
		case 'T': res = 1; break;
		case 'v': res = v*alphav; break;
		case 'u': res = cp-p*v*alphav; break;
		case 'h': res = cp; break;
		case 's': res = cp/T; break;
		case 'g': res = -s; break;
		case 'a':
		case 'f': res = -p*v*alphav-s; break;
		default:
			fprintf(stderr,"%s (%s:%d): Invalid character x = '%c'\n", __func__,__FILE__,__LINE__,x);
			exit(1);
	}
#if 0
	fprintf(stderr,"(∂%c/∂T)p = %g\n",x,res);
	if(x=='v'){
		fprintf(stderr,"(∂ρ/∂T)p = %g\n",-1/SQ(v)*res);
	}
#endif
	return res;
}

double freesteam_region2_dAdpT(FREESTEAM_CHAR x, SteamState S){
	double res;
	switch(x){
		case 'p': res = 1; break;
		case 'T': res = 0; break;
		case 'v': res = -v*kappaT; break;
		case 'u': res = v*(p*kappaT-T*alphav); break;
		case 'h': res = v*(1.-T*alphav); break;
		case 's': res = -v*alphav; break;
		case 'g': res = v; break;
		case 'a':
		case 'f': res = p*v*kappaT; break;
		default:
			fprintf(stderr,"%s (%s:%d): Invalid character x = '%c'\n", __func__,__FILE__,__LINE__,x);
			exit(1);
	}
#if 0
	fprintf(stderr,"(∂%c/∂p)T = %g\n",x,res);
	if(x=='v'){
		fprintf(stderr,"(∂ρ/∂p)T = %g\n",-1/SQ(v)*res);
	}
#endif
	return res;
}

#undef p
#undef T
#undef cp
#undef v
#undef s
#undef alphav
#undef kappaT

/*------------------------------------------------------------------------------
  REGION 4 DERIVATIVES

In region 4, we use (T,x) as coordinates, so we can express general derivatives
in terms of (∂z/∂T)x and (∂z/∂x)T.
*/

/*
	⎰ ∂z ⎱   =  ⎰∂z_f⎱ (1 - x) + ⎰∂z_f⎱ x
	⎱ ∂T ⎰x     ⎱ ∂T ⎰           ⎱ ∂T ⎰
*/
double freesteam_region4_dAdTx(FREESTEAM_CHAR z, SteamState S){
	double res;
#define T S.R4.T
	switch(z){
		case 'p': res = freesteam_region4_dpsatdT_T(T); return res;
		case 'T': res = 1; return res;
		case 'x': res = 0; return res;
	}

	//fprintf(stderr,"%s: T = %g\n",__func__,T);
	assert(!isnan(T));

	double dzfdT, dzgdT;
	if(T < REGION1_TMAX){
		//fprintf(stderr,"%s: below REGION1_TMAX\n",__func__);
		double psat = freesteam_region4_psat_T(T);
		SteamState Sf = freesteam_region1_set_pT(psat,T);
		SteamState Sg = freesteam_region2_set_pT(psat,T);
		double dpsatdT = freesteam_region4_dpsatdT_T(T);
		dzfdT = PT1(z,Sf)*dpsatdT + TP1(z,Sf);
		dzgdT = PT2(z,Sg)*dpsatdT + TP2(z,Sg);
	}else{
		double rhof = freesteam_region4_rhof_T(T);
		double rhog = freesteam_region4_rhog_T(T);
		assert(rhof!=0);
		assert(rhog!=0);
		SteamState Sf = freesteam_region3_set_rhoT(rhof,T);
		SteamState Sg = freesteam_region3_set_rhoT(rhog,T);
		double dvfdT = -1./SQ(rhof) * freesteam_drhofdT_T(T);
		assert(!isnan(dvfdT));
		double dvgdT = -1./SQ(rhog) * freesteam_drhogdT_T(T);
		assert(!isnan(dvgdT));
		dzfdT = VT3(z,Sf)*dvfdT + TV3(z,Sf);
		dzgdT = VT3(z,Sg)*dvgdT + TV3(z,Sg);
	}
	assert(!isnan(dzfdT));
	assert(!isnan(dzgdT));
#define x S.R4.x
	res = dzfdT*(1-x) + dzgdT*x;
	//fprintf(stderr,"(∂%c/∂T)x = %g\n",z,res);
	return res;
#undef T
#undef x
}

#define ZFG(Z,P,T) \
	zf = freesteam_region1_##Z##_pT(P,T);\
	zg = freesteam_region2_##Z##_pT(P,T);

/*
	These derivatives are simply the gradient within the two-phase region,
	and is very simply calculated as

	⎰ ∂z ⎱   =  z_g - z_f  where z in {v,u,h,z,s,g,a}.
	⎱ ∂x ⎰T

	or, otherwise,

	⎰ ∂T ⎱  , ⎰ ∂p ⎱    = 0
	⎱ ∂x ⎰T   ⎱ ∂x ⎰T

*/	
double freesteam_region4_dAdxT(FREESTEAM_CHAR z, SteamState S){
	switch(z){
		case 'p': return 0;
		case 'T': return 0;
		case 'x': return 1;
	}
#define T S.R4.T
#define x S.R4.x
	double p = freesteam_region4_psat_T(T);
	double zf, zg;
	switch(z){
		case 'v': ZFG(v,p,T); break;
		case 'u': ZFG(u,p,T); break;
		case 'h': ZFG(h,p,T); break;
		case 's': ZFG(s,p,T); break;
		case 'g': ZFG(g,p,T); break;
		case 'a': case 'f': ZFG(a,p,T); break;
		default:
			fprintf(stderr,"%s (%s:%d): Invalid character x = '%c'\n", __func__,__FILE__,__LINE__,z);
			exit(1);
	}
	//fprintf(stderr,"(∂%c/∂x)T = %g\n",z,zg-zf);
	return zg - zf;
}
#undef T
#undef x
#undef ZFG

/*------------------------------------------------------------------------------
  DERIVATIVES OF rhof and rhog with temperature
*/

double freesteam_drhofdT_T(double T){
	double dpsatdT = freesteam_region4_dpsatdT_T(T);
	if(T < REGION1_TMAX){
		double psat = freesteam_region4_psat_T(T);
		SteamState Sf = freesteam_region1_set_pT(psat,T);
		double vf = freesteam_v(Sf);
		return -1./SQ(vf) * (PT1('v',Sf) * dpsatdT + TP1('v',Sf));
	}else{
		/* FIXME: add iterative refinement of value of rhof */
		double rhof = freesteam_region4_rhof_T(T);
		SteamState Sf = freesteam_region3_set_rhoT(rhof,T);
		double dpdT = TV3('p',Sf);
		double dpdrho = -1./SQ(rhof) * VT3('p',Sf);
		return (dpsatdT - dpdT)/dpdrho;
	}
}

double freesteam_drhogdT_T(double T){
	double dpsatdT = freesteam_region4_dpsatdT_T(T);
	double rhog = freesteam_region4_rhog_T(T);
	if(T < REGION1_TMAX){
		double psat = freesteam_region4_psat_T(T);
		SteamState Sg = freesteam_region2_set_pT(psat,T);
		double vf = freesteam_v(Sg);
		return -1./SQ(vf) * (PT2('v',Sg) * dpsatdT + TP2('v',Sg));
	}else{
		SteamState Sg = freesteam_region3_set_rhoT(rhog,T);
		double dpdT = TV3('p',Sg);
		double dpdrho = -1./SQ(rhog) * VT3('p',Sg);
		return (dpsatdT - dpdT)/dpdrho;
	}
}

