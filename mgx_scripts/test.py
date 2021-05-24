#
# import sys
#
# for p in sys.path:
#     print(p)
#
# if not hasattr(sys, 'argv'):
#     sys.argv  = ['']
#
# import Tkinter
#
# Tkinter._test()


#  write to file for stepping
# https://docs.python.org/3/tutorial/inputoutput.html
import os
import sys

path = os.path.abspath(os.getcwd())

dirs_dict ={'meshes': ['d', 'd2', 'd3']}


# if decide to remove the dialog and include the pauses for snapping
# + if inter_display + if intra_display

# def record_step(track_name, message):
#     '''
#     function to track where you are in a process to exit and re-enter
#     :param track_name: string, name of the process, should be unique to make tracking file
#     :param message: string, message to print to console so user knows how to proceed
#     :return: none
#     '''
#
#     filename = track_name + '.txt'
#
#     if os.path.exists(os.path.join(path, filename)):
#         with open(filename, 'r') as f:
#             step = f.read()
#         with open(filename, 'w') as f:
#             print(step)
#             f.write(str(int(step) + 1))
#
#
#     else:
#         with open(filename, 'w') as f:
#             f.write('1')
#     #https://www.geeksforgeeks.org/python-exit-commands-quit-exit-sys-exit-and-os-_exit/
#     sys.exit(message)


#record_step('Proximal-Distal', 'Select cells for Proximal-Distal measure then run script again')

# practice with writing to master file
params_dict = {'gen_measures': False,
               'distance_measures': [],
               'inter_display': ['d_Area'],
               'intra_display': ['Geometry/Area'],
               'gen display':['blah'],
               'distance_measure_step':0,
               'intra_display_step':0,
               'inter_display_step':0}

# make sure read/write as proper data types
print params_dict['intra_display']

params_dict['intra_display'] = params_dict['intra_display'] +params_dict['gen display']
params_dict['gen display'] = []

print params_dict['intra_display']

import pprint
print pprint.pprint(params_dict)

print params_dict.has_key('non')

import json
import pprint

path = os.path.abspath(os.getcwd())

#
# def master_step_get(path, filename, params_dict):
#     '''
#     function to track where you are in a process to exit and re-enter
#     :param path: string path to data files, where step tracking file will be saved
#     :param filename: string, name of the file where the params dict will be tracked
#     :param params_dict: dict of params
#     :return: none
#     '''
#     step_file = os.path.join(path, filename)
#
#     if os.path.exists(step_file):
#         with open(step_file, 'r') as f:
#             params_dict = json.load(f)
#
#     else:
#         master_step_set(path, filename, params_dict)
#
#     return params_dict
#
#
# def master_step_set(path, filename, params_dict):
#     '''
#     function to track where you are in a process to exit and re-enter
#     :param path: string path to data files, where step tracking file will be saved
#     :param filename: string, name of the file where the params dict will be tracked
#     :param params_dict: dict of params
#     :return: none
#     '''
#     step_file = os.path.join(path, filename)
#
#     with open(step_file, 'w') as f:
#         json.dump(params_dict, f)
#
# pp = pprint.PrettyPrinter()
# pp.pprint(params_dict)
# params_dict = master_step_get(path, 'test.txt', params_dict)
# pp.pprint(params_dict)
# master_step_set(path, 'test.txt', params_dict)
# pp.pprint(params_dict)