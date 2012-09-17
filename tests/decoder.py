# -*- coding: utf-8 -*-

import unittest

import opus.decoder
import opus.constants


class DecoderStereo8Bit(unittest.TestCase):
    """
    >>> $ opusinfo tests/samples/stereo_8bit.opus
    Processing file "stereo_8bit.opus"...

    New logical stream (#1, serial: 16e8753e): type opus
    Encoded with libopus 1.0.1
    User comments section follows...
            ENCODER=opusenc from opus-tools 0.1.5
    Opus stream 1:
            Pre-skip: 312
            Playback gain: 0 dB
            Channels: 2
            Original sample rate: 8000Hz
            Packet duration:   20.0ms (max),   20.0ms (avg),   20.0ms (min)
            Page duration:   1000.0ms (max),  986.7ms (avg),  960.0ms (min)
            Total data length: 35304 bytes (overhead: 1.18%)
            Playback length: 0m:02.936s
            Average bitrate: 96.18 kb/s, w/o overhead: 95.04 kb/s
    Logical stream 1 ended
    """

    def setUp(self):
        self.data = open('tests/samples/stereo_8bit.opus', 'rb').read()
        self.decoder = opus.decoder.create(8000, 2)  # 8 bit and stereo

    def tearDown(self):
        opus.decoder.destroy(self.decoder)

    def test_get_size(self):
        self.assertEqual(18196, opus.decoder.get_size(1))
        self.assertEqual(26964, opus.decoder.get_size(2))

    def test_packet_get_bandwidth(self):
        self.assertEqual(opus.constants.BANDWIDTH_WIDEBAND, opus.decoder.packet_get_bandwidth(self.data))

    def test_packet_get_nb_channels(self):
        self.assertEqual(2, opus.decoder.packet_get_nb_channels(self.data))

    def test_packet_get_nb_frames(self):
        self.assertEqual(39, opus.decoder.packet_get_nb_frames(self.data, len(self.data)))
        self.assertEqual(39, opus.decoder.packet_get_nb_frames(self.data))

    def test_packet_get_samples_per_frame(self):
        self.assertEqual(39, opus.decoder.packet_get_samples_per_frame(self.data, 8000))
