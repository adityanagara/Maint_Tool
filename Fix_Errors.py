#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      t0136261
#
# Created:     07/01/2014
# Copyright:   (c) t0136261 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import re
import clearcase
import os

'''
    This package will have the functions to fix all the errors and be called in the main program
    based on the error type.
    1. error_1: missing_func_param: This error deals with the case when there is a missing argument in a
    method. It will create a global variable(Given by the user) initialize it in each test and assign this global
    variable to each of the methods where it has been found missing.

'''
class Fix_Errors():
    def missing_func_param(self,file_list,line,variable_init,param):
        final_file_list = []
        for file in file_list:
            if file not in final_file_list:
                final_file_list.append(file)

        for file in final_file_list:
            if not clearcase.is_checked_out(file):
                clearcase.checkout(file)
        a1 = '"'
        my_re = re.escape(a1) + r'(.*)' + re.escape(a1) + ' in call to "(.*)"'
        k = re.search(my_re,line)
        #print k.group(1)
        # Lot of opportuinities for optimization in this area, if you notice the file gets opened and
        # closed 4 times, we can open and close  just once. This will reduce run time
        print k.group(2)
        for file in final_file_list:
            base_name = os.path.basename(file)[:-4]
            read1 = open (file,'r')
            lines = read1.readlines()
            print(base_name)
            index_of = lines.index('package body ' + base_name + ' is\n')
            #variable_init = 'G_Use_ICAO_Altitude_State_Conditions : boolian := True;'
            lines.insert(index_of + 1,variable_init)
            read1.close()
            write1 = open (file,'w')
            write1.write(''.join(lines))
            write1.close()
            g = open (file,'r')
            lines = g.read()
            g.close()
            find = re.findall(re.escape('.') + k.group(2) + '(.*?);',lines,re.DOTALL|re.IGNORECASE)
            for line in find:
                if line <> '':
                    list1 = line.split(',')
                    list1.insert(2,'\n'+param)
                    new_string = ",".join(list1)
                    lines = lines.replace(line,new_string)
                    g = open (file,'w')
                    g.write(lines)
                    g.close()
