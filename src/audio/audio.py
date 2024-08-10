from typing import TypedDict, cast

from pyaudio import PyAudio, paInt32, Stream

from .audio_device import get_audio_device, VbCableIn, VbCableOut, get_cable
from .exceptions import StreamNeverOpened


class _PyAudioArgs(TypedDict):
    format: int
    channels: int
    rate: int
    output_device_index: int | None
    input_device_index: int | None
    output: bool
    input: bool


class _ContextAudio(PyAudio):

    def __init__(self, **kwargs):
        super().__init__()
        self._stream = None
        self._open_args: _PyAudioArgs = cast(_PyAudioArgs, kwargs)

    def open(self, *args, **kwargs) -> Stream:
        return super(_ContextAudio, self).open(*args, **(kwargs | self._open_args))

    def __enter__(self) -> "_ContextAudio":
        self._stream = self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._stream is None:
            raise StreamNeverOpened()
        self._stream.stop_stream()
        self._stream.close()
        self.terminate()

    @property
    def audio_format(self):
        return self._open_args["format"]

    @property
    def audio_channels(self):
        return self._open_args["channels"]

    @property
    def rate(self):
        return self._open_args["rate"]


class Audio(_ContextAudio):

    def __init__(self, device: str, is_input: bool):
        device = get_audio_device(device)
        super(Audio, self).__init__(
            **{
                "format": paInt32,  # mini-tortoise-tts outputs 32int format
                "channels": 1,  # mini-tortoise-tts outputs single channel audio
                "rate": 24000,  # mini-tortoise-tts outputs 24k audio
                "output_device_index": device['index'] if not is_input else None,
                "output": not is_input,
                "input_device_index": device['index'] if is_input else None,
                "input": is_input,
            }
        )


class VbCableAudio(_ContextAudio):

    def __init__(self, device: VbCableIn | VbCableOut):
        cable_device = get_cable(device)
        is_input = isinstance(device, VbCableIn)
        super(VbCableAudio, self).__init__(
            **{
                "format": paInt32,  # mini-tortoise-tts outputs 32int format
                "channels": 1,  # mini-tortoise-tts outputs single channel audio
                "rate": 24000,  # mini-tortoise-tts outputs 24k audio
                "output": not is_input,
                "input": is_input,
                "output_device_index": cable_device['index'] if not is_input else None,
                "input_device_index": cable_device['index'] if is_input else None,
            }
        )
        self._stream = None
