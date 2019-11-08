#!/usr/bin/env python
# This is a build script that makes use of the SCONS build system, see
# http://www.scons.org/. This script is frequently tested on both Windows
# (via MinGW/MSYS) and Linux, and should work in both of these environments.
# We don't currently propose to support building freesteam from MSVS but
# that shouldn't be necessary, as you should be able to use the MinGW-generated
# DLL even with MSVS, because it only uses C code.
import platform, sys, distutils.sysconfig, os, os.path

#version number for this copy of freesteam
version = "2.1"

# version number of python
pyversion = "%d.%d" % (sys.version_info[0],sys.version_info[1])

# architecture
instarch = ("","-amd64")[platform.architecture()[0] == "64bit"]

# Set up some platform-specific defaults
if platform.system()=="Windows":
	default_emso_location = "c:\\Program Files\\EMSO\\interface"
	default_prefix = 'c:/MinGW'
	python_exe = sys.executable
	default_python = distutils.sysconfig.get_python_lib()
	default_gsl_static = 1
else:
	default_emso_location = None
	default_prefix = '/usr/local'
	python_exe = "/usr/bin/env python"
	default_python = distutils.sysconfig.get_python_lib()
	default_gsl_static = 0

if platform.system()=="Darwin":
	default_gsl_static = 0

# SONAME related flags, for linux shared object versioning. Because this is a
# re-write of freesteam with a new API, we will bump the soname to .1

if platform.system()=="Windows":
	soname_major = ""
	soname_minor = ""
else:
	soname_major = ".1"
	soname_minor = ".0"

soname_default = "${SHLIBPREFIX}freesteam${SHLIBSUFFIX}${SONAME_MAJOR}"

# Configuration options for the build. You can set these on the command-line
# eg using "scons GCOV=1 ..."

vars = Variables()

vars.Add(BoolVariable(
	'GCOV'
	,"Build for coverage testing using gcov."
	,False
))

vars.Add(BoolVariable(
	'DEBUG'
	,"Build with debug data for use with GDB."
	,False
))

vars.Add(PathVariable(
	'INSTALL_PREFIX'
	,"Base directory for install, see also INSTALL_LIB and INSTALL_INCLUDE"
	,default_prefix
))

vars.Add(
	'INSTALL_LIB'
	,"Location to install library"
	, "$INSTALL_PREFIX/lib"
)

vars.Add(
	'INSTALL_INCLUDE'
	,"Location to install headers"
	,"$INSTALL_PREFIX/include"
)

vars.Add(
	'INSTALL_BIN'
	,"Location to install binaries"
	,"$INSTALL_PREFIX/bin"
)

vars.Add(
	'INSTALL_SHARE'
	,"Location to install 'share' files, examples, etc."
	,"$INSTALL_PREFIX/share"
)

vars.Add(PathVariable(
	'INSTALL_ROOT'
	,"Root onto which installation should take place. Normally only for "
		+"use when building RPMs"
	,None
))

vars.Add(PathVariable(
	'INSTALL_PYTHON'
	,"Directory for installation of Python extensions"
	,"%s" % default_python
))

vars.Add(
	'SONAME_MAJOR'
	,"major version of the freesteam library"
	,soname_major
)

vars.Add(
	'SONAME_MINOR'
	,"Shared library minor version number (for use in installed file name). Should be '.0' for example."
	,soname_minor
)

vars.Add(
	'SONAME'
	,"'soname' to be assigned to the shared library. Should be 'freesteam.so.1' for example."
	,soname_default
)

vars.Add(
	'DISTTAR_NAME'
	,"Stem name of the tarball created by 'scons dist'. So for 'freesteam-aaa.tar.bz2', set this to 'freesteam-aaa'."
	,"freesteam-"+version
)

vars.Add(
	'HOST_PREFIX'
	,"Host prefix, for use in cross-compiling. Defaults to empty"
	,""
)

vars.Add(
	'CC'
	,'C Compiler command'
	,"${HOST_PREFIX}gcc"
)

vars.Add(
	'SWIG'
	,"Name of your swig executable"
	,'swig'
)

if platform.system()=="Windows":
	vars.Add(
		'WIN_INSTALLER_NAME'
		,"Name of the installer .exe to create under Windows (minus the '.exe')"
		,"freesteam-"+version+instarch+"-py"+pyversion+".exe"
	)

# TODO work out a way to set gsl_static via options...?

# Set up the 'tools' the SCONS will need access to , eg compilers
# and create the SCONS 'environment':

tools = ['swig','ascend','substinfile','gsl','gtk','tar','disttar', 'nsis']
if platform.system()=="Windows":
	env = Environment(ENV=os.environ
		, GSL_STATIC = default_gsl_static
		, toolpath = ['scons']
		, tools = ['mingw']+tools
	)
