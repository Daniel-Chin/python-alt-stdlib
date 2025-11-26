'''
A context for temporary PulseAudio configuration.
'''

from contextlib import contextmanager
import subprocess
import warnings

def getDefault():
    return subprocess.check_output(['pactl', 'get-default-sink']).decode('utf-8').strip()

def setDefault(sink: str):
    subprocess.run(['pactl', 'set-default-sink', sink])

@contextmanager
def PulseAudioTempDefault(sink: str):
    original_sink = getDefault()
    try:
        setDefault(sink)
        yield
    finally:
        now_sink = getDefault()
        if now_sink != sink:
            warnings.warn(f'PulseAudioTempDefault: default sink changed during context by someone else. From {sink} to {now_sink}.')
        setDefault(original_sink)
