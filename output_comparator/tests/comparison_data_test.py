import unittest
from comparison_data import ComparisonData

class ComparisonDataTests(unittest.TestCase):
    def test_createresultobject_withtitle_titleset(self):
        resultData = ComparisonData("SGAS")
        self.assertEqual("SGAS", resultData.getKeywordName())

    def test_averageabsolutedeviation_nodata_averagethrows(self):
        resultData = ComparisonData("TEST")
        resultData.setAverageRelativeDeviation(0.06)
        with self.assertRaises(RuntimeError):
            resultData.getAverageAbsoluteDeviation()

    def test_comparisondata_addAverageAbsoluteValue_averagevalueSet(self):
        resultData = ComparisonData("TEST")
        resultData.setAverageAbsoluteDeviation(12.43)
        self.assertEqual(12.43, resultData.getAverageAbsoluteDeviation())

    def test_comparisondata_addAverageRelativeValue_averagevalueSet(self):
        resultData = ComparisonData("TEST")
        resultData.setAverageRelativeDeviation(0.00546)
        self.assertEqual(0.00546, resultData.getAverageRelativeDeviation())

    def test_averagerelativedeviation_nodata_averagethrows(self):
        resultData = ComparisonData("TEST")
        resultData.setAverageAbsoluteDeviation(22.33)
        with self.assertRaises(RuntimeError):
            resultData.getAverageRelativeDeviation()

    def test_comparisondata_addAbsoluteMedianValue_medianvalueSet(self):
        resultData = ComparisonData("TEST")
        resultData.setMedianRelativeDeviation(0.0982734)
        self.assertEqual(0.0982734, resultData.getMedianRelativeDeviation())

    def test_comparisondata_addRelativeMedianValue_medianvalueSet(self):
        resultData = ComparisonData("TEST")
        resultData.setMedianAbsoluteDeviation(0.034234)
        self.assertEqual(0.034234, resultData.getMedianAbsoluteDeviation())

    def test_comparisonData_setMinMaxForFirstStepAB_valuesAreSet(self):
        resultData = ComparisonData("TEST")
        resultData.setMinMaxForFirstStepAB([0.001, 1.2], [0.0001, 2.22])
        self.assertEqual([0.001, 1.2], resultData.getMinMaxFirstStepA())
        self.assertEqual([0.0001, 2.22], resultData.getMinMaxFirstStepB())

if __name__ == '__main__':
    unittest.main()
