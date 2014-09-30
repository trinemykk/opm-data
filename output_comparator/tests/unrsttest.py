from unittest import TestCase
import unittest
import compare_eclipse


class UNRSTTest(TestCase):
    def test_close_equalvalues_returnstrue(self):
        self.assertTrue(compare_eclipse.close(103213.434, 103213.434, 0.001, True))
        self.assertTrue(compare_eclipse.close(0.0045, 0.0045, 0.001, False))

    def test_close_faroff_returnsfalse(self):
        self.assertFalse(compare_eclipse.close(143433, 34234, 0.001, True))
        self.assertFalse(compare_eclipse.close(0.01323, 0.1231331, 0.001, False))

    def test_close_oneorbothzero_returnscorrect(self):
        self.assertTrue(compare_eclipse.close(0, 0, 0.001, True))
        self.assertFalse(compare_eclipse.close(0, 1, 0.001, True))
        self.assertTrue(compare_eclipse.close(0, 0, 0.001, True))
        self.assertFalse(compare_eclipse.close(0.001, 0, 0.001, True))
        self.assertTrue(compare_eclipse.close(0.001, 0, 0.001, False))

if __name__ == '__main__':
    unittest.main()
