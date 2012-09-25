import ctypes
from ctypes.util import find_library


libopus = ctypes.CDLL(find_library('opus'))
