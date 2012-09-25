# -*- coding: utf-8 -*-

import unittest
import sys

from opus.api import encoder, constants
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
                    fs = sys.maxint
                elif i == -7:
                    fs = -1*(sys.maxint-1)
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
        # TODO: rewrite that code
        # err=opus_encoder_ctl(enc,OPUS_GET_LOOKAHEAD(&i));
        # if(err!=OPUS_OK || i<0 || i>32766)test_failed();
        encoder.destroy(enc)

        enc = encoder.create(48000, 2, constants.APPLICATION_AUDIO)
        # TODO: rewrite that code
        # err=opus_encoder_ctl(enc,OPUS_GET_LOOKAHEAD(&i));
        # if(err!=OPUS_OK || i<0 || i>32766)test_failed();
        encoder.destroy(enc)
