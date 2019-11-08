#to use this: change the source file name for your project

######################################
# setup has been done in project level, just do it again
######################################

find_package(PythonInterp REQUIRED)
message(STATUS "Found Python: ${PYTHON_EXECUTABLE} (found version \"${PYTHON_VERSION_STRING}\")")

# cross OS setup
IF(WIN32)
   # windows
   SET(PY_EXTENSION "pyd")
ELSE()
   SET(PY_EXTENSION "so")
ENDIF()

# DO NOT use relative include path within *.i file, but add the include_path
include_directories("${PROJECT_SOURCE_DIR}")

set(MY_MODULE "freesteam")  # it is possible to use the same name as sharedlib name
set(MY_SHARED_LIB "freesteam")
set(MY_SWIG_INTERFACE "freesteam.i")

######################################
# swig build
######################################
message( "if this cmake failed, turn off SWIG option in cmake, and then build with setup.py")

#how to enforce python3
FIND_PACKAGE(PythonLibs)
INCLUDE_DIRECTORIES(${PYTHON_INCLUDE_PATH})

find_package(SWIG REQUIRED)  # cmake 3 has official swig support
if(${CMAKE_VERSION} VERSION_GREATER "3.6.0") 
    include(UseSWIG)

    # error here
    #set_property(SOURCE ${MY_SWIG_INTERFACE}  PROPERTIES SWIG_FLAGS "-includeall")
    #set_property(SOURCE  ${MY_SWIG_INTERFACE}  PROPERTY CPLUSPLUS ON)  # for C++ code

    #TYPE <SHARED|MODULE|STATIC|USE_BUILD_SHARED_LIBS>  default to MODULE
    swig_add_library(${MY_MODULE}
                        LANGUAGE python
                        #NO_PROXY
                        OUTPUT_DIR ${PROJECT_BINARY_DIR}
                        #OUTFILE_DIR ${PROJECT_BINARY_DIR}/lib
                        SOURCES ${MY_SWIG_INTERFACE}
                    )
else()  # this section is not tested
    INCLUDE(${SWIG_USE_FILE}) # 3.6 or less
    #http://www.swig.org/Doc3.0/SWIGDocumentation.html#Introduction_build_system
    #SET_SOURCE_FILES_PROPERTIES(  ${MY_SWIG_INTERFACE}  PROPERTIES CPLUSPLUS ON)
    SET_SOURCE_FILES_PROPERTIES(${MY_SWIG_INTERFACE}  PROPERTIES SWIG_FLAGS "-includeall")

    swig_add_module(${MY_MODULE}
                        python
                    ${MY_SWIG_INTERFACE}
                    )
endif()

#set_target_properties(${MY_MODULE} PROPERTIES OUTPUT_NAME "freesteam")
swig_link_libraries(${MY_MODULE} ${MY_SHARED_LIB} ${PYTHON_LIBRARIES})
# the output wrap module are put into ${CMAKE_LIBRARY_OUTPUT_DIRECTORY}