else:
	env = Environment(
		ENV={"PATH":os.environ['PATH']}
		, GSL_STATIC = default_gsl_static
		, toolpath=['scons']
		, tools=['default']+tools
	)
	# import this one if it's been specified
	if os.environ.get('PKG_CONFIG_PATH'):
		env['ENV']['PKG_CONFIG_PATH'] = os.environ['PKG_CONFIG_PATH']

Help(vars.GenerateHelpText(env))

# Some utility tools for installing file with suitable permissions
  	 
import SCons 	 
from SCons.Script.SConscript import SConsEnvironment 	 
SConsEnvironment.Chmod = SCons.Action.ActionFactory(os.chmod, 	 
	lambda dest, mode: 'Chmod("%s", 0%o)' % (dest, mode)) 	 
  	 
def InstallPerm(env, dest, files, perm): 	 
	obj = env.Install(dest, files) 	 
	for i in obj: 	 
		env.AddPostAction(i, env.Chmod(str(i), perm))
	return dest

def InstallPermAs(env, dest, filen, perm): 	 
	obj = env.InstallAs(dest, filen) 	 
	for i in obj: 	 
		env.AddPostAction(i, env.Chmod(str(i), perm))
	return dest
  	 
SConsEnvironment.InstallPerm = InstallPerm
SConsEnvironment.InstallProgram = lambda env, dest, files: InstallPerm(env, dest, files, 0755) 	 
SConsEnvironment.InstallHeader = lambda env, dest, files: InstallPerm(env, dest, files, 0644) 	 
SConsEnvironment.InstallLibrary = lambda env, dest, files: InstallPerm(env, dest, files, 0644) 	 
SConsEnvironment.InstallLibraryAs = lambda env, dest, files: InstallPermAs(env, dest, files, 0644)

# Add configuration options to the 'environment'

vars.Update(env)

#----------------
# SWIG

import re,subprocess

def get_swig_version(env):
	#print "SWIG='%s'" % env['SWIG']
	cmd = [env['SWIG'],'-version']
	output = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
	
	restr = "SWIG\\s+Version\\s+(?P<maj>[0-9]+)\\.(?P<min>[0-9]+)\\.(?P<pat>[0-9]+)\\s*$"
	expr = re.compile(restr,re.M);
	m = expr.search(output);
	if not m:
		return None
	maj = int(m.group('maj'))
	min = int(m.group('min'))
	pat = int(m.group('pat'))

	return (maj,min,pat)
	

def CheckSwigVersion(context):
	
	try:
		context.Message("Checking version of SWIG... ")
		maj,min,pat = get_swig_version(context.env)
	except Exception,e:
		context.Result("Failed to detect version, or failed to run SWIG (%s)"% str(e))
		return False;
	
	context.env['SWIGVERSION']=tuple([maj,min,pat])
	
	if maj == 1 and (
			min > 3
			or (min == 3 and pat >= 24)
		):
		context.Result("ok, %d.%d.%d" % (maj,min,pat))
		return True;
	elif maj >= 2:
		context.Result("ok, %d.%d.%d" % (maj,min,pat))
		return True;
	else:
		context.Result("too old, %d.%d.%d" % (maj,min,pat))
		return False;

# Check that we got all the associated stuff that we need...

if not env.get('HAVE_GSL'):
	print "GSL was not found... install GSL (package 'libgsl0-dev' or similar in Ubuntu)."
	Exit(1)

# TODO: detect PYTHON properly.
if platform.system()=="Windows":
	python_lib='python%d%d'
else:
	python_lib='python%d.%d'

import distutils.sysconfig

python_lib = python_lib % (sys.version_info[0],sys.version_info[1])

conf = env.Configure(custom_tests =
	{'CheckSwigVersion' : CheckSwigVersion}
)

if not conf.CheckFunc('fprintf'):
	print "You compiler and/or environment is not correctly configured (see config.log for details)"
	Exit(1)

without_python_reason = "Python header 'Python.h' not found"
env['HAVE_PYTHON'] = False
pyinc = os.path.join(distutils.sysconfig.get_python_inc(),"Python.h")
#print "PYINC =",pyinc
_havepy = conf.CheckHeader(pyinc)
if _havepy:
	env['HAVE_PYTHON'] = True

#without_python_reason = "Python library '%s' not found" % python_lib
#conf.env['HAVE_PYTHON'] = conf.CheckLib(python_lib)

if conf.env['HAVE_PYTHON'] and conf.CheckSwigVersion() is False:
	without_python_reason = 'SWIG >= 1.3.24 is required'
	conf.env['HAVE_PYTHON']=False

