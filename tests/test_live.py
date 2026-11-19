import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import live_session as L


class Spike(unittest.TestCase):
    quiet = [3, 4, 2, 3, 5, 3, 4, 3, 2, 4] * 3

    def test_big_burst_is_a_spike(self):
        self.assertTrue(L.is_spike(30, self.quiet))

    def test_normal_chat_is_not(self):
        for c in (0, 3, 5, 7):
            self.assertFalse(L.is_spike(c, self.quiet), c)

    def test_needs_minimum_messages(self):
        self.assertFalse(L.is_spike(L.MIN_MSGS - 1, [0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0] * 2))

    def test_needs_history(self):
        self.assertFalse(L.is_spike(50, [1, 2, 3]))
        self.assertFalse(L.is_spike(50, [0] * 30))

    def test_busy_chat_needs_a_bigger_jump(self):
        busy = [60, 70, 65, 80, 75, 62, 68, 71, 66, 74] * 3
        self.assertFalse(L.is_spike(90, busy))       # busy chat getting a bit busier
        self.assertTrue(L.is_spike(400, busy))

    def test_ratio_rule(self):
        # high variance chat: above mean + 2.5 sd is not enough unless also 2.5x the mean
        wild = [2, 40, 3, 45, 2, 38, 4, 42, 3, 41] * 3
        self.assertFalse(L.is_spike(60, wild))


class Targets(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(L.parse_target('kaicenat')[:2], ('twitch', 'kaicenat'))
        self.assertEqual(L.parse_target('https://www.twitch.tv/XQC')[:2], ('twitch', 'xqc'))
        self.assertEqual(L.parse_target('https://www.youtube.com/watch?v=hwSg39yIBGU')[:2], ('youtube', 'hwSg39yIBGU'))
        self.assertEqual(L.parse_target('https://youtu.be/hwSg39yIBGU')[:2], ('youtube', 'hwSg39yIBGU'))
        self.assertEqual(L.parse_target('https://www.youtube.com/live/hwSg39yIBGU')[:2], ('youtube', 'hwSg39yIBGU'))
        for bad in ('', 'ab', 'a b c', 'https://youtube.com/@name'):
            with self.assertRaises(ValueError):
                L.parse_target(bad)


if __name__ == '__main__':
    unittest.main()
