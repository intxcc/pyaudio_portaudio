Example: Blocking Mode Audio I/O
--------------------------------

.. literalinclude:: ../test/play_wave.py

To use PyAudio, first instantiate PyAudio using
:py:func:`pyaudio.PyAudio` (1), which sets up the portaudio system.

To record or play audio, open a stream on the desired device with the
desired audio parameters using :py:func:`pyaudio.PyAudio.open`
(2). This sets up a :py:class:`pyaudio.Stream` to play or record
audio.

Play audio by writing audio data to the stream using
:py:func:`pyaudio.Stream.write`, or read audio data from the stream
using :py:func:`pyaudio.Stream.read`. (3)

Note that in "blocking mode", each :py:func:`pyaudio.Stream.write` or
:py:func:`pyaudio.Stream.read` blocks until all the given/requested
frames have been played/recorded.  Alternatively, to generate audio
data on the fly or immediately process recorded audio data, use the
"callback mode" outlined below.

Use :py:func:`pyaudio.Stream.stop_stream` to pause playing/recording,
and :py:func:`pyaudio.Stream.close` to terminate the stream. (4)

Finally, terminate the portaudio session using
:py:func:`pyaudio.PyAudio.terminate` (5)

Example: Callback Mode Audio I/O
--------------------------------

.. literalinclude:: ../test/play_wave_callback.py

In callback mode, PyAudio will call a specified callback function (2)
whenever it needs new audio data (to play) and/or when there is new
(recorded) audio data available.  Note that PyAudio calls the callback
function in a separate thread.  The function has the following
signature ``callback(<input_data>, <frame_count>, <time_info>,
<status_flag>)`` and must return a tuple containing ``frame_count``
frames of audio data and a flag signifying whether there are more
frames to play/record.

Start processing the audio stream using
:py:func:`pyaudio.Stream.start_stream` (4), which will call the
callback function repeatedly until that function returns
:py:data:`pyaudio.paComplete`.

To keep the stream active, the main thread must not terminate, e.g.,
by sleeping (5).