conf.Finish()

if  not env.get('HAVE_ASCEND'):
	print "WARNING: ASCEND was not found... freesteam will be built without ASCEND bindings."

if not env['HAVE_PYTHON']:
	print "WARNING: Freesteam will be built without Python bindings.", without_python_reason


# Flags to give some more warning output from the GCC compiler

env.Append(CFLAGS=['-Wall','-W','-Wconversion','-Wimplicit'])

# Flags for coverage testing (will apply to all code built in 'env')

if env.get('GCOV'):
	env.Append(
		CFLAGS=['-fprofile-arcs','-ftest-coverage']
		,LIBS=['gcov']
	)

if env.get('DEBUG'):
	env.Append(
		CFLAGS=['-g']
	)

# Create config.h including version number

subst_dict = {
	'@VERSION@':version
	,'@SONAME_MAJOR@':soname_major
	,'@SONAME_MINOR@':soname_minor
	, '@PYTHON@' : python_exe
	, '@INSTALL_BIN@':env['INSTALL_BIN']
	, '@INSTALL_INCLUDE@':env['INSTALL_INCLUDE']
	, '@INSTALL_LIB@':env['INSTALL_LIB']
	, '@INSTALL_SHARE@':env['INSTALL_SHARE']
}

env.Append(SUBST_DICT=subst_dict)

configh = env.SubstInFile('config.h.in')
configscript = env.SubstInFile('freesteam-config.in')
specfile = env.SubstInFile('freesteam.spec.in')

install_config = env.InstallProgram("${INSTALL_ROOT}$INSTALL_BIN",configscript)

default_targets =['python','ascend']

# Here is the list of all of the source files that will go into
# the freesteam DLL/SO.

srcs = ["region1.c", "region2.c", "region3.c", "region4.c", "steam_ph.c"
	,"steam.c", "backwards.c","b23.c", "common.c", "derivs.c", "zeroin.c"
	,"steam_ps.c", "solver2.c","steam_pT.c","steam_pu.c","steam_Ts.c"
	,"steam_Tx.c", "surftens.c"
	,"bounds.c", "steam_pv.c", "viscosity.c", "thcond.c"
]

# Create a sub-environment with linking to libm for mathematics routines

lib_env = env.Clone()
lib_env.Append(
	LIBS = ['m']
)
lib_env.Append(
	CPPPATH = env.get('GSL_CPPPATH')
)
lib_srcs = srcs
if not lib_env['GSL_STATIC']:
	lib_env.Append(
		LIBS = env.get('GSL_LIBS')
		,LIBPATH = env.get('GSL_LIBPATH')
	)
else:
	lib_srcs = srcs + env.get('GSL_STATICLIBS',[])
if platform.system()=="Linux":
	lib_env.Append(LINKFLAGS=['-Wl,-soname,$SONAME'])

# Create the shared library

lib = lib_env.SharedLibrary("freesteam",lib_srcs)
env.Depends('python',lib)

libs = [lib]

# create local symlink for the soname stuff.
if platform.system()=="Linux":
	if env.get('SONAME_MAJOR'):
		lib_env.Command("${SHLIBPREFIX}freesteam${SHLIBSUFFIX}${SONAME_MAJOR}",lib,Move("$TARGET","$SOURCE"))
		#print "MAKING LINK, SONAME_MAJOR =",env.get('SONAME_MAJOR')
		liblink = lib_env.Command("${SHLIBPREFIX}freesteam${SHLIBSUFFIX}${SONAME_MAJOR}"
			,lib
			,"ln -s $SOURCE $TARGET"
		)
		libs.append(liblink)
		env.Depends('python',liblink)
		env.Depends('test',liblink)

# Store a reference to this library so that we can reference it from
# SConscript files in subdirectories

env['libfreesteam'] = lib

# Create an environment variable into which locations of installed files can be
# stored.

env['installedfiles'] = []

# Build the Python API for freesteam

env.SConscript(["python/SConscript"],'env')

# Build the ASCEND API for freesteam (TODO move this into the ASCEND project
# once it becomes stable.

env.SConscript(["ascend/SConscript"],'env')

# Install the examples, but don't build them

env.SConscript(["examples/SConscript"],'env')

# Build the cheery little GTK GUI that everyone will like :-)
env.SConscript(["gtk/SConscript"],'env')

# Create the test program. Currently we're not using any unit testing library;
# this is currently just simple bespoke code.

prog_env = env.Clone()
prog_env.Append(
	LIBS=['freesteam']
	,LIBPATH=['#']
	,LINKFLAGS=['-Wl,-rpath,'+str(Dir('#'))]
)

