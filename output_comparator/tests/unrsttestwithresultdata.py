import unittest
from unittest import TestCase
from comparison_data import ComparisonData
from compare_eclipse import compareRestarts
from ert.ecl import EclFile



class UNRSTTestWithResultData(TestCase):
    def test_createresultobject_withtitle_titleset(self):
        resultData = ComparisonData("SGAS")
        self.assertEqual("SGAS", resultData.getKeywordName())

    def test_averagedeviation_nodata_averagethrows(self):
        resultData = ComparisonData("TEST")
        with self.assertRaises(RuntimeError):
            resultData.getAverageAbsoluteDeviation()

    def test_comparisondata_addAverageValue_averagevalueSet(self):
        resultData = ComparisonData("TEST")
        resultData.setAverageAbsoluteDeviation(12.43)
        self.assertEqual(12.43, resultData.getAverageAbsoluteDeviation())

    def test_compareRestartKeyword_identicaltuple_averagedeviationiszero(self):
        restart_file_A = EclFile("../testdata/SPE1AUTODIFF.UNRST")
        restart_file_B = EclFile("../testdata/SPE1AUTODIFF.UNRST")
        comparison_result = compareRestarts(restart_file_A, restart_file_B, "SGAS")
        self.assertEqual(0.0, comparison_result.getAverageAbsoluteDeviation())


if __name__ == '__main__':
    unittest.main()
