# -*- coding: utf-8 -*-

import ctypes
from ctypes.util import find_library

from info import strerror
import constants


libopus = ctypes.CDLL(find_library('opus'))
c_int_pointer = ctypes.POINTER(ctypes.c_int)


class Decoder(ctypes.Structure):
    """Opus decoder state.

    This contains the complete state of an Opus decoder.
    """

    pass

DecoderPointer = ctypes.POINTER(Decoder)


get_size = libopus.opus_decoder_get_size
get_size.argtypes = (ctypes.c_int,)
get_size.restype = ctypes.c_int
get_size.__doc__ = 'Gets the size of an OpusDecoder structure'


_create = libopus.opus_decoder_create
_create.argtypes = (ctypes.c_int, ctypes.c_int, c_int_pointer)
_create.restype = DecoderPointer

def create(fs, channels):
    """Allocates and initializes a decoder state"""

    result_code = ctypes.c_int()

    result = _create(fs, channels, ctypes.byref(result_code))
    if result_code.value != 0:
        raise ValueError(strerror(result_code.value))

    return result


_packet_get_bandwidth = libopus.opus_packet_get_bandwidth
_packet_get_bandwidth.argtypes = (ctypes.c_char_p,)
_packet_get_bandwidth.restype = ctypes.c_int

def packet_get_bandwidth(data):
    """Gets the bandwidth of an Opus packet."""

    data_pointer = ctypes.c_char_p(data)

    result = _packet_get_bandwidth(data_pointer)
    if result == constants.INVALID_PACKET:
        raise ValueError('The compressed data passed is corrupted or of an unsupported type')

    return result


_packet_get_nb_channels = libopus.opus_packet_get_nb_channels
_packet_get_nb_channels.argtypes = (ctypes.c_char_p,)
_packet_get_nb_channels.restype = ctypes.c_int

def packet_get_nb_channels(data):
    """Gets the number of channels from an Opus packet"""

    data_pointer = ctypes.c_char_p(data)

    result = _packet_get_nb_channels(data_pointer)
    if result == constants.INVALID_PACKET:
        raise ValueError('The compressed data passed is corrupted or of an unsupported type')

    return result


destroy = libopus.opus_decoder_destroy
destroy.argtypes = (DecoderPointer,)
destroy.restype = None
destroy.__doc__ = 'Frees an OpusDecoder allocated by opus_decoder_create()'

if __name__ == '__main__':
    decoder = create(12000, 2)
    print get_size(1)
    print get_size(2)
    print packet_get_bandwidth('some strange data')
    print packet_get_nb_channels('another strange data')
    destroy(decoder)