prog_env.Program("test","test.c")

#-------------------------------------------------------------------------------
# Install files, if requested.

#print "INSTALL_LIB =",env.get('INSTALL_LIB')
#print "INSTALL_PREFIX =",env.get('INSTALL_PREFIX')
#print "INSTALL_ROOT =",env.get('INSTALL_ROOT')

try:
	umask = os.umask(022)
except OSError:
	# ignore on systems that don't support umask
	pass


libname = "${INSTALL_LIB}/$SONAME$SONAME_MINOR"
if platform.system()=="Windows":
	install_lib = env.InstallLibrary("$INSTALL_ROOT$INSTALL_LIB",[lib])
else:
	install_lib = env.InstallLibraryAs("${INSTALL_ROOT}"+libname, [lib])

	link1 = "$INSTALL_LIB/${SHLIBPREFIX}freesteam$SHLIBSUFFIX"
	link2 = "$INSTALL_LIB/$SONAME"

	install_link1 = None
	if env.subst(link1) != env.subst(libname):
		install_link1 = env.Command("${INSTALL_ROOT}"+link1,install_lib,"ln -s %s $TARGET" % os.path.basename(libname))

	install_link2 = None
	if env.get("SONAME_MINOR"):
		install_link2 = env.Command("${INSTALL_ROOT}"+link2,install_lib,"ln -s %s $TARGET"%os.path.basename(libname))
	
	env['installedfiles'] += [install_link1, install_link2]

env['installedfiles'] += [install_lib, install_config]

import glob
headerfiles = glob.glob("*.h")

if env.get('HAVE_SWIG') and env.get('HAVE_PYTHON'):
	headerfiles += glob.glob("python/*.i")

#---------------
# DISTRIBUTION TARBALL

env['DISTTAR_FORMAT']='bz2'
env.Append(
	DISTTAR_EXCLUDEEXTS=['.o','.os','.so','.0','.1','.2','.3'
		,'.a','.dll','.lib','.cc','.cache'
		,'.pyc','.cvsignore','.dblite','.log','.pl','.out','.exe','.aux','.idx'
		,'.toc','.lof','.lot','.mm','.warnings','.tm2','.swp',',tmp','.gz'
		,'.bz2','.7z','.deb','.dsc','.changes','_wrap.c','.pyc'
		,'.dvi','.tex','.lot','.loc','.eps'
	]
	, DISTTAR_EXCLUDEDIRS=['CVS','.svn','.sconf_temp', 'dist','debian']
	, DISTTAR_EXCLUDERES=[r"_wrap\.c$", r"~$", r"python/freesteam\.py", r"/test$",r"examples/isentropic$"]
)

tar = env.DistTar("dist/"+env['DISTTAR_NAME']
	, [env.Dir('#'),'freesteam.spec']
)

#------------------------------------------------------

# DEBIAN TARBALL for use with Build Service

if platform.system() != "Windows":
	import glob
	deb_files = glob.glob('debian/*.install')
	deb_files += glob.glob('debian/*.docs')
	deb_files += glob.glob('debian/*.dirs')
	deb_files += glob.glob('debian/*.man')
	deb_files += glob.glob('debian/*.manpages')
	deb_files += ['debian/%s' % s for s in ['rules','control','changelog','compat','copyright','dirs']]

	deb_tar = env.Tar(
		'dist/debian.tar.gz'
		,deb_files
		,TARFLAGS = ['cz']
	)

#---------------------------------------------------
env['installedfiles'] += [env.InstallHeader("${INSTALL_ROOT}$INSTALL_INCLUDE/freesteam", headerfiles)]
	
env.Alias('install',env['installedfiles'])

#------------------------------------------------------
# WINDOWS INSTALLER

with_installer = True

if not env.get('NSIS'):
	with_installer = False
	without_installer_reason = "NSIS not found"

if platform.system()=="Windows":
	if with_installer:
		inst64 = ("0","1")[platform.architecture()[0] == "64bit"]
		env.Append(NSISDEFINES={
			'OUTFILE':"#dist/"+env['WIN_INSTALLER_NAME']
			,"VERSION":version
			,'PYVERSION':pyversion
			,'INST64':inst64
		})
		installer = env.Installer('installer.nsi')
		Depends(installer,["python","ascend"])
		Depends(installer,[configscript])
		env.Alias('installer',installer)
	else:
		print "Skipping... Windows installer isn't being built:",without_installer_reason

#------------------------------------------------------
# DEFAULT TARGETS

env.Default(default_targets)

print "Building targets:"," ".join([str(i) for i in BUILD_TARGETS])

# vim:set ts=4 sw=4 noexpandtab ft=python:

