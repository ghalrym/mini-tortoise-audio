from enum import Enum
from typing import TypedDict, cast
from pyaudio import PyAudio

from .exceptions import DeviceNotFound, NoCableFound


class VbCableOut(Enum):
    CABLE_OUTPUT = "CABLE Input (VB-Audio Virtual C"
    CABLE_A_OUTPUT = "CABLE-A Input (VB-Audio Cable A"
    CABLE_B_OUTPUT = "CABLE-B Input (VB-Audio Cable B"
    CABLE_C_OUTPUT = "CABLE-C Input (VB-Audio Cable C"
    CABLE_D_OUTPUT = "CABLE-D Input (VB-Audio Cable D"


class VbCableIn(Enum):
    CABLE_Input = "CABLE Output (VB-Audio Virtual "
    CABLE_A_Input = "CABLE-A Output (VB-Audio Cable "
    CABLE_B_Input = "CABLE-B Output (VB-Audio Cable "
    CABLE_C_Input = "CABLE-C Output (VB-Audio Cable "
    CABLE_D_Input = "CABLE-C Output (VB-Audio Cable "


class AudioDevice(TypedDict):
    index: int
    structVersion: int
    name: str
    hostApi: int
    maxInputChannels: int
    maxOutputChannels: int
    defaultLowInputLatency: float
    defaultLowOutputLatency: float
    defaultHighInputLatency: float
    defaultHighOutputLatency: float
    defaultSampleRate: float


def get_audio_device(device_name: str) -> AudioDevice:
    audio = PyAudio()
    for i in range(audio.get_device_count()):
        info = audio.get_device_info_by_index(i)
        if info["hostApi"] == 0 and device_name == info['name']:
            return cast(AudioDevice, info)
    raise DeviceNotFound(device_name)


def get_cable(cable: VbCableIn | VbCableOut) -> AudioDevice:
    audio = PyAudio()
    for i in range(audio.get_device_count()):
        info = audio.get_device_info_by_index(i)
        if info["hostApi"] == 0 and cable.value == info['name']:
            return cast(AudioDevice, info)
    raise NoCableFound()
