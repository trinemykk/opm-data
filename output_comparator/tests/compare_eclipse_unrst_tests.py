import unittest
from unittest import TestCase
from compare_eclipse import compareRestarts
from ert.ecl import EclFile



class UNRSTTestWithResultData(TestCase):
    def test_compareRestartKeyword_identicaltuple_averagedeviationiszero(self):
        restart_file_A = EclFile("../testdata/SPE1AUTODIFF.UNRST")
        restart_file_B = EclFile("../testdata/SPE1AUTODIFF.UNRST")
        comparison_result = compareRestarts(restart_file_A, restart_file_B, "SGAS")
        self.assertEqual(0.0, comparison_result.getAverageAbsoluteDeviation())
        self.assertEqual(0.0, comparison_result.getAverageRelativeDeviation())
        self.assertEqual(0.0, comparison_result.getMedianAbsoluteDeviation())
        self.assertEqual(0.0, comparison_result.getMedianRelativeDeviation())

    def test_compareRestartKeyword_differentData_SGAS_deviationstats_are_correct(self):
        restart_file_A = EclFile("../testdata/SPE1AUTODIFF.UNRST")
        restart_file_B = EclFile("../testdata/SPE1ECLIPSE.UNRST")
        comparison_result = compareRestarts(restart_file_A, restart_file_B, "SGAS")
        self.assertAlmostEqual(0.00465, comparison_result.getAverageAbsoluteDeviation(), 5)
        self.assertAlmostEqual(0.03575, comparison_result.getAverageRelativeDeviation(), 4)
        self.assertAlmostEqual(0.0034, comparison_result.getMedianAbsoluteDeviation(), 5)
        self.assertAlmostEqual(0.0117, comparison_result.getMedianRelativeDeviation(), 3)

    def test_compareRestartKeyword_differentData_SWAT_deviationstats_are_correct(self):
        restart_file_A = EclFile("../testdata/SPE1AUTODIFF.UNRST")
        restart_file_B = EclFile("../testdata/SPE1ECLIPSE.UNRST")
        comparison_result = compareRestarts(restart_file_A, restart_file_B, "SWAT")
        self.assertAlmostEqual(2.7e-06, comparison_result.getAverageAbsoluteDeviation(), 6)
        self.assertAlmostEqual(2.3e-05, comparison_result.getAverageRelativeDeviation(), 6)
        self.assertAlmostEqual(2.44e-06, comparison_result.getMedianAbsoluteDeviation(), 7)
        self.assertAlmostEqual(2.05e-05, comparison_result.getMedianRelativeDeviation(), 7)

    def test_compareRestartKeyword_differentData_PRESSURE_deviationstats_are_correct(self):
        restart_file_A = EclFile("../testdata/SPE1AUTODIFF.UNRST")
        restart_file_B = EclFile("../testdata/SPE1ECLIPSE.UNRST")
        comparison_result = compareRestarts(restart_file_A, restart_file_B, "PRESSURE")
        self.assertAlmostEqual(6e-04, comparison_result.getAverageRelativeDeviation(), 4)
        self.assertAlmostEqual(3.76085, comparison_result.getAverageAbsoluteDeviation(), 4)
        self.assertAlmostEqual(3.334, comparison_result.getMedianAbsoluteDeviation(), 3)
        self.assertAlmostEqual(0.00052, comparison_result.getMedianRelativeDeviation(), 5)

if __name__ == '__main__':
    unittest.main()
