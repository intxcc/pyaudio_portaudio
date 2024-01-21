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
from pathlib import Path
import logging

from setuptools import setup, Extension


__version__ = "0.2.14"

# setup.py/setuptools will try to locate and link dynamically against portaudio,
# except on Windows. On Windows, setup.py will attempt to statically link in
# portaudio, since most users will install PyAudio from pre-compiled wheels.
# Optionally specify the environment variable PORTAUDIO_PATH with the build tree of PortAudio.

STATIC_LINKING = sys.platform == 'win32'

portaudio_path = Path(os.environ.get('PORTAUDIO_PATH', 'portaudio-v19'))
mac_sysroot_path = os.environ.get('SYSROOT_PATH', None)

pyaudio_module_sources = ['src/_portaudiomodule.c']
include_dirs = ['portaudio-v19/include']
external_libraries = []
extra_compile_args = []
extra_link_args = []
scripts = []
defines = []
data_files = []  # for dynamic libraries
is_x64 = sys.maxsize > 2**32

if sys.platform == 'win32':
    if is_x64:
        defines.append(('MS_WIN64', '1'))
elif sys.platform == 'darwin':  # mac
    defines += [('MACOSX', '1')]
    if mac_sysroot_path:
        extra_compile_args += ['-isysroot', mac_sysroot_path]
        extra_link_args += ['-isysroot', mac_sysroot_path]


# check if we are running in a cygwin environment. if not we assume a native windows library in the msvc release path
# To check if we are running on a 32 or 64 bit environment
if 'ORIGINAL_PATH' in os.environ and 'cygdrive' in os.environ['ORIGINAL_PATH']:
    portaudio_shared = portaudio_path.joinpath('lib/.libs/libportaudio.a')
elif is_x64:
    lib_path = 'build/msvc/x64/ReleaseDLL/portaudio.lib'
    portaudio_shared = portaudio_path.joinpath(lib_path)
else:
    lib_path = 'build/msvc/Win32/ReleaseDLL/portaudio.lib'
    portaudio_shared = portaudio_path.joinpath(lib_path)
extra_link_args.append(str(portaudio_shared))

external_libraries.append('portaudio')
library_dirs = []
lib_path = 'build/msvc/x64/ReleaseDLL' if is_x64 else 'build/msvc/Win32/ReleaseDLL'
lib_path = os.path.join(portaudio_path, lib_path)
if not STATIC_LINKING:
    data_files.append(('', [os.path.join(lib_path, 'portaudio.dll')]))
else:
    library_dirs.append(lib_path)
    include_dirs = [os.path.join(portaudio_path, 'include/')]
    data_files.append((r'Lib\site-packages', [os.path.join(lib_path, 'portaudio.dll')]))
    # platform specific configuration
    if sys.platform == 'win32':
        # i.e., Win32 Python with mingw32
        # run: python setup.py build -cmingw32
        if 'ORIGINAL_PATH' in os.environ and 'cygdrive' in os.environ['ORIGINAL_PATH']:
            external_libraries += ['winmm', 'ole32', 'uuid']
            extra_link_args += ['-lwinmm', '-lole32', '-luuid']
        else:
            # MSVC
            # TODO: external_libraries += ["user32", "Advapi32"]?
            external_libraries += ['winmm', 'ole32', 'uuid', 'advapi32', 'user32']
            # extra_link_args.append('/NODEFAULTLIB:MSVCRT')
            # disable Buffer Security Checks
            extra_link_args.append('/GS-')
            # extra_link_args.append('/MT')
    elif sys.platform == 'darwin':
        extra_link_args += ['-framework', 'CoreAudio',
                            '-framework', 'AudioToolbox',
                            '-framework', 'AudioUnit',
                            '-framework', 'Carbon']
    elif sys.platform == 'cygwin':
        external_libraries += ["winmm", "ole32", "uuid"]
        extra_link_args += ["-lwinmm", "-lole32", "-luuid"]
    elif sys.platform == 'linux2':
        extra_link_args += ['-lrt', '-lm', '-lpthread']
        # GNU/Linux has several audio systems (backends) available; be
        # sure to specify the desired ones here.  Start with ALSA and
        # JACK, since that's common today.
        extra_link_args += ['-lasound', '-ljack']
setup(name='PyAudio',
      version=__version__,
      author='Hubert Pham',
      url='http://people.csail.mit.edu/hubert/pyaudio/',
      description='Cross-platform audio I/O with PortAudio',
      long_description=__doc__.lstrip(),
      license='MIT',
      scripts=scripts,
      py_modules=['pyaudio'],
      package_dir={'': 'src'},
      ext_modules=[
          Extension('_portaudio',
                    sources=pyaudio_module_sources,
                    include_dirs=include_dirs,
                    define_macros=defines,
                    libraries=external_libraries,
                    library_dirs=library_dirs,
                    extra_compile_args=extra_compile_args,
                    extra_link_args=extra_link_args)
      ], data_files=data_files)
