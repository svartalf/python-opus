# -*- coding: utf-8 -*-

import unittest
import sys
import ctypes

from opus import decoder, constants
from opus.exceptions import OpusError


TESTVECTORS = {
    'testvector1.bit': {
        'bitrate': 8000,
        'channels': 2,
        'frames': 1,
    },
}


class DecoderTest(unittest.TestCase):

    def test_get_size(self):
        """Invalid configurations which should fail"""

        for c in range(4):
            i = decoder.get_size(c)
            if c in (1, 2):
                self.assertFalse(1<<16 < i <= 2048)
                pass
            else:
                self.assertEqual(i, 0)

    def _test_unsupported_sample_rates(self):
        """Unsupported sample rates

        TODO: make the same test with a opus_decoder_init() function"""

        for c in range(4):
            for i in range(-7, 96000):
                if i in (8000, 12000, 16000, 24000, 48000) and c in (1, 2):
                    continue

                if i == -5:
                    fs = -8000
                elif i == -6:
                    fs = sys.maxint  # TODO: should be a INT32_MAX
                elif i == -7:
                    fs = -1*(sys.maxint-1)  # Emulation of the INT32_MIN
                else:
                    fs = i

                try:
                    decoder.create(fs, c)
                except OpusError as e:
                    self.assertEqual(e.code, constants.BAD_ARG)

    def test_create(self):
        try:
            decoder.create(48000, 2)
        except OpusError:
            raise AssertionError()

        # TODO: rewrite this code
        # VG_CHECK(dec,opus_decoder_get_size(2));

    def test_decode(self):
        dec = decoder.create(48000, 2)

        packet = ''.join([chr(x) for x in (63<<2, 0, 0)])

        self.assertEqual(960, decoder.decode(dec, packet, 3, 960, False))

    def test_get_nb_samples(self):
        """opus_decoder_get_nb_samples()"""

        dec = decoder.create(48000, 2)

        self.assertEqual(480, decoder.get_nb_samples(dec, '\x00', 1))

        packet = ''.join([chr(x) for x in ((63<<2)|3, 63)])
        # TODO: check for exception code
        self.assertRaises(OpusError, lambda: decoder.get_nb_samples(dec, packet, 2))

    def test_packet_get_nb_frames(self):
        """opus_packet_get_nb_frames()"""

        packet = ''.join([chr(x) for x in ((63<<2)|3, 63)])
        self.assertRaises(OpusError, lambda: decoder.packet_get_nb_frames(packet, 0))

        l1res = (1, 2, 2, constants.INVALID_PACKET)

        for i in range(0, 256):

            packet = chr(i)
            expected_result = l1res[ord(packet[0]) & 3]
            try:
                self.assertEqual(expected_result, decoder.packet_get_nb_frames(packet, 1))
            except OpusError as e:
                if e.code == expected_result:
                    continue

            for j in range(0, 256):
                packet = chr(i)+chr(j)

                self.assertEqual(expected_result if expected_result != 3 else (ord(packet[1]) & 63),
                    decoder.packet_get_nb_frames(packet, 2))

    def test_packet_get_bandwidth(self):
        """opus_packet_get_bandwidth()"""

        for i in range(0, 256):
            packet = chr(i)
            bw = ord(packet[0]) >> 4

            # Very cozy code from the test_opus_api.c
            bw = constants.BANDWIDTH_NARROWBAND+(((((bw&7)*9)&(63-(bw&8)))+2+12*((bw&8)!=0))>>4)

            self.assertEqual(bw, decoder.packet_get_bandwidth(packet))
