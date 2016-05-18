#
# PortAudio V19 Makefile.in
#
# Dominic Mazzoni
# Modifications by Mikael Magnusson
# Modifications by Stelios Bounanos
#

top_srcdir = .
srcdir = .

top_builddir = .
PREFIX = /usr/local
prefix = $(PREFIX)
exec_prefix = ${prefix}
bindir = ${exec_prefix}/bin
libdir = ${exec_prefix}/lib
includedir = ${prefix}/include
CC = gcc
CXX =
CFLAGS = -g -O2 -DPA_LITTLE_ENDIAN -I$(top_srcdir)/include -I$(top_srcdir)/src/common -I$(top_srcdir)/src/os/win -DPA_USE_DS=0 -DPA_USE_WDMKS=0 -DPA_USE_ASIO=0 -UPA_USE_WASAPI -DPA_USE_WASAPI=1 -DPA_USE_WMME=0 -mthreads -DPACKAGE_NAME=\"\" -DPACKAGE_TARNAME=\"\" -DPACKAGE_VERSION=\"\" -DPACKAGE_STRING=\"\" -DPACKAGE_BUGREPORT=\"\" -DPACKAGE_URL=\"\" -DSTDC_HEADERS=1 -DHAVE_SYS_TYPES_H=1 -DHAVE_SYS_STAT_H=1 -DHAVE_STDLIB_H=1 -DHAVE_STRING_H=1 -DHAVE_MEMORY_H=1 -DHAVE_STRINGS_H=1 -DHAVE_INTTYPES_H=1 -DHAVE_STDINT_H=1 -DHAVE_UNISTD_H=1 -DHAVE_DLFCN_H=1 -DLT_OBJDIR=\".libs/\" -DHAVE_SYS_SOUNDCARD_H=1 -DSIZEOF_SHORT=2 -DSIZEOF_INT=4 -DSIZEOF_LONG=8 -DHAVE_CLOCK_GETTIME=1 -DHAVE_NANOSLEEP=1
LIBS = -lwinmm -lm -lole32 -luuid
AR = /usr/bin/ar
RANLIB = ranlib
SHELL = /bin/sh
LIBTOOL = $(SHELL) $(top_builddir)/libtool
INSTALL = /usr/bin/install -c
INSTALL_DATA = ${INSTALL} -m 644
SHARED_FLAGS =
LDFLAGS = -Wl
DLL_LIBS =  -lrt -lwinmm -lole32
CXXFLAGS =
NASM =
NASMOPT =
LN_S = cp -pR
LT_CURRENT=2
LT_REVISION=0
LT_AGE=0

OTHER_OBJS = src/hostapi/wasapi/pa_win_wasapi.o src/common/pa_ringbuffer.o src/os/win/pa_win_hostapis.o src/os/win/pa_win_util.o src/os/win/pa_win_coinitialize.o src/os/win/pa_win_waveformat.o
INCLUDES = portaudio.h

PALIB = libportaudio.la
PAINC = include/portaudio.h

PA_LDFLAGS = $(LDFLAGS) $(SHARED_FLAGS) -rpath $(libdir) -no-undefined \
	     -export-symbols-regex "(Pa|PaMacCore|PaJack|PaAlsa|PaAsio|PaOSS)_.*" \
	     -version-info $(LT_CURRENT):$(LT_REVISION):$(LT_AGE)

COMMON_OBJS = \
	src/common/pa_allocation.o \
	src/common/pa_converters.o \
	src/common/pa_cpuload.o \
	src/common/pa_dither.o \
	src/common/pa_debugprint.o \
	src/common/pa_front.o \
	src/common/pa_process.o \
	src/common/pa_stream.o \
	src/common/pa_trace.o \
	src/hostapi/skeleton/pa_hostapi_skeleton.o

OBJS := $(COMMON_OBJS) $(OTHER_OBJS)

LTOBJS := $(OBJS:.o=.lo)

SRC_DIRS = \
	src/common \
	src/hostapi/alsa \
	src/hostapi/asihpi \
	src/hostapi/asio \
	src/hostapi/coreaudio \
	src/hostapi/dsound \
	src/hostapi/jack \
	src/hostapi/oss \
	src/hostapi/wasapi \
	src/hostapi/wdmks \
	src/hostapi/wmme \
	src/os/unix \
	src/os/win

