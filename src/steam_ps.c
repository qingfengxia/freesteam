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
#include "steam_ps.h"

#include "region1.h"
#include "region2.h"
#include "region3.h"
#include "region4.h"
#include "zeroin.h"
#include "b23.h"
#include "solver2.h"
#include "backwards.h"

#include <stdlib.h>

int freesteam_bounds_ps(double p, double s, int verbose){
	if(p < 0){
		if(verbose){
			fprintf(stderr,"%s (%s:%d): WARNING p < 0 (p = %g MPa, s = %g kJ/kgK)\n"
			,__func__,__FILE__,__LINE__,p/1e6,s/1e3);
		}
		return 1;
	}
	if(p > IAPWS97_PMAX){
		if(verbose){
			fprintf(stderr,"%s (%s:%d): WARNING p > PMAX (p = %g MPa, s = %g kJ/kgK)\n"
				,__func__,__FILE__,__LINE__,p/1e6,s/1e3);
		}
		return 2;
	}
	double smin = freesteam_region1_s_pT(p, IAPWS97_TMIN);
	if(s < smin){
		if(verbose){
			fprintf(stderr,"%s (%s:%d): WARNING s < smin (p = %g MPa, s = %g kJ/kgK)\n"
				,__func__,__FILE__,__LINE__,p/1e6,s/1e3);
		}
		return 3;
	}
	double smax = freesteam_region2_s_pT(p, IAPWS97_TMAX);
	if(s > smax){
		if(verbose){
			fprintf(stderr,"%s (%s:%d): WARNING s > smax (p = %g MPa, s = %g kJ/kgK)\n"
				,__func__,__FILE__,__LINE__,p/1e6,s/1e3);
		}
		return 4;
	}
	return 0;
}

int freesteam_region_ps(double p, double s){
	// FIXME add test/warning for max S

	// FIXME check p > min p, p < max p, s > 0

	if(p <= freesteam_region4_psat_T(REGION1_TMAX)){
		double T = freesteam_region4_Tsat_p(p);
		double sf = freesteam_region1_s_pT(p,T);
		double sg = freesteam_region2_s_pT(p,T);
		if(s <= sf){
			return 1;
		}
		if(s >= sg){
			return 2;
		}
		return 4;
	}

	/* FIXME solve for s_b13(p) */
	double s_b13 = freesteam_region1_s_pT(p, REGION1_TMAX);

	if(s <= s_b13){
		return 1;
	}

	/* FIXME solve for s_b23(p) */
	double T_b23 = freesteam_b23_T_p(p);
	double s_b23 = freesteam_region2_s_pT(p,T_b23);
	if(s >= s_b23){
		return 2;
	}

	if(p < IAPWS97_PCRIT){ /* but not in region 1/2 */
		double T = freesteam_region4_Tsat_p(p);
		double rhof = freesteam_region4_rhof_T(T);
		double rhog = freesteam_region4_rhog_T(T);
		double sf = freesteam_region3_s_rhoT(rhof,T);
		double sg = freesteam_region3_s_rhoT(rhog,T);
		if(s <= sf || s >= sg)return 3;
		return 4;
	}

	return 3;
}

typedef struct SolvePSData_struct{
	double p, s, T;
} SolvePSData;

#define D ((SolvePSData *)user_data)
static ZeroInSubjectFunction ps_region1_fn, ps_region2_fn, ps_region4_fn;
double ps_region1_fn(double T, void *user_data){
	return D->s - freesteam_region1_s_pT(D->p, T);
}
double ps_region2_fn(double T, void *user_data){
	return D->s - freesteam_region2_s_pT(D->p, T);
}
double ps_region4_fn(double x, void *user_data){
	double T = freesteam_region4_Tsat_p(D->p);
	return D->s - freesteam_region4_s_Tx(T, x);
}
#undef D

SteamState freesteam_set_ps(double p, double s){
	double lb, ub, tol, sol, err;
	SolvePSData D = {p, s, 0.};

	int region = freesteam_region_ps(p,s);
	switch(region){
		case 1:
			lb = IAPWS97_TMIN;
			ub = REGION1_TMAX;
			tol = 1e-9; /* ??? */
			zeroin_solve(&ps_region1_fn, &D, lb, ub, tol, &sol, &err);
			return freesteam_region1_set_pT(p,sol);
		case 2:
			lb = IAPWS97_TMIN;
			ub = REGION2_TMAX;
			tol = 1e-9; /* ??? */
			zeroin_solve(&ps_region2_fn, &D, lb, ub, tol, &sol, &err);
			return freesteam_region2_set_pT(p,sol);
		case 3:
#define USE_SOLVER_FOR_PS3
#ifdef USE_SOLVER_FOR_PS3
		/* FIXME looks like a problem with the derivative routines here? */
			{
				int status;
				double v = freesteam_region3_v_ps(p,s);
				double T = freesteam_region3_T_ps(p,s);
				SteamState guess = freesteam_region3_set_rhoT(1./v,T);
				//SteamState guess = freesteam_region3_set_rhoT(322,700);
				SteamState S = freesteam_solver2_region3('p','s', p, s, guess, &status);
				if(status){
					fprintf(stderr,"%s (%s:%d): Failed solve in region 3 for (p = %g MPa, s = %g kJ/kgK\n"
						,__func__,__FILE__,__LINE__,p/1e6,s/1e3);
					fprintf(stderr,"%s: Starting guess was ",__func__);
					freesteam_fprint(stderr,guess);
					fprintf(stderr,"%s: v = %g, T = %f => p = %g MPa, s = %g kJ/kgK\n",__func__,v,T,freesteam_p(S)/1e6,freesteam_s(S)/1e3);
					//exit(1);
				}
				return S;
			}
#else
			{
				SteamState S;
				double v = freesteam_region3_v_ps(p,s);
				double T = freesteam_region3_T_ps(p,s);
				S = freesteam_region3_set_rhoT(1./v,T);
				if((freesteam_p(S) - p) > 30000){
					fprintf(stderr,"%s (%s:%d): Failed p solution in region 3(p,s)"	
						" (p = %g MPa, s = %g kJ/kgK => v = %g m³/kg, T = %g K => p = %g\n"
						,__func__,__FILE__,__LINE__,p/1e6,s/1e3,v,T,freesteam_p(S)/1e6);
				}
				if((freesteam_s(S) - s) > 0.2){
					fprintf(stderr,"%s (%s:%d): Failed s solution in region 3(p,s)"
						" (p = %g MPa, s = %g kJ/kgK => v = %g m³/kg, T = %g K => s = %g\n"
						,__func__,__FILE__,__LINE__,p/1e6,s/1e3,v,T,freesteam_s(S)/1e3);
				}
				return S;
			}
#endif
		case 4:
			{
				lb = 0.;
				ub = 1.;
				tol = 1e-9; /* ??? */
				D.T = freesteam_region4_Tsat_p(p);
				//fprintf(stderr,"%s: (%s:%d): p = %g\n",__func__,__FILE__,__LINE__,D.p);
				zeroin_solve(&ps_region4_fn, &D, lb, ub, tol, &sol, &err);
				SteamState S = freesteam_region4_set_Tx(D.T,sol);
				//fprintf(stderr,"%s: (%s:%d): p = %g\n",__func__,__FILE__,__LINE__,D.p);
				return S;
			}
		default:
			/* ??? */
			fprintf(stderr,"%s (%s:%d): Region '%d' not implemented\n",__func__,__FILE__,__LINE__,region);
			exit(1);
	}
}


