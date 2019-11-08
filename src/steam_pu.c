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
#include "steam_pu.h"

#include "region1.h"
#include "region2.h"
#include "region3.h"
#include "region4.h"
#include "b23.h"
#include "backwards.h"
#include "zeroin.h"
#include "solver2.h"

#include "common.h"

#include <stdio.h>
#include <stdlib.h>

int freesteam_region_pu(double p, double u){
	double p13 = freesteam_region4_psat_T(REGION1_TMAX);
	if(p < p13){
		double Tsat = freesteam_region4_Tsat_p(p);
		double uf = freesteam_region1_u_pT(p,Tsat);
		if(u < uf)return 1;
		double ug = freesteam_region2_u_pT(p,Tsat);
		if(u > ug)return 2;
		return 4;
	}
	double u13 = freesteam_region1_u_pT(p,REGION1_TMAX);
	if(u < u13){
		return 1;
	}
	double T23 = freesteam_b23_T_p(p);
	double u23 = freesteam_region2_u_pT(p,T23);
	if(u > u23){
		return 2;
	}

	if(p > IAPWS97_PCRIT)return 3;

	/* FIXME what we really need here is a psat(u) function! The current method
	is singular. */
	
	double Tsat = freesteam_region4_Tsat_p(p);
	double rhof = freesteam_region4_rhof_T(Tsat);
	double uf = freesteam_region3_u_rhoT(rhof,Tsat);
	if(u<uf) return 3;
	double rhog = freesteam_region4_rhog_T(Tsat);
	double ug = freesteam_region3_u_rhoT(rhog,Tsat);
	if(u>ug)return 3;
	return 4;
}

typedef struct{
	double p, u, T;
} SolvePUData;

#define D ((SolvePUData *)user_data)
static ZeroInSubjectFunction pu_region1_fn, pu_region2_fn, pu_region4_fn;
double pu_region1_fn(double T, void *user_data){
	return D->u - freesteam_region1_u_pT(D->p, T);
}
double pu_region2_fn(double T, void *user_data){
	return D->u - freesteam_region2_u_pT(D->p, T);
}
double pu_region4_fn(double x, void *user_data){
	return D->u - freesteam_region4_u_Tx(D->T, x);
}
#undef D

SteamState freesteam_set_pu(double p, double u){
	double lb, ub, tol, sol, err;
	SolvePUData D = {p, u, 0.};
	SteamState S;

	int region = freesteam_region_pu(p,u);
	switch(region){
		case 1:
			lb = IAPWS97_TMIN;
			ub = REGION1_TMAX;
			tol = 1e-9; /* ??? */
			zeroin_solve(&pu_region1_fn, &D, lb, ub, tol, &sol, &err);
			S = freesteam_region1_set_pT(p,sol);
			break;
		case 2:
			lb = IAPWS97_TMIN;
			ub = REGION2_TMAX;
			tol = 1e-9; /* ??? */
			zeroin_solve(&pu_region2_fn, &D, lb, ub, tol, &sol, &err);
			S = freesteam_region2_set_pT(p,sol);
			break;
		case 4:
			lb = 0.;
			ub = 1.;
			tol = 1e-9; /* ??? */
			D.T = freesteam_region4_Tsat_p(p);
			//fprintf(stderr,"%s: (%s:%d): p = %g\n",__func__,__FILE__,__LINE__,D.p);
			zeroin_solve(&pu_region4_fn, &D, lb, ub, tol, &sol, &err);
			S = freesteam_region4_set_Tx(D.T,sol);
			break;
		case 3:
		/* FIXME looks like a problem with the derivative routines here? */
			{
				int status;
				SteamState guess = freesteam_region3_set_rhoT(IAPWS97_RHOCRIT,IAPWS97_TCRIT);
				S = freesteam_solver2_region3('p','u', p, u, guess, &status);
				if(status){
					fprintf(stderr,"%s (%s:%d): Failed solve in region 3 for (p = %g MPa, u = %g kJ/kg\n"
						,__func__,__FILE__,__LINE__,p/1e6,u/1e3);
					//exit(1);
				}
			}
			break;
		default:
			fprintf(stderr,"%s (%s:%d): Region '%d' not implemented\n",__func__,__FILE__,__LINE__,region);
			exit(1);
	}
	return S;
}


