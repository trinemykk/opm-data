import sys

from ert.ecl import EclFile, EclGrid
from comparison_data import ComparisonData

def findDeviationsThroughAllReportSteps(absolute_deviations, relative_deviations, restart_file_A, restart_file_B, keyword):
    ecl_kw_list_A = restart_file_A[keyword]
    ecl_kw_list_B = restart_file_B[keyword]

    if len(ecl_kw_list_B) != len(ecl_kw_list_B):
        print("Different number of report steps")
        exit(1)

    for report_step in range(0, len(ecl_kw_list_A)):
        A_values_in_step_i = ecl_kw_list_A[report_step]
        B_values_in_step_i = ecl_kw_list_B[report_step]

        if len(A_values_in_step_i) != len(B_values_in_step_i):
            print(
                "Error: files {0} and {1} does not have the same number of active cells in report step {2}, {3} and {4}".
                format(ecl_kw_list_A, ecl_kw_list_B, report_step, A_values_in_step_i, B_values_in_step_i))
            exit(1)

        for active_cell in range(0, len(A_values_in_step_i)):
            cell_value_A = A_values_in_step_i[active_cell]
            cell_value_B = B_values_in_step_i[active_cell]

             # Set negative values to 0
            if (cell_value_A < 0):

                print("Warning, for keyword {0} a cell has negative value ({1}) - setting it to zero for comparison. Originating file: {2}".format(keyword, cell_value_A, restart_file_A))
                cell_value_A = 0
                
            if (cell_value_B < 0):
                print("Warning, for keyword {0} a cell has negative value ({1}) - setting it to zero for comparison. Originating file: {2}".format(keyword, cell_value_B, restart_file_B))
                cell_value_B = 0
            
            if cell_value_B != cell_value_A or (cell_value_A != 0.0 or cell_value_B != 0.0):
                absolute_deviation = abs(cell_value_A - cell_value_B)
                absolute_deviations.append(absolute_deviation)
                deviation_as_part_of_biggest_number = absolute_deviation / float(max(cell_value_A, cell_value_B))
                relative_deviations.append(deviation_as_part_of_biggest_number)


def compareValuesForKeyword(restart_file_A, restart_file_B, result_data, keyword):
    absolute_deviations = []
    relative_deviations = []
    findDeviationsThroughAllReportSteps(absolute_deviations, relative_deviations, restart_file_A, restart_file_B, keyword)
    absolute_deviations.sort()
    relative_deviations.sort()

    average_absolute_deviations = 0
    if len(absolute_deviations) > 0:
        average_absolute_deviations = sum(absolute_deviations) / float(len(absolute_deviations))
    result_data.setAverageAbsoluteDeviation(average_absolute_deviations)

    average_relative_deviations = 0
    if len(relative_deviations) > 0:
        average_relative_deviations = sum(relative_deviations) / float(len(relative_deviations))
    result_data.setAverageRelativeDeviation(average_relative_deviations)

    median_position_absolute = len(absolute_deviations) / 2
    median_position_relative = len(relative_deviations) / 2

    result_data.setMedianAbsoluteDeviation(absolute_deviations[median_position_absolute])
    result_data.setMedianRelativeDeviation(relative_deviations[median_position_relative])

    keyword_kw_A = restart_file_A[keyword]
    keyword_kw_B = restart_file_B[keyword]

    result_data.setMinMaxForFirstStepAB(keyword_kw_A[0].getMinMax(), keyword_kw_B[0].getMinMax())
    
    return result_data



def compareRestarts(restart_file_A, restart_file_B, keyword):
    comparison_data = ComparisonData(keyword)
    result_data = compareValuesForKeyword(restart_file_A, restart_file_B, comparison_data, keyword)
    return result_data


def compareRestartFiles(eclipse_restart_file, opm_restart_file, rel_tolerance, abs_tolerance):

    comparison_data_sgas = compareRestarts(eclipse_restart_file, opm_restart_file, "SGAS")
    sgas_good = comparison_data_sgas.getAverageAbsoluteDeviation() <= abs_tolerance
    print "\n"
    print "Average absolute deviation must be lower than ({0}) for SGAS results to be OK".format(abs_tolerance)
    comparison_data_sgas.printInformation(sgas_good)

    comparison_data_swat = compareRestarts(eclipse_restart_file, opm_restart_file, "SWAT")
    swat_good = comparison_data_swat.getAverageAbsoluteDeviation() <= abs_tolerance

    print "\n"
    print "Average absolute deviation must be lower than ({0}) for SWAT results to be OK".format(abs_tolerance)
    comparison_data_swat.printInformation(swat_good)

    comparison_data_pressure = compareRestarts(eclipse_restart_file, opm_restart_file, "PRESSURE")
    pressure_good = comparison_data_pressure.getAverageRelativeDeviation() <= rel_tolerance

    print "\n"
    print "Average relative deviation must be lower than ({0}) for PRESSURE results to be OK".format(rel_tolerance)
    comparison_data_pressure.printInformation(pressure_good)

    if sgas_good and swat_good and pressure_good:
        exit(0)
    else:
        print "\nWarning: one or more of the restart types had too deviating results"
        exit(1)


def main( eclipse_file_location , opm_file_location ,  base_name , rel_tolerance, abs_tolerance):
    print "Using relative tolerance of: " + str(rel_tolerance)
    print "Using absolute tolerance of: " + str(abs_tolerance)

    eclipse_restart_file = EclFile(eclipse_file_location + base_name + ".UNRST")
    eclipse_grid_file = EclGrid(eclipse_file_location + base_name + ".EGRID")

    opm_restart_file = EclFile(opm_file_location + base_name + ".UNRST")
    opm_grid_file = EclGrid(opm_file_location + base_name + ".EGRID")

    grids_equal = eclipse_grid_file.equal(opm_grid_file, include_lgr=True, verbose=True)
    if not grids_equal:
        print("The grids in files {0} and {1} are not equal!".format(eclipse_grid_file.name, opm_grid_file.name))
        exit(1)

    compareRestartFiles(eclipse_restart_file, opm_restart_file, rel_tolerance, abs_tolerance)


if __name__ == '__main__':
    if len(sys.argv) != 6:
        print("Script for comparison of ECLIPSE output from two output sets.\n")
        print("Usage: python compare_eclipse.py arg1 arg2 arg3 arg4 arg5, where\n"
              "arg1 = <path to folder for ECLIPSE output 1>\n"
              "arg2 = <path to folder for ECLIPSE output 2>\n"
              "arg3 = <base input (deck) name, without .DATA>\n"
              "arg4 = <relative tolerance, between 0 and 1, used for PRESSURE>\n"
              "arg5 = <absolute tolerance, used for SGAS and SWAT>\n")
        exit(0)

    eclipse_file_location = sys.argv[1]
    opm_file_location = sys.argv[2]
    base_name = sys.argv[3]
    rel_tolerance = float(sys.argv[4])
    abs_tolerance = float(sys.argv[5])

    main( eclipse_file_location , opm_file_location ,  base_name , rel_tolerance, abs_tolerance)
