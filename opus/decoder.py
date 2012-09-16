# -*- coding: utf-8 -*-

import ctypes
from ctypes.util import find_library


libopus = ctypes.CDLL(find_library('opus'))


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


if __name__ == '__main__':
    print get_size(1)
    print get_size(2)
