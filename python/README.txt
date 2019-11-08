
freesteam for Python users
==========================

freesteam will put the necessary libraries into your Python 'site-packages'
folder such that you can immediately use the following Python code:

  from freesteam import *
  
  p = 10e5 # note: assumed units are Pascal
  T = 300 # note: assumed units are Kelvin
  S = steam_pT(p,T)
  print "density = %f kg/m3" % S.rho

Previous 0.x versions of freesteam included some functionality for performing
units of measurement manipulation. This was seen as unnecessary functionality,
and has been removed in the 2.x release. All units are in base SI units, such as

  kg/m^3, Pa, m/s, J/kg/K, J/kg, Pa*s

Be very careful therefore to ensure you have made the appropriate unit
conversions before passing parameters to freesteam.

If you have any questions with the Python interface for freesteam, please let me
know via the contact details at http://freesteam.sf.net. The Python interface is
still in a fairly formative stage, and I am keen to improve it with suggestions
from users.


Windows users
-------------

The windows installer will place _freesteam.pyd in your Python directory, but
only if the correct version of Python was detected at the time you installed
freesteam. If you installed Python afterwards, just re-run the freesteam setup
program and the Python components should then be installed. You can check the
detailed install log to make sure that the required DLL is in place.

Note that these Python scripts have been primarily developed under Linux; they
may take some fiddling to work completely on Windows.


Linux users
-----------

'scons install' should put your _freesteam.so and freesteam.py files in the
correct location so that python finds them.

We propose to make .RPM and .DEB packages available for freesteam; in this case,
a separate 'python-freesteam' package will need to be installed for the Python
bindings.


Example python scripts
----------------------

Some example Python scripts will be included in the freesteam package on
Windows, accessible/browsable from the Start menu.

Some of these scripts make use of the Matplotlib plotting library, which should
install before running such scripts. http://matplotlib.sf.net


-- 
John Pye
Oct 2009
