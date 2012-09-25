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

unimplemented = query(constants.UNIMPLEMENTED)

get_final_range = get(constants.GET_FINAL_RANGE_REQUEST, ctypes.c_uint)

get_lookahead_request = get(constants.GET_LOOKAHEAD_REQUEST, ctypes.c_int)

get_bandwidth = get(constants.GET_BANDWIDTH_REQUEST, ctypes.c_int)

get_pitch = get(constants.GET_PITCH_REQUEST, ctypes.c_int)

get_gain = get(constants.GET_GAIN_REQUEST, ctypes.c_int)
set_gain = set(constants.SET_GAIN_REQUEST)

reset_state = query(constants.RESET_STATE)
