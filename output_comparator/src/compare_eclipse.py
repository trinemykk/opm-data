import sys

from ert.ecl import EclFile, EclGrid
from comparison_data import ComparisonData

def findDeviationsThroughAllReportSteps(absolute_deviations, relative_deviations, ecl_kw_list_A, ecl_kw_list_B):
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

            if cell_value_B != cell_value_A or (cell_value_A != 0.0 or cell_value_B != 0.0):
                absolute_deviation = abs(cell_value_A - cell_value_B)
                absolute_deviations.append(absolute_deviation)

                deviation_as_part_of_biggest_number = abs(cell_value_A - cell_value_B) / float(max(cell_value_A, cell_value_B))
                relative_deviations.append(deviation_as_part_of_biggest_number)


def compareValuesForKeyword(ecl_kw_list_A, ecl_kw_list_B, result_data):
    if len(ecl_kw_list_B) != len(ecl_kw_list_B):
        print("Different number of report steps")
        exit(1)

    absolute_deviations = []
    relative_deviations = []
    findDeviationsThroughAllReportSteps(absolute_deviations, relative_deviations, ecl_kw_list_A, ecl_kw_list_B)
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

    return result_data



def compareRestarts(restart_file_A, restart_file_B, keyword):
    comparison_data = ComparisonData(keyword)
    result_data = compareValuesForKeyword(restart_file_A[keyword], restart_file_B[keyword], comparison_data)
    return result_data


def compareRestartFiles(eclipse_restart_file, opm_restart_file, rel_tolerance, abs_tolerance):
    all_good = True
    comparison_data_sgas = compareRestarts(eclipse_restart_file, opm_restart_file, "SGAS")
    all_good &= comparison_data_sgas.getAverageAbsoluteDeviation() <= abs_tolerance

    print "\n"
    comparison_data_sgas.printInformation()

    comparison_data_swat = compareRestarts(eclipse_restart_file, opm_restart_file, "SWAT")
    all_good &= comparison_data_swat.getAverageAbsoluteDeviation() <= abs_tolerance

    print "\n"
    comparison_data_swat.printInformation()

    comparison_data_pressure = compareRestarts(eclipse_restart_file, opm_restart_file, "PRESSURE")
    all_good &= comparison_data_pressure.getAverageRelativeDeviation() <= rel_tolerance

    print "\n"
    comparison_data_pressure.printInformation()

    if not all_good:
        exit(1)
    else:
        exit(0)


def main( eclipse_file_location , opm_file_location ,  base_name , rel_tolerance, abs_tolerance):
    eclipse_restart_file = EclFile(eclipse_file_location + base_name + ".UNRST")
    eclipse_grid_file = EclGrid(eclipse_file_location + base_name + ".EGRID")

    opm_restart_file = EclFile(opm_file_location + base_name + ".UNRST")
    opm_grid_file = EclGrid(opm_file_location + base_name + ".EGRID")

    grids_equal = eclipse_grid_file.equal(opm_grid_file, include_lgr=True, verbose=True)
    if not grids_equal:
        print("The grids in files {0} and {1} are not equal!".format(eclipse_grid_file.name, opm_grid_file.name))
        exit(1)

    if compareRestartFiles(eclipse_restart_file, opm_restart_file, rel_tolerance, abs_tolerance):
        print("All within the acceptable difference")
        exit(0)
    else:
        print("Too large differences observered")
        exit(1)


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
