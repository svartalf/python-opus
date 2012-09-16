# -*- coding: utf-8 -*-

import ctypes
from ctypes.util import find_library

import constants


libopus = ctypes.CDLL(find_library('opus'))
c_int_pointer = ctypes.POINTER(ctypes.c_int)


class Encoder(ctypes.Structure):
    """Opus encoder state.

    This contains the complete state of an Opus encoder.
    """

    pass

EncoderPointer = ctypes.POINTER(Encoder)


_create = libopus.opus_encoder_create
_create.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.c_int, c_int_pointer)
_create.restype = EncoderPointer

def create(fs, channels, application):
    """Allocates and initializes an encoder state."""

    if fs not in (8000, 12000, 16000, 24000, 48000):
        raise ValueError('Wrong fs value. Must be equal to 8000, 12000, 16000, 24000 or 48000')

    if not channels in (1, 2):
        raise ValueError('Wrong channels value. Must be equal to 1 or 2')

    if not application in (constants.APPLICATION_VOIP, constants.APPLICATION_AUDIO, constants.APPLICATION_RESTRICTED_LOWDELAY):
        raise ValueError('Wrong application value')

    result_code = ctypes.c_int()

    result = _create(fs, channels, application, ctypes.byref(result_code))
    if result_code.value is not 0:
        raise ValueError('Some error was occured, and we need (TODO) to show proper message here')

    return result

if __name__ == '__main__':
    create(12000, 2, constants.APPLICATION_VOIP)