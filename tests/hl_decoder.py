"""Tests for a high-level Decoder object"""

import unittest

from opus.decoder import Decoder
from opus.exceptions import OpusError
from opus.api import constants


class DecoderTest(unittest.TestCase):

    def test_create(self):
        try:
            Decoder(1000, 3)
        except OpusError as e:
            self.assertEqual(e.code, constants.BAD_ARG)

        Decoder(48000, 2)

    def test_get_bandwidth(self):
        decoder = Decoder(48000, 2)
        self.assertEqual(decoder.bandwidth, 0)

    def test_get_pitch(self):
        decoder = Decoder(48000, 2)

        self.assertIn(decoder.pitch, (-1, 0))

        packet = chr(63<<2)+chr(0)+chr(0)
        decoder.decode(packet, frame_size=960)
        self.assertIn(decoder.pitch, (-1, 0))

        packet = chr(1)+chr(0)+chr(0)
        decoder.decode(packet, frame_size=960)
        self.assertIn(decoder.pitch, (-1, 0))

    def test_gain(self):
        decoder = Decoder(48000, 2)

        self.assertEqual(decoder.gain, 0)

        try:
            decoder.gain = -32769
        except OpusError as e:
            self.assertEqual(e.code, constants.BAD_ARG)

        try:
            decoder.gain = 32768
        except OpusError as e:
            self.assertEqual(e.code, constants.BAD_ARG)

        decoder.gain = -15
        self.assertEqual(decoder.gain, -15)

    def test_reset_state(self):
        decoder = Decoder(48000, 2)
        decoder.reset_state()

    def test_decode(self):
        decoder = Decoder(48000, 2)

        packet = chr((63<<2)+3)+chr(49)
        for j in range(2, 51):
            packet += chr(0)

        try:
            decoder.decode(packet, frame_size=960)
        except OpusError as e:
            self.assertEqual(e.code, constants.INVALID_PACKET)

        packet = chr(63<<2)+chr(0)+chr(0)

        try:
            decoder.decode(packet, frame_size=60)
        except OpusError as e:
            self.assertEqual(e.code, constants.BUFFER_TOO_SMALL)

        try:
            decoder.decode(packet, frame_size=480)
        except OpusError as e:
            self.assertEqual(e.code, constants.BUFFER_TOO_SMALL)

        try:
            decoder.decode(packet, frame_size=960)
        except OpusError:
            self.fail('Decode failed')

    def test_decode_float(self):
        decoder = Decoder(48000, 2)

        packet = chr(63<<2)+chr(0)+chr(0)
        try:
            decoder.decode_float(packet, frame_size=960)
        except OpusError:
            self.fail('Decode failed')
