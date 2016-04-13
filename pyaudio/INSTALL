======================================================================
PyAudio Compilation Hints
======================================================================

Here are some hints for compiling PortAudio and PyAudio on various
platforms:

    * General UNIX Guide: (GNU/Linux, Mac OS X, Cygwin)
    * Microsoft Windows (native)

Generally speaking, installation involves building the PortAudio v19
library and then building PyAudio.

----------------------------------------------------------------------
General UNIX Guide (GNU/Linux, Mac OS X, Cygwin)
----------------------------------------------------------------------

1. Use a package manager to install PortAudio v19.

   To build PortAudio from source instead, extract the source and run:

   % ./configure
   % make
   % make install # you may need to be root

2. Extract PyAudio.  To build and install, run:

   % python setup.py install

----------------------------------------------------------------------
Microsoft Windows
----------------------------------------------------------------------

Targeting native Win32 Python will require either Microsoft Visual
Studio or MinGW (via Cygwin).  Here are compilation hints for using
MinGW under the Cygwin build environment.

Note: I've only tested this under Cygwin's build environment. Your
mileage may vary in other environments (i.e., compiling PortAudio with
MinGW's compiler).

1. Install cygwin's gcc and mingw packages.

2. Download PortAudio and build.  When running configure, be sure to
   specify the MinGW compiler (via a CC environment variable) to
   generate native Win32 binaries:

      % CC=i686-w64-mingw32-gcc ./configure --enable-static --with-pic
      % make

3. Before building PyAudio, apply a few necessary modifications:

   a. Python distutils calls ``gcc'' to build the C extension, so
      temporarily move your MinGW compiler to /usr/bin/gcc.

   b. Modify Python's Lib/distutils/cygwincompiler.py so that
      mscvr900.dll is not included in the build.  See:
      http://bugs.python.org/issue16472.

      Both Python 2.7 and Python 3+ require similar modification.

   c. For some versions of Python (e.g., Python 2.7 32-bit), it is
      necessary to further modify Python's
      Lib/distutils/cygwincompiler.py and remove references to
      -cmingw32, a flag which is no longer supported.
      See http://hg.python.org/cpython/rev/6b89176f1be5/.

   d. For some versions of 64-bit Python 3 (e.g., Python 3.2, 3.3, 3.4),
      it is necessary to generate .a archive of the Python DLL.
      See https://bugs.python.org/issue20785. Example for Python 3.4:

      % cd /path/to/Python34-x64/libs/
      % gendef /path/to/Windows/System32/python34.dll
      % dlltool --as-flags=--64 -m i386:x64-64 -k --output-lib libpython34.a \
          --input-def python34.def

4. To build PyAudio, run:

      % PORTAUDIO_PATH=/path/to/portaudio_tree /path/to/win/python \
            setup.py build --static-link -cmingw32

   Be sure to invoke the native Win32 python rather than cygwin's
   python.  The --static-link option statically links in the PortAudio
   library to the PyAudio module.

5. To install PyAudio:

      % python setup.py install --skip-build

   Or create a Python wheel and install using pip.
