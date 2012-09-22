# -*- coding: utf-8 -*-

"""Matches to `opus_defines.h`"""

# No Error
OK = 0

# One or more invalid/out of range arguments
BAD_ARG = -1

# The mode struct passed is invalid
BUFFER_TOO_SMALL = -2

# The compressed data passed is corrupted
INVALID_PACKET = -4


# Pre-defined values for CTL interface

APPLICATION_VOIP = 2048
APPLICATION_AUDIO = 2049
APPLICATION_RESTRICTED_LOWDELAY = 2051


# Values for the various encoder CTLs

BANDWIDTH_NARROWBAND = 1101
BANDWIDTH_MEDIUMBAND = 1102
BANDWIDTH_WIDEBAND = 1103
BANDWIDTH_SUPERWIDEBAND = 1104
BANDWIDTH_FULLBAND = 1105
