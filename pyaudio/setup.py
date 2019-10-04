"""
PyAudio v0.2.11: Python Bindings for PortAudio.

Copyright (c) 2006 Hubert Pham

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY
OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE
USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import os
import platform
import sys
try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension

__version__ = "0.2.11"

# distutils will try to locate and link dynamically against portaudio.
#
# If you would rather statically link in the portaudio library (e.g.,
# typically on Microsoft Windows), run:
#
# % python setup.py build --static-link
#
# Specify the environment variable PORTAUDIO_PATH with the build tree
# of PortAudio.

STATIC_LINKING = False

if "--static-link" in sys.argv:
    STATIC_LINKING = True
    sys.argv.remove("--static-link")

portaudio_path = os.environ.get("PORTAUDIO_PATH", "./portaudio-v19")
mac_sysroot_path = os.environ.get("SYSROOT_PATH", None)

pyaudio_module_sources = ['src/_portaudiomodule.c']
include_dirs = ['portaudio-v19/include']
external_libraries = []
extra_compile_args = []
extra_link_args = []
scripts = []
defines = []

if sys.platform == 'darwin':
    defines += [('MACOSX', '1')]
    if mac_sysroot_path:
        extra_compile_args += ["-isysroot", mac_sysroot_path]
        extra_link_args += ["-isysroot", mac_sysroot_path]
elif sys.platform == 'win32':
    bits = platform.architecture()[0]
    if '64' in bits:
        defines.append(('MS_WIN64', '1'))

if not STATIC_LINKING:
    external_libraries = ['portaudio']
    extra_link_args = []
else:
    include_dirs = [os.path.join(portaudio_path, 'include/')]
    extra_link_args = []

    # check if we are running in a cygwin environment. if not we assume a native windows library in the msvc release path
    # To check if we are running on a 32 or 64 bit environment
    bits = platform.architecture()[0]
    if 'ORIGINAL_PATH' in os.environ and 'cygdrive' in os.environ['ORIGINAL_PATH']:
        extra_link_args.append(os.path.join(portaudio_path, 'lib/.libs/libportaudio.a'))
    elif '64' in bits:
        extra_link_args.append(os.path.join(portaudio_path, 'build/msvc/x64/Release/portaudio.lib'))
    else:
        extra_link_args.append(os.path.join(portaudio_path, 'build/msvc/Win32/Release/portaudio.lib'))

    # platform specific configuration
    if sys.platform == 'darwin':
        extra_link_args += ['-framework', 'CoreAudio',
                            '-framework', 'AudioToolbox',
                            '-framework', 'AudioUnit',
                            '-framework', 'Carbon']
    elif sys.platform == 'cygwin':
        external_libraries += ["winmm","ole32","uuid"]
        extra_link_args += ["-lwinmm","-lole32","-luuid"]
    elif sys.platform == 'win32':
        # i.e., Win32 Python with mingw32
        # run: python setup.py build -cmingw32
        if 'ORIGINAL_PATH' in os.environ and 'cygdrive' in os.environ['ORIGINAL_PATH']:
            external_libraries += ["winmm","ole32","uuid"]
            extra_link_args += ["-lwinmm","-lole32","-luuid"]
        else:
            external_libraries += ["winmm","ole32","uuid","advapi32","user32"]
            extra_link_args += ["/NODEFAULTLIB:MSVCRT"]

    elif sys.platform == 'linux2':
        extra_link_args += ['-lrt', '-lm', '-lpthread']
        # GNU/Linux has several audio systems (backends) available; be
        # sure to specify the desired ones here.  Start with ALSA and
        # JACK, since that's common today.
        extra_link_args += ['-lasound', '-ljack']

setup(name='PyAudio',
      version=__version__,
      author="Hubert Pham",
      url="http://people.csail.mit.edu/hubert/pyaudio/",
      description='PortAudio Python Bindings',
      long_description=__doc__.lstrip(),
      scripts=scripts,
      py_modules=['pyaudio'],
      package_dir={'': 'src'},
      ext_modules=[
    Extension('_portaudio',
              sources=pyaudio_module_sources,
              include_dirs=include_dirs,
              define_macros=defines,
              libraries=external_libraries,
              extra_compile_args=extra_compile_args,
              extra_link_args=extra_link_args)
    ])
