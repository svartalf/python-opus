"""Tests for a high-level Decoder object"""

import unittest

from opus.encoder import Encoder
from opus.exceptions import OpusError
from opus.api import constants


class EncoderTest(unittest.TestCase):

    def test_create(self):
        try:
            Encoder(1000, 3, constants.APPLICATION_AUDIO)
        except OpusError as e:
            self.assertEqual(e.code, constants.BAD_ARG)

        Encoder(48000, 2, constants.APPLICATION_AUDIO)

    def test_reset_state(self):
        encoder = Encoder(48000, 2, constants.APPLICATION_AUDIO)
        encoder.reset_state()
