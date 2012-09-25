"""CTL macros rewritten to Python

Usage example:

    from opus import decoder, ctl

    dec = decoder.create(48000, 2)
    decoder.ctl(dec, ctl.set_gain, -15)
    gain_value = decoder.ctl(dec, ctl.get_gain)

"""

import ctypes

import constants
from info import strerror
from exceptions import OpusError


def query(request):
    """Query encoder/decoder with a request value"""

    def inner(func, obj):
        result_code = func(obj, request)

        if result_code is not constants.OK:
            raise OpusError(result_code, strerror(result_code))

        return result_code

    return inner


def get(request, result_type):
    """Get CTL value from a encoder/decoder"""

    def inner(func, obj):
        result = result_type()
        result_code = func(obj, request, ctypes.byref(result))

        if result_code is not constants.OK:
            raise OpusError(result_code, strerror(result_code))

        return result.value

    return inner


def set(request):
    """Set new CTL value to a encoder/decoder"""

    def inner(func, obj, value):
        result_code = func(obj, request, value)
        if result_code is not constants.OK:
            raise OpusError(result_code, strerror(result_code))

    return inner

#
# Generic CTLs
#

# Resets the codec state to be equivalent to a freshly initialized state
reset_state = query(constants.RESET_STATE)

# Gets the final state of the codec's entropy coder
get_final_range = get(constants.GET_FINAL_RANGE_REQUEST, ctypes.c_uint)

# Gets the encoder's configured bandpass or the decoder's last bandpass
get_bandwidth = get(constants.GET_BANDWIDTH_REQUEST, ctypes.c_int)

# Gets the pitch of the last decoded frame, if available
get_pitch = get(constants.GET_PITCH_REQUEST, ctypes.c_int)

# Configures the depth of signal being encoded
set_lsb_depth = set(constants.SET_LSB_DEPTH_REQUEST)

# Gets the encoder's configured signal depth
get_lsb_depth = get(constants.GET_LSB_DEPTH_REQUEST, ctypes.c_int)

#
# Decoder related CTLs
#

# Gets the decoder's configured gain adjustment
get_gain = get(constants.GET_GAIN_REQUEST, ctypes.c_int)

# Configures decoder gain adjustment
set_gain = set(constants.SET_GAIN_REQUEST)

#
# Encoder related CTLs
#

get_lookahead = get(constants.GET_LOOKAHEAD_REQUEST, ctypes.c_int)


#
# Other stuff
#

unimplemented = query(constants.UNIMPLEMENTED)
