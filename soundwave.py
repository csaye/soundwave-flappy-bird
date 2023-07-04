import numpy as np
import sounddevice as sd

device_id = None
devices = sd.query_devices()
for index, device in enumerate(devices):
    if 'BlackHole' in device['name']:
        device_id = index
        break

assert device_id is not None, "Could not find device"


def audio_callback(indata, frames, time, status):
    volume_norm = np.linalg.norm(indata)*10
    print('|' + '█' * int(volume_norm) + ' ' * (10 - int(volume_norm)) + '|')


with sd.InputStream(callback=audio_callback, device=device_id):
    while True:
        pass
