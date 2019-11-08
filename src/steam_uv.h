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
#ifndef FREESTEAM_STEAMUV_H
#define FREESTEAM_STEAMUV_H

#include "common.h"
#include "steam.h"

/*
	Warning: the routines that calculate steam properties as functions of
	(u,v) are generally more computationally intensive that alternative
	functions. It is suggested that you attempt to make use of other
	forms of your governing equations, if possible, perhaps for example through
	the use of transformations such as those of the 'T dS' equations.
*/
FREESTEAM_DLL int freesteam_bounds_uv(double u, double v, int verbose);

FREESTEAM_DLL int freesteam_region_uv(double u, double v);

FREESTEAM_DLL SteamState freesteam_set_uv(double u, double v);

#endif

