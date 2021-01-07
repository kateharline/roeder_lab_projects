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

def record_step(track_name, message):
    '''
    function to track where you are in a process to exit and re-enter
    :param track_name: string, name of the process, should be unique to make tracking file
    :param message: string, message to print to console so user knows how to proceed
    :return: none
    '''

    filename = track_name + '.txt'

    if os.path.exists(os.path.join(path, filename)):
        with open(filename, 'r') as f:
            step = f.read()
        with open(filename, 'w') as f:
            print(step)
            f.write(str(int(step) + 1))


    else:
        with open(filename, 'w') as f:
            f.write('1')

    sys.exit(message)


record_step('Proximal-Distal', 'Select cells for Proximal-Distal measure then run script again')