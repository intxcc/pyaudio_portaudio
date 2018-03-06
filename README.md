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

You will need a working cygwin installation with basic developer tools and python.

#### 1.
Change to /pyaudio/portaudio-v19 and type
```bash
./configure --with-winapi=wasapi --enable-static=yes --enable-shared=no
make loopback
```

To rebuild type
```bash
make clean
make loopback
```

#### 2.
Change to /pyaudio and type
```bash
python setup.py install --static-link
```

# Help!!
If you get errors, let me know. Thank you &hearts;
