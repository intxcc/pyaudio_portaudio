# _Precompiled & Extended_ | PyAudio with PortAudio for Windows

#### _Used versions_: <br>&middot; PyAudio 0.2.11 | co 7090e25bcba41413bd7ce89aa73bc0efb1ae1ca1<br>&middot; PortAudio V19 | co 1bdcb9e41357ec76d8cf73f9ef278202a3ea1e3b

#### Extensions:<br>&middot; Support of Windows sound loopback: Record the output of your soundcard

---
This project is a fork of two open source projects. If you'd like, give them some love:
- http://www.portaudio.com/
- https://people.csail.mit.edu/hubert/pyaudio/

---

# Usage

See the [example](https://github.com/intxcc/pyaudio_portaudio/tree/master/example).

Exactly like the official PyAudio but with the extra option "as_loopback" which expects a boolean.
```python
import pyaudio
p = pyaudio.PyAudio()
stream = p.open([...], as_loopback = True)
```

# How to install?

### You can find the precompiled PyAudio build, static linked with PortAudio, as well as only the static linked PortAudio in the [release](https://github.com/intxcc/pyaudio_portaudio/releases).

I will try to rebuild the project on each update from one of the used projects.

# How to build?

## Cygwin

You will need a working cygwin installation with basic developer tools and python.

#### Step 0
You might have to change all files to use LF line endings with
```bash
find . -type f -exec sed -i 's/\x0d//g' {} \+
```

#### Step 1
Change to */pyaudio/portaudio-v19* and type
```bash
./configure --with-winapi=wasapi --enable-static=yes --enable-shared=no
make loopback
```

To rebuild type
```bash
make clean
make loopback
```

#### Step 2
Change to /pyaudio and type
```bash
python setup.py install --static-link
```

## Microsoft Visual Studio (2017)

You will need to include the python executable in PATH.

#### Step 1

- Open the portaudio project located in *pyaudio\portaudio-v19\build\msvc\portaudio.sln*.

- Open the project configuration and make sure that the configuration type is set to static library.

- Select the build type __Release__ and __x64__. Then build the project.

- Make sure the build was succesful and the file *pyaudio\portaudio-v19\build\msvc\x64\Release\portaudio.lib* does exist.

#### Step 2

Open the PowerShell __as administrator__ and change the directory. Then you can build and install pyaudio with portaudio:

```
cd <Location of the repository>\pyaudio_portaudio\pyaudio
python.exe .\setup.py install --static-link
```

## Microsoft Visual Studio (2017) - 32 bit

### For 32-bit support see instructions above and this issue: https://github.com/intxcc/pyaudio_portaudio/issues/8.

### The code from that issue is merged now, but as I do not have a 32-bit version I can't verify it. Comment in the issue for further help.

# Help!!
If you get errors, let me know. Thank you &hearts;
