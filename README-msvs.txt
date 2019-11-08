
HOW TO BUILD FREESTEAM FOR VISUAL STUDIO 2010
=============================================

Dr Peter Franz, December 2012

Prerequisites
-------------

	- freesteam Source Code (.h and .c files)

	- GNU Scientific Library (GSL). There is a pre-compiled version but I did
	  not get it to work for me: http://gordon-taft.net/SciencePack.html
	  Alternatively, you need the source code from 
	  http://www.gnu.org/software/gsl/ and a package to compile with Visual Studio:
	  http://gladman.plushost.co.uk/oldsite/computing/gnu_scientific_library.php


1. Install GSL for Visual Studio
--------------------------------

If you're re-compiling GSL then follow the instructions in the README file given 
in the package. In essence, you need to properly set up a folder structure and 
run a python script before compiling the GSL libraries. I only targeted GSL.lib. 
I could not get the Debug version running but the Release version worked fine.


2. Re-compiling freesteam
-------------------------

* Start a new Visual Studio project, with a static library as target. Call it 
freesteam, with target freesteam.lib

* Copy all freesteam .c and .h files from the original distribution into the 
new project folder.

* In the Solution Explorer, right-click on Header Files, and select 
Add->Existing Item. Select all .h files from freesteam.

* Repeat the same for the Source Files, selecting all .c files from freesteam.

* In the Solution Explorer, right-click on the freesteam solution and bring up 
the Properties.

* Select your target configuration, i.e. Debug or Release or All Configurations

* Under C/C++->General, insert under Additional Include Directories a reference 
to the GSL header location, or - more precisely - the folder ABOVE the header 
location, since GSL headers are referenced in freesteam as GSL\multiroots

* Under C/C++->Advanaced, select Compile as C++ Code (/TP)

* Under Librarian->General, set Additional Library Directories to the location 
of the GSL.lib (Debug or Release version - or use only the Release version, if 
the Debug version did not compile) and add GSL.lib to Additional Dependencies.

* Under Librarian->General, set Link Library Dependencies to Yes (optional).
Finally, compile freesteam.lib as either Debug or Release version.


3. Testing freesteam.lib in new C++ code
----------------------------------------

* Start a new Visual Studio project, with Console Application as target.

* In the Solution Explorer, right-click the solution and bring up the properties.

* Under C/C++->General add a reference to the location of the freesteam header files.

* Under Linker->General add a reference to the location where freesteam.lib is stored.

* Under Linker->Input add freesteam.lib to the Additional Dependencies.

You can use the code below for testing that everything works alright - it 
calculates the execution time for freesteam function calls:

 #include "stdafx.h"
 #include <iostream>
 #include <stdlib.h>
 #include <time.h> 
 
 #include <steam_ph.h>
 
 using namespace std;
 
 int _tmain(int argc, _TCHAR* argv[])
 {
 	cout << "Hello to the world of freesteam users!" << endl;
 	SteamState s;
 	double T;
 	long i, N = 10000000;
 	time_t t0, t1;
 	t0 = time(NULL);
 	for (i=0;i<N;i++)
 	{
 		s = freesteam_set_ph(100e5,300e3);
 		T = freesteam_T(s);
 	}
 	t1 = time(NULL);
 	cout << "Temperature T = " << T << endl;
 	cout << "Time per execution cycle : " << difftime(t1,t0)/N << endl;
 	return 0;
 }

-- 
Dr Peter Franz
December 2012

