# -*- coding: utf-8 -*-

import ctypes
from ctypes.util import find_library


libopus = ctypes.CDLL(find_library('opus'))
c_int_pointer = ctypes.POINTER(ctypes.c_int)


class Decoder(ctypes.Structure):
    """Opus decoder state.

    This contains the complete state of an Opus decoder.
    """

    pass

DecoderPointer = ctypes.POINTER(Decoder)


_get_size = libopus.opus_decoder_get_size
_get_size.argtypes = (ctypes.c_int,)
_get_size.restype = ctypes.c_int

def get_size(channels):
    """Gets the size of an OpusDecoder structure"""

    if not channels in (1, 2):
        raise ValueError()  # TODO: error message

    return _get_size(channels)


_create = libopus.opus_decoder_create
_create.argtypes = (ctypes.c_int, ctypes.c_int, c_int_pointer)
_create.restype = DecoderPointer

def create(fs, channels):
    """Allocates and initializes a decoder state"""

    if fs not in (8000, 12000, 16000, 24000, 48000):
        raise ValueError('Wrong fs value. Must be equal to 8000, 12000, 16000, 24000 or 48000')

    if not channels in (1, 2):
        raise ValueError('Wrong channels value. Must be equal to 1 or 2')

    result_code = ctypes.c_int()

    result = _create(fs, channels, ctypes.byref(result_code))
    # TODO: check for `result_code` value and raise an exception if needed

    return result


destroy = libopus.opus_decoder_destroy
destroy.argtypes = (DecoderPointer,)
destroy.restype = None
destroy.__doc__ = 'Frees an OpusDecoder allocated by opus_decoder_create()'

if __name__ == '__main__':
    decoder = create(12000, 2)
    print get_size(1)
    print get_size(2)
    destroy(decoder)