SUBDIRS =
#SUBDIRS += bindings/cpp

all: lib/$(PALIB) all-recursive

# With ASIO enabled we must link libportaudio and all test programs with CXX
lib/$(PALIB): lib-stamp $(LTOBJS) $(MAKEFILE) $(PAINC)
	 $(LIBTOOL) --mode=link $(CC) $(PA_LDFLAGS) -o lib/$(PALIB) $(LTOBJS) $(DLL_LIBS)
	@ #  $(LIBTOOL) --mode=link --tag=CXX $(CXX) $(PA_LDFLAGS) -o lib/$(PALIB) $(LTOBJS) $(DLL_LIBS)

bin/paloopback: lib/$(PALIB) $(MAKEFILE) $(PAINC) $(LOOPBACK_OBJS)
	 $(LIBTOOL) --mode=link $(CC) -o $@ $(CFLAGS) $(LOOPBACK_OBJS) lib/$(PALIB) $(LIBS)
	@ # $(LIBTOOL) --mode=link --tag=CXX $(CXX) -o $@ $(CXXFLAGS)  $(LOOPBACK_OBJS) lib/$(PALIB) $(LIBS)

install: lib/$(PALIB) portaudio-2.0.pc
	$(INSTALL) -d $(DESTDIR)$(libdir)
	$(LIBTOOL) --mode=install $(INSTALL) lib/$(PALIB) $(DESTDIR)$(libdir)
	$(INSTALL) -d $(DESTDIR)$(includedir)
	for include in $(INCLUDES); do \
		$(INSTALL_DATA) -m 644 $(top_srcdir)/include/$$include $(DESTDIR)$(includedir)/$$include; \
	done
	$(INSTALL) -d $(DESTDIR)$(libdir)/pkgconfig
	$(INSTALL) -m 644 portaudio-2.0.pc $(DESTDIR)$(libdir)/pkgconfig/portaudio-2.0.pc
	@echo ""
	@echo "------------------------------------------------------------"
	@echo "PortAudio was successfully installed."
	@echo ""
	@echo "On some systems (e.g. Linux) you should run 'ldconfig' now"
	@echo "to make the shared object available.  You may also need to"
	@echo "modify your LD_LIBRARY_PATH environment variable to include"
	@echo "the directory $(libdir)"
	@echo "------------------------------------------------------------"
	@echo ""
	$(MAKE) install-recursive

uninstall:
	$(LIBTOOL) --mode=uninstall rm -f $(DESTDIR)$(libdir)/$(PALIB)
	$(LIBTOOL) --mode=uninstall rm -f $(DESTDIR)$(includedir)/portaudio.h
	$(MAKE) uninstall-recursive

clean:
	$(LIBTOOL) --mode=clean rm -f $(LTOBJS) $(LOOPBACK_OBJS) $(ALL_TESTS) lib/$(PALIB)
	$(RM) lib-stamp
	-$(RM) -r lib

%.o: %.c $(MAKEFILE) $(PAINC)
	$(CC) -c $(CFLAGS) $< -o $@

%.lo: %.c $(MAKEFILE) $(PAINC)
	$(LIBTOOL) --mode=compile $(CC) -c $(CFLAGS) $< -o $@

%.lo: %.cpp $(MAKEFILE) $(PAINC)
	$(LIBTOOL) --mode=compile --tag=CXX $(CXX) -c $(CXXFLAGS) $< -o $@

%.o: %.cpp $(MAKEFILE) $(PAINC)
	$(CXX) -c $(CXXFLAGS) $< -o $@

%.o: %.asm
	$(NASM) $(NASMOPT) -o $@ $<

lib-stamp:
	-mkdir lib
	-mkdir -p $(SRC_DIRS)
	touch $@

all-recursive:
	if test -n "$(SUBDIRS)" ; then for dir in "$(SUBDIRS)"; do $(MAKE) -C $$dir all; done ; fi

install-recursive:
	if test -n "$(SUBDIRS)" ; then for dir in "$(SUBDIRS)"; do $(MAKE) -C $$dir install; done ; fi

uninstall-recursive:
	if test -n "$(SUBDIRS)" ; then for dir in "$(SUBDIRS)"; do $(MAKE) -C $$dir uninstall; done ; fi
