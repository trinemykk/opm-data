from unittest import TestCase
import unittest
import compare_eclipse
from ert.ecl import EclFile


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

    def test_compareRestartKeyword_comparefiles_withSGAS(self):
        eclipse_restart = EclFile("../testdata/SPE1ECLIPSE.UNRST")
        opm_restart = EclFile("../testdata/SPE1AUTODIFF.UNRST")
        num_mismatches = compare_eclipse.compareRestartKeyword(eclipse_restart, opm_restart, "SGAS", 0.02, False )
        self.assertEqual(164, num_mismatches)

    def test_compareRestartKeyword_comparefiles_withSWAT(self):
        eclipse_restart = EclFile("../testdata/SPE1ECLIPSE.UNRST")
        opm_restart = EclFile("../testdata/SPE1AUTODIFF.UNRST")

        num_mismatches = compare_eclipse.compareRestartKeyword(eclipse_restart, opm_restart, "SWAT", 0.00002, False )
        self.assertEqual(117, num_mismatches)

    def test_compareRestartKeyword_comparefiles_withPRESSURE(self):
        eclipse_restart = EclFile("../testdata/SPE1ECLIPSE.UNRST")
        opm_restart = EclFile("../testdata/SPE1AUTODIFF.UNRST")

        num_mismatches = compare_eclipse.compareRestartKeyword(eclipse_restart, opm_restart, "PRESSURE", 0.005, True )
        self.assertEqual(141, num_mismatches)

if __name__ == '__main__':
    unittest.main()
