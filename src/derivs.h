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
#ifndef FREESTEAM_DERIVS_H
#define FREESTEAM_DERIVS_H

#include "common.h"
#include "steam.h"

/*
These functions are drawn from the IAPWS Guidelines document "Revised Advisory
Note No. 3 Thermodynamic Derivatives from IAPWS Formulations". (2008).
*/

/**
	@param xyz is a 3-char string containing the names of the variables x y z
	in the a derivative (dx/dy)_z, ie partial derivative of x wrt y holding z
	constant. Valid variables for this function are p T v u h s g a f. Note
	that speed of sound and specific heat capacities are NOT in the list at this
	stage.

	It was problematic having three different char constants, because of the
	way C handles character constants versus how SWIG would like to wrap this 
	function for use in Python.
	http://stackoverflow.com/questions/433895/why-are-c-character-literals-ints-instead-of-chars
 */
FREESTEAM_DLL double freesteam_deriv(SteamState S, char xyz[3]);

FREESTEAM_DLL double freesteam_drhofdT_T(double T);
FREESTEAM_DLL double freesteam_drhogdT_T(double T);

/* region-by-region derivative functions */
typedef double PartialDerivFn(FREESTEAM_CHAR,SteamState);
FREESTEAM_DLL double freesteam_region3_dAdvT(FREESTEAM_CHAR,SteamState);
FREESTEAM_DLL double freesteam_region3_dAdTv(FREESTEAM_CHAR,SteamState);
FREESTEAM_DLL double freesteam_region1_dAdTp(FREESTEAM_CHAR,SteamState);
FREESTEAM_DLL double freesteam_region1_dAdpT(FREESTEAM_CHAR,SteamState);
FREESTEAM_DLL double freesteam_region2_dAdTp(FREESTEAM_CHAR,SteamState);
FREESTEAM_DLL double freesteam_region2_dAdpT(FREESTEAM_CHAR,SteamState);
FREESTEAM_DLL double freesteam_region4_dAdTx(FREESTEAM_CHAR,SteamState);
FREESTEAM_DLL double freesteam_region4_dAdxT(FREESTEAM_CHAR,SteamState);



#endif

