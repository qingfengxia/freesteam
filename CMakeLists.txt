cmake_minimum_required(VERSION 2.8.11)  # centos7

project("freesteam")
set(PROJECT_BRIEF "a free implementation of IAPWS-IF97 thermophysical properties for water and steam")

set(PACKAGE_VERSION_MAJOR "3")
set(PACKAGE_VERSION_MINOR "0")
set(PACKAGE_VERSION_PATCH "0")

# this version name is used by CPack
set(PACKAGE_VERSION_NAME ${PACKAGE_VERSION_MAJOR}.${PACKAGE_VERSION_MINOR})

set(VERSION ${PACKAGE_VERSION_MAJOR})
#configure_file()
#config.h.in

# steam_uv.c seems not yet completely implemented, comented out
set(MY_SOURCES
"src/b23.c"
"src/backwards.c"
"src/bounds.c"
"src/common.c"
"src/derivs.c"
"src/region1.c"
"src/region2.c"
"src/region3.c"
"src/region4.c"
"src/solver2.c"
"src/steam.c"
"src/steam_ph.c"
"src/steam_ps.c"
"src/steam_pT.c"
"src/steam_pu.c"
"src/steam_pv.c"
"src/steam_Ts.c"
"src/steam_Tx.c"
#"src/steam_uv.c"
"src/surftens.c"
"src/thcond.c"
"src/viscosity.c"
"src/zeroin.c"
)

set(MY_TEST_SOURCES
"src/test.c"
)

# if installed, if should be put in subfolder of `freesteam` on system include dir
set(MY_HEADER_DIR "${PROJECT_SOURCE_DIR}/src")

set(MY_HEADERS
"src/b23.h"
"src/backwards.h"
"src/backwards_impl.h"
"src/bounds.h"
"src/common.h"
"src/compat.h"
"src/config.h"
"src/derivs.h"
"src/region1.h"
"src/region2.h"
"src/region3.h"
"src/region4.h"
"src/solver2.h"
"src/steam.h"
"src/steam_ph.h"
"src/steam_ps.h"
"src/steam_pT.h"
"src/steam_pu.h"
"src/steam_pv.h"
"src/steam_Ts.h"
"src/steam_Tx.h"
#"src/steam_uv.h"
"src/surftens.h"
"src/thcond.h"
"src/viscosity.h"
"src/zeroin.h"
)

add_library(freesteam SHARED ${MY_SOURCES})

#GSL is only depedence
find_package(GSL REQUIRED)
if(GSL_FOUND)
    target_include_directories(freesteam PRIVATE ${GSL_INCLUDE_DIRS})
    target_link_libraries(freesteam ${GSL_LIBRARIES})
else()
    message(ERROR "GNU Scientific Library (GSL) lib and headers are not found:"
                "please install libgls-dev or libgls-devel using package manager, "
                "or export GSL_ROOT_DIR variable as hint")
endif()

# test main exe
add_executable(freesteam_test ${MY_TEST_SOURCES})
include_directories(${MY_HEADER_DIR})
target_link_libraries(freesteam_test freesteam)

#swig wrapping
add_subdirectory("python")

#RPM spec config
#configure_file()

#pkg-config
#configure_file()

# debian package could be made from this