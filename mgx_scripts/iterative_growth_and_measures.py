######## New MorphoGraphX session v2.0 r1-63-ga635c756: 2020-08-27 18:16:00
import os
import logging
from Tkinter import *
import pprint
import sys
#import funcs

####### DIR MANAGEMENT ########

# https://docs.python.org/2/library/os.html
o_s = os.name
if o_s == 'posix':
    root_path = '/home/kate'
# elif os == '':

# todo add root for windows

# workaround to use tkinter https://github.com/googleapis/oauth2client/issues/642
if not hasattr(sys, 'argv'):
    sys.argv  = ['']


# make all missing folders to avoid throwing errors https://stackoverflow.com/questions/1274405/how-to-create-new-folder
require_folders = ['meshes', 'parents', 'attributes', 'snaps']

for i in range(1, len(require_folders)):
    if not os.path.exists(os.path.join(file_path, require_folders[i])):
        os.makedirs(os.path.join(file_path, require_folders[i]))

######### USER INPUT ##########

# variables for control flow
deployed = False
inter_measures = True
intra_measures = True
distance_measures = False
inter_display = False
intra_display = False


# fun fun file management shit between dev env of vm build and windows build
data_files = '202003_0715_analysis'
data_files_path = os.path.join('Desktop', data_files)

if deployed:
    # allow user dialogue to pick path when ready https://stackoverflow.com/questions/9319317/quick-and-easy-file-dialog-in-python
    root = Tkinter.Tk()
    root.withdraw()
    file_path = tkFileDialog.askopenfilename()
else:
    # main directory
    file_path = os.path.join(root_path, data_files_path)

####### FILES ##########

# get list of files in dir https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
dirs_lib = {}

for (dirpath, dirnames, filenames) in os.walk(file_path):
    # meshes.extend(filenames)
    dot_dir = dirpath.split(os.sep)[-1]
    # clean up dirs list so that meshes are in date order and only load those types of files
    # https://docs.python.org/2/howto/sorting.html
    filenames.sort()

    if 'MorphoGraphX.py' in filenames:
        filenames.remove('MorphoGraphX.py')
    ##### option to define additional file selection rules


    dirs_lib[dot_dir] = filenames

############ MEASURES #################

# measures single mesh
for i in range(0,len(dirs_lib['meshes'])):

    if intra_measures:
        do_intra_measures(dirs_lib['meshes'][i])

    if intra_display:
        do_intra_display(dirs_lib['meshes'][i])


    savepath = os.path.join(file_path, 'attributes', dirs_lib['meshes'][i][:-5] + '_attr')

    pprint.pprint(savepath)
    Process.Mesh__Attributes__Save_to_CSV(savepath)

# lineage tracing measures
for i in range(0, len(dirs_lib['meshes'])-1):

    if inter_measures:
        do_inter_measures(dirs_lib['meshes'][i],dirs_lib['meshes'][i+1])

    if inter_display:
        do_inter_display(dirs_lib['meshes'][i],dirs_lib['meshes'][i+1])

    savepath = os.path.join(file_path, 'attributes', dirs_lib['meshes'][i][:-5] + '_attr')

    pprint.pprint(savepath)
    Process.Mesh__Attributes__Save_to_CSV(savepath)

# todo maybe add a wait in so that user can arrange the

# # todo check that parent file exists, if not save

# # todo check if there is a special axis to load, then load if so
# # todo for each heat map
#

# # todo set the parents to active, then stack 0

