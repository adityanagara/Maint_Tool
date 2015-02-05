#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      T0136261(ADI)
#
# Created:     16/12/2013
# Copyright:   (c) t0136261 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python
import csv
import gpr_file
import os
import clearcase
import Fix_Errors
import re

'''
@@@@@This code needs to be modified at three places in order to work for other components
these places are line 30,39,42,92 The change has been specified above the line
Import_Errors:
    This function will import all the errors from the data in the compiled text document TEMP_ITGroup-1.txt
    it will segrigate the errors only and create the error matrix. The error matrix will have the various distinct errors
    and under each error the files in which this particular error occurs will be clubed
'''
def import_errors(dist_errors_list,error_test,new_list):
    # Modification needs to be done at this place to work in any other component give the path of the compile.txt document
    # loop in the case of fixing errors in all the groups together
    error_file = open('N:\T0125397_SOCA_PRED_TEST_TSI_EST_Dyn\cc_FMA4_TRAJPRED\PRED\TEST\FORMAL\A-UNIT\Compil_Results_1\TEMP_ITGroup-11.txt')
    parse_error = []
    file_list = error_file.readlines()
    main_list = []
    all_errors = []
    #Consider only test files in the compile results document
    for lines in file_list:
        if lines[0:3] == 'swu':
            parse_error.append(lines)
    # This temporary text document is used to create the error matrix change the path for other component
    a = open('N:\T0125397_SOCA_PRED_TEST_TSI_EST_Dyn\cc_FMA4_TRAJPRED\PRED\TEST\FORMAL\A-UNIT\Compil_Results_1\ALL_ERRORS.txt','w')
    a.writelines(parse_error)
    a.close()
    # Change this path for other component
    b = open('N:\T0125397_SOCA_PRED_TEST_TSI_EST_Dyn\cc_FMA4_TRAJPRED\PRED\TEST\FORMAL\A-UNIT\Compil_Results_1\ALL_ERRORS.txt')
    #Split each line with : since this seperates Test_File_Name:line number:position:error/warning:type of error/warning
    error_1 = b.readlines()
    for line in error_1:
        k = line.split(':')
        main_list.append(k)
    #Extract only the errors from the previous list
    for line in main_list:
        if line[3] == ' error':
            all_errors.append(line)
    error_list = []
    for line in all_errors:
        error_list.append(line[4])
    dist_errors = {}
    length1 = len(all_errors)
    #Make a list of unique errors --the cound of each error can be implemented using this list
    for line in error_list:
        if line not in dist_errors_list:
            dist_errors_list.append(line)
    error_matrix = []
    length = len(dist_errors_list)
    #The following builds the error matrix
    for i in xrange(len(dist_errors_list)):
        error_matrix.append([])
        for j in xrange(len(all_errors)):
            if dist_errors_list[i] == all_errors[j][4]:
                error_matrix[i].append(all_errors[j][0])
    i = 0
    #Make the dictionary of errors d(error_type) = lins of files where error_type occurs
    for line in dist_errors_list:
        error_test[line] = error_matrix[i]
        i = i + 1
    #print (error_test[dist_errors_list[10]])
    # For now since only one error is taken care of we will only display that error. This can be removed later
    # after more error functions can be written
    for line in dist_errors_list:
        if line[0:31] == ' missing argument for parameter':
            new_list.append(line)


'''
    Get file names:
    This function will give the exact path of each file based on the error, this can then be used by
    clearcase.py to check out the files open the file and perform read/write operations.

'''

def get_file_name(error,error_test,file_names):
    file_path = r'N:\T0125397_SOCA_PRED_TEST_TSI_EST_Dyn\cc_FMA4_TRAJPRED\PRED\TEST\FORMAL\A-UNIT\Compil_Results_1\error_data.xls'
    gpr_file_name = 'N:\T0125397_SOCA_PRED_TEST_TSI_EST_Dyn\cc_FMA4_TRAJPRED\PRED\TEST\FORMAL\A-UNIT\PRED_TEST_NATIVE.gpr'
    # Change this path for other components, more changes might be required here. This function mainly
    # gives the entire path of the file that needs to be checked out.
    file_PRED = 'N:\T0125397_SOCA_PRED_TEST_TSI_EST_Dyn\cc_FMA4_TRAJPRED\PRED\TEST\FORMAL\A-UNIT\Test\PRED'
    #my_gpr_file = gpr_file.GprFile(gpr_file_name)
    #my_file_list = my_gpr_file.get_source_files()
    #file = 'N:\T0125397_SOCA_PRED_TEST_TSI_EST_Dyn\cc_FMA4_TRAJPRED\PRED\TEST\FORMAL\A-UNIT\Test\PRED'
    my_file_list = []
    #This will extract all the test files in PRED and will create a dictionary of d(file name in small) = file fath exactly
    # This causes a lot of run time in the code and can be optimized. This only needs to be run the first time
    # second time the list can be saved in a global variable.
    sub_dirs = [x[0] for x in os.walk(file_PRED)]
    for line in sub_dirs:
        files = os.walk(line).next()[2]
        if (len(files)> 0):
            for file in files:
                my_file_list.append(line + os.sep + file)
    file_dict = {}
    Check_Out_File_Dict = {}
    file_list = []
    file_list = error_test[error]
    # Limit our list to only test files
    for file in my_file_list:
        if os.path.basename(file)[0:3] == 'SwU':
            Check_Out_File_Dict[os.path.basename(file).lower()] = os.path.basename(file)
            file_dict[os.path.basename(file).lower()] = os.path.dirname(file)
    print (Check_Out_File_Dict)
    print (file_list)
    for files in file_list:
        file_names.append(file_dict[files] + os.sep + Check_Out_File_Dict[files])



def get_missing_param_error(error_list,missing_error_list,error_matrix,dist_error_list):
    for error in error_list:
        if error[0:31] == ' missing argument for parameter':
            missing_error_list.append(error)
    print(missing_error_list)
    error1 = ' missing argument for parameter "Speed_Type" in call to "Limit_Speed_By_Flight_Envelope" declared at trajpred-prediction-integration-prediction_phase.ads'
    file_list = error_matrix[error1]
    for file in file_list:
        if file not in dist_error_list:
            dist_error_list.append(file)


def call_error_fixer(file_list,error,variable_init,param):
    error_filter = Fix_Errors.Fix_Errors()
    # This is the error fixer function. Once new functions are written they can be implemented here
    # Use the error input parameter to determine which function needs to be called
    if error[0:31] == ' missing argument for parameter':
        error_filter.missing_func_param(file_list,error,variable_init,param)




