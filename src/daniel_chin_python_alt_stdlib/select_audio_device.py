'''
A terminal interface that lets the user select 
the audio input/output device.  

What if device list changed during selection?  
- pyaudio doesn't offer open-by-name. Perfection is impossible.  
- I recommend you init the stream as soon as the function returns.  
'''

import typing as tp

import pyaudio

from .interactive import inputChin

Direction = tp.Literal['In', 'Out']

def select_audio_device_input(
    pa: pyaudio.PyAudio, 
    guesses: list[str] = ['Line', 'Headset', 'Microphone Array'], 
) -> int:
    return select_audio_device(pa, 'In',  guesses)

def select_audio_device_output(
    pa: pyaudio.PyAudio, 
    guesses: list[str] = ['VoiceMeeter Input'], 
) -> int:
    return select_audio_device(pa, 'Out', guesses)

def get_device_info(
    pa: pyaudio.PyAudio, 
    device_index: int, 
    query_direction: Direction,
    api_index: int = 0,
) -> tuple[str, bool]:
    info = pa.get_device_info_by_host_api_device_index(api_index, device_index)
    name: str = info['name']    # type: ignore
    do_align = info[f'max{query_direction}putChannels'] > 0    # type: ignore
    return name, do_align

def select_audio_device(
    pa: pyaudio.PyAudio, 
    direction: Direction,
    guesses: list[str], 
    api_index: int = 0,
) -> int:
    api_info = pa.get_host_api_info_by_index(api_index)
    n_devices: int = api_info['deviceCount']    # type: ignore
    devices = list[str]()
    relevant_indices = list[int]()
    for i in range(n_devices):
        name, do_align = get_device_info(pa, i, direction, api_index)
        devices.append(name)
        if do_align:
            relevant_indices.append(i)
    default = str(guess([
        (i, devices[i]) for i in relevant_indices
    ], guesses) or '')
    print()
    print(direction + 'put Devices:')
    for i in relevant_indices:
        print(i, devices[i])
    selected = int(inputChin('select input device: ', default))
    print()
    print(direction + 'put device:', devices[selected])

    now_name, _ = get_device_info(pa, selected, direction, api_index)
    assert now_name == devices[selected], (
        'Device list changed during selection.'
    )
    return selected

def guess(devices: list[tuple[int, str]], targets: list[str]) -> int | None:
    for t in targets:
        matches = [i for i, name in devices if t in name]
        try:
            index_, = matches
        except ValueError:
            return
        else:
            return index_
    return

if __name__ == '__main__':
    pa = pyaudio.PyAudio()
    try:
        print(select_audio_device_input (pa))
        print(select_audio_device_output(pa))
    finally:
        pa.terminate()
