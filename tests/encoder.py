# -*- coding: utf-8 -*-

import ctypes
import sys
try:
    import unittest2 as unittest # For Python<=2.6
except ImportError:
    import unittest

from opus.api import encoder, constants, ctl
from opus.exceptions import OpusError


class EncoderTest(unittest.TestCase):
    """Encoder basic API tests

    From the `tests/test_opus_api.c`
    """

    def _test_unsupported_sample_rates(self):
        for c in range(0, 4):
            for i in range(-7, 96000+1):

                if i in (8000, 12000, 16000, 24000, 48000) and c in (1, 2):
                    continue

                if i == -5:
                    fs = -8000
                elif i == -6:
                    fs = sys.maxint  # TODO: Must be an INT32_MAX
                elif i == -7:
                    fs = -1*(sys.maxint-1)  # TODO: Must be an INT32_MIN
                else:
                    fs = i

                try:
                    encoder.create(fs, c, constants.APPLICATION_VOIP)
                except OpusError as e:
                    self.assertEqual(e.code, constants.BAD_ARG)

    def test_create(self):
        try:
            encoder.create(48000, 2, constants.AUTO)
        except OpusError as e:
            self.assertEqual(e.code, constants.BAD_ARG)

        enc = encoder.create(48000, 2, constants.APPLICATION_VOIP)
        encoder.destroy(enc)

        enc = encoder.create(48000, 2, constants.APPLICATION_RESTRICTED_LOWDELAY)
        i = encoder.ctl(enc, ctl.get_lookahead)
        # TODO: rewrite that code
        # if(err!=OPUS_OK || i<0 || i>32766)test_failed();
        encoder.destroy(enc)

        enc = encoder.create(48000, 2, constants.APPLICATION_AUDIO)
        i = encoder.ctl(enc, ctl.get_lookahead)
        # TODO: rewrite that code
        # err=opus_encoder_ctl(enc,OPUS_GET_LOOKAHEAD(&i));
        # if(err!=OPUS_OK || i<0 || i>32766)test_failed();
        encoder.destroy(enc)

    def test_encode(self):
        enc = encoder.create(48000, 2, constants.APPLICATION_AUDIO)
        data = chr(0)*ctypes.sizeof(ctypes.c_short)*2*960
        encoder.encode(enc, data, 960, len(data))
        encoder.destroy(enc)

    def test_encode_float(self):
        enc = encoder.create(48000, 2, constants.APPLICATION_AUDIO)
        data = chr(0)*ctypes.sizeof(ctypes.c_float)*2*960
        encoder.encode_float(enc, data, 960, len(data))
        encoder.destroy(enc)

    def test_unimplemented(self):
        enc = encoder.create(48000, 2, constants.APPLICATION_AUDIO)
        try:
            encoder.ctl(enc, ctl.unimplemented)
        except OpusError as e:
            self.assertEqual(e.code, constants.UNIMPLEMENTED)

        encoder.destroy(enc)

    def test_application(self):
        self.check_setget(ctl.set_application, ctl.get_application, (-1, constants.AUTO),
            (constants.APPLICATION_AUDIO, constants.APPLICATION_RESTRICTED_LOWDELAY))

    def test_bitrate(self):
        enc = encoder.create(48000, 2, constants.APPLICATION_AUDIO)

        encoder.ctl(enc, ctl.set_bitrate, 1073741832)

        value = encoder.ctl(enc, ctl.get_bitrate)
        self.assertLess(value, 700000)
        self.assertGreater(value, 256000)

        encoder.destroy(enc)

        self.check_setget(ctl.set_bitrate, ctl.get_bitrate, (-12345, 0), (500, 256000))

    def test_force_channels(self):
        self.check_setget(ctl.set_force_channels, ctl.get_force_channels, (-1, 3), (1, constants.AUTO))

    def test_bandwidth(self):
        enc = encoder.create(48000, 2, constants.APPLICATION_AUDIO)

        # Set bandwidth
        i = -2
        self.assertRaises(OpusError, lambda: encoder.ctl(enc, ctl.set_bandwidth, i))
        i = constants.BANDWIDTH_FULLBAND+1
        self.assertRaises(OpusError, lambda: encoder.ctl(enc, ctl.set_bandwidth, i))
        i = constants.BANDWIDTH_NARROWBAND
        encoder.ctl(enc, ctl.set_bandwidth, i)
        i = constants.BANDWIDTH_FULLBAND
        encoder.ctl(enc, ctl.set_bandwidth, i)
        i = constants.BANDWIDTH_WIDEBAND
        encoder.ctl(enc, ctl.set_bandwidth, i)
        i = constants.BANDWIDTH_MEDIUMBAND
        encoder.ctl(enc, ctl.set_bandwidth, i)

        # Get bandwidth
        i = -12345
        value = encoder.ctl(enc, ctl.get_bandwidth)
        self.assertIn(value, (constants.BANDWIDTH_FULLBAND, constants.BANDWIDTH_MEDIUMBAND, constants.BANDWIDTH_WIDEBAND,
            constants.BANDWIDTH_NARROWBAND, constants.AUTO))

        encoder.ctl(enc, ctl.set_bandwidth, constants.AUTO)

        encoder.destroy(enc)

    def test_max_bandwidth(self):
        enc = encoder.create(48000, 2, constants.APPLICATION_AUDIO)

        i = -2
        self.assertRaises(OpusError, lambda: encoder.ctl(enc, ctl.set_max_bandwidth, i))
        i = constants.BANDWIDTH_FULLBAND+1
        self.assertRaises(OpusError, lambda: encoder.ctl(enc, ctl.set_max_bandwidth, i))
        i = constants.BANDWIDTH_NARROWBAND
        encoder.ctl(enc, ctl.set_max_bandwidth, i)
        i = constants.BANDWIDTH_FULLBAND
        encoder.ctl(enc, ctl.set_max_bandwidth, i)
        i = constants.BANDWIDTH_WIDEBAND
        encoder.ctl(enc, ctl.set_max_bandwidth, i)
        i = constants.BANDWIDTH_MEDIUMBAND
        encoder.ctl(enc, ctl.set_max_bandwidth, i)

        i = -12345
        value = encoder.ctl(enc, ctl.get_max_bandwidth)
        self.assertIn(value, (constants.BANDWIDTH_FULLBAND, constants.BANDWIDTH_MEDIUMBAND, constants.BANDWIDTH_WIDEBAND,
            constants.BANDWIDTH_NARROWBAND, constants.AUTO))

        encoder.destroy(enc)

    def test_dtx(self):
        self.check_setget(ctl.set_dtx, ctl.get_dtx, (-1, 2), (1, 0))

    def test_complexity(self):
        self.check_setget(ctl.set_complexity, ctl.get_complexity, (-1, 11), (0, 10))

    def test_inband_fec(self):
        self.check_setget(ctl.set_inband_fec, ctl.get_inband_fec, (-1, 2), (1, 0))

    def test_packet_loss_perc(self):
        self.check_setget(ctl.set_packet_loss_perc, ctl.get_packet_loss_perc, (-1, 101), (100, 0))

    def test_vbr(self):
        self.check_setget(ctl.set_vbr, ctl.get_vbr, (-1, 2), (1, 0))

    def test_vbr_constraint(self):
        self.check_setget(ctl.set_vbr_constraint, ctl.get_vbr_constraint, (-1, 2), (1, 0))

    def test_signal(self):
        self.check_setget(ctl.set_signal, ctl.get_signal, (-12345, 0x7FFFFFFF), (constants.SIGNAL_MUSIC, constants.AUTO))

    def test_lsb_depth(self):
        self.check_setget(ctl.set_lsb_depth, ctl.get_lsb_depth, (7, 25), (16, 24))

    def check_setget(self, set, get, bad, good):
        enc = encoder.create(48000, 2, constants.APPLICATION_AUDIO)

        for value in bad:
            self.assertRaises(OpusError, lambda: encoder.ctl(enc, set, value))

        for value in good:
            encoder.ctl(enc, set, value)
            result = encoder.ctl(enc, get)
            self.assertEqual(value, result)

        encoder.destroy(enc)
