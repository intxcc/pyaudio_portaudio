"""
PyAudio Example: Make a wire between input and output (i.e., record a
few samples and play them back immediately).

This is the callback (non-blocking) version.
"""

import pyaudio
import time
import sys

WIDTH = 2
CHANNELS = 2
RATE = 44100
DURATION = 5

if sys.platform == 'darwin':
    CHANNELS = 1

p = pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    return (in_data, pyaudio.paContinue)

stream = p.open(format=p.get_format_from_width(WIDTH),
                channels=CHANNELS,
                rate=RATE,
                input=True,
                output=True,
                stream_callback=callback)

stream.start_stream()

start = time.time()

while stream.is_active() and (time.time() - start) < DURATION:
    time.sleep(0.1)

stream.stop_stream()
stream.close()

p.terminate()
