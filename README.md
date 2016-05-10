# _Precompiled & Extended_ | PyAudio with PortAudio for Windows

#### _Used versions_: <br>&middot; PyAudio 0.2.9 | co dce064b428<br>&middot; PortAudio V19 | rev 1919

#### Extensions:<br>&middot; Support of Windows sound loopback: Record the output of your soundcard

---
This project is a fork of two open source projects. If you'd like, give them some love:
- http://www.portaudio.com/
- https://people.csail.mit.edu/hubert/pyaudio/

---

You can find the precompiled build, static linked with portaudio as well as the static linked portaudio in the [release](https://github.com/intxcc/pyaudio_portaudio/releases). For using PyAudio you will not need the static linked portaudio, as this is static linked into PyAudio as well.

I will try to rebuild the project on each update from one of the used projects.

# How to install?

You will need a working cygwin installation with basic developer tools and python.

#### 1.
Change to /pyaudio/portaudio-v19 and type
```bash
make
```

To rebuild type
```bash
make clean
make
```

#### 2.
Change to /pyaudio and type
```bash
python setup.py install
```

# Help!!
If you get errors, let me know. Thank you &hearts;
