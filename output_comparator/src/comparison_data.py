
class ComparisonData():
    def __init__(self, compared_keyword):
        self.__compared_keyword = compared_keyword
        self.__compared = False
        self.__averageAbsoluteDeviation = 0

    def getKeywordName(self):
        return self.__compared_keyword

    def numberOfTimesteps(self):
        return 0

    def getAverageAbsoluteDeviation(self):
        if (not self.__compared):
            raise RuntimeError("Cannot get average absolute deviation, comparison has not been performed")
        else:
            return self.__averageAbsoluteDeviation

    def setAverageAbsoluteDeviation(self, absolutionDeviation):
        self.__averageAbsoluteDeviation = absolutionDeviation
        self.__compared = True