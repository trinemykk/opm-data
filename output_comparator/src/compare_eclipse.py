import sys

from ert.ecl import EclFile, EclGrid
from comparison_data import ComparisonData


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


def compareRestartFiles(eclipse_restart_file, opm_restart_file, rel_tolerance, abs_tolerance):
    number_of_failed_comparisons = 0
    number_of_failed_comparisons = compareRestartKeyword(eclipse_restart_file, opm_restart_file, "SGAS", abs_tolerance, False)
    number_of_failed_comparisons += compareRestartKeyword(eclipse_restart_file, opm_restart_file, "SWAT", abs_tolerance, False)
    number_of_failed_comparisons += compareRestartKeyword(eclipse_restart_file, opm_restart_file, "PRESSURE", rel_tolerance, True)

    print("Done - in total {0} failed comparisons.".format(number_of_failed_comparisons))
    return number_of_failed_comparisons == 0


def compareRestartKeyword(eclipse_restart_file, opm_restart_file, keyword, tolerance, use_relative_tolerance):
    number_of_mismatches = 0
    print("Processing keyword {0}".format(keyword))
    if len(eclipse_restart_file[keyword]) != len(opm_restart_file[keyword]):
        print("Error: files {0} and {1} does not have the same number of report steps for {4}, {2} and {3}".
              format(eclipse_restart_file, opm_restart_file, len(eclipse_restart_file[keyword]),
                     len(opm_restart_file[keyword]), keyword))
        exit(1)

    print ("Number of report steps for keyword {0} in {1}: {2}".format(keyword, eclipse_restart_file.name,
                                                               len(eclipse_restart_file[keyword])))

    all_ok = True
    for report_step in range(0, len(eclipse_restart_file[keyword])):
        eclipse_sgas_step_i = eclipse_restart_file[keyword][report_step]
        opm_sgas_step_i = opm_restart_file[keyword][report_step]

        if len(eclipse_sgas_step_i) != len(opm_sgas_step_i):
            print(
                "Error: files {0} and {1} does not have the same number of active cells in report step {2}, {3} and {4}".
                format(eclipse_restart_file, opm_restart_file, report_step, eclipse_sgas_step_i, eclipse_sgas_step_i))
            exit(1)

        num_mismatch_in_report_step = 0
        for active_cell in range(0, len(eclipse_sgas_step_i)):
            saturation_value_eclipse = eclipse_sgas_step_i[active_cell]
            saturation_value_opm = opm_sgas_step_i[active_cell]

            if not close(saturation_value_eclipse, saturation_value_opm, tolerance, use_relative_tolerance):
                all_ok = False
                if num_mismatch_in_report_step < 5:
                    print("Error: {0} value in files {1} and {2} in report step {3}, active cell number {4} does not match: {5} != {6}".
                    format(keyword, eclipse_restart_file, opm_restart_file, report_step, active_cell, saturation_value_eclipse,
                           saturation_value_opm))
                num_mismatch_in_report_step += 1

        if num_mismatch_in_report_step >= 5:
            # To truncate output a bit
            print("... in total " + str(num_mismatch_in_report_step) + " mismatches in report step")

        number_of_mismatches+=num_mismatch_in_report_step

    return number_of_mismatches


def close(input_A, input_B, tolerance, use_relative_tolerance):
    if input_A == input_B:
        return True
    elif use_relative_tolerance:
        deviation_as_part_of_biggest_number = abs(input_A - input_B) / float(max(input_A, input_B))
        return deviation_as_part_of_biggest_number <= tolerance
    else:
        return abs(input_A - input_B) <= tolerance


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

    print absolute_deviations
    print relative_deviations

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
