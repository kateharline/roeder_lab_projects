######## New MorphoGraphX session v2.0 r1-63-ga635c756: 2020-08-27 18:16:00
import os
import logging
from Tkinter import *
import pprint
import sys

####### DIR MANAGEMENT ########

# https://docs.python.org/2/library/os.html
o_s = os.name
if o_s == 'posix':
    root_path = '/home/kate'
# elif os == '':

# hack add current dir to sys path so python can import personal modules https://stackoverflow.com/questions/338768/python-error-importerror-no-module-named
sys.path.insert(0,os.path.join(root_path, 'Desktop', 'roeder_lab_projects', 'mgx_scripts'))

import funcs as f

# todo add root for windows

# workaround to use tkinter https://github.com/googleapis/oauth2client/issues/642
if not hasattr(sys, 'argv'):
    sys.argv  = ['']

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


# make all missing folders to avoid throwing errors https://stackoverflow.com/questions/1274405/how-to-create-new-folder
require_folders = ['meshes', 'parents', 'attributes', 'snaps']

for i in range(1, len(require_folders)):
    if not os.path.exists(os.path.join(file_path, require_folders[i])):
        os.makedirs(os.path.join(file_path, require_folders[i]))



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

######### FUNCTIONS

def do_distance_measures(mesh, types):
    """
    allow user to input cell based axes for measures of distance within a mesh
    :param mesh: string denoting path to mesh to be used
    :param types: list of strings, which axes to measure
    :return: none
    """

    return

def do_intra_measures(mesh):
    """
    conduct all single mesh measures, then export attribute map to csv
    :param mesh:
    :return:
    """
    # load mesh
    Process.Mesh__System__Load(os.path.join(file_path, 'meshes', mesh), 'no', 'no', '0')
    Process.Stack__System__Set_Current_Stack('Main', '0')

    # run desired processes
    Process.Mesh__Heat_Map__Measures__Geometry__Area()
    Process.Mesh__Heat_Map__Measures__Geometry__Aspect_Ratio()
    Process.Mesh__Heat_Map__Measures__Geometry__Average_Radius()
                                                            # min or max, direct junctions (yes) or also neighbors (no)
    Process.Mesh__Heat_Map__Measures__Geometry__Junction_Distance('Min', 'No')
    # todo check that it will measure and save both as attributes
    Process.Mesh__Heat_Map__Measures__Geometry__Junction_Distance('Max', 'No')
    Process.Mesh__Heat_Map__Measures__Geometry__Length_Major_Axis()
    Process.Mesh__Heat_Map__Measures__Geometry__Length_Minor_Axis()
    Process.Mesh__Heat_Map__Measures__Geometry__Maximum_Radius()
    Process.Mesh__Heat_Map__Measures__Geometry__Minimum_Radius()
    Process.Mesh__Heat_Map__Measures__Geometry__Neighbors()
    Process.Mesh__Heat_Map__Measures__Geometry__Perimeter()
    Process.Mesh__Heat_Map__Measures__Lobeyness__Circularity()
    Process.Mesh__Heat_Map__Measures__Lobeyness__Largest_Empty_Space()
    Process.Mesh__Heat_Map__Measures__Lobeyness__Lobeyness()
    Process.Mesh__Heat_Map__Measures__Lobeyness__Rectangularity()
    Process.Mesh__Heat_Map__Measures__Lobeyness__Solidarity()
    Process.Mesh__Heat_Map__Measures__Lobeyness__Visibility_Pavement()
    Process.Mesh__Heat_Map__Measures__Lobeyness__Visibility_Stomata()
    Process.Mesh__Heat_Map__Measures__Neighborhood__Area()
    Process.Mesh__Heat_Map__Measures__Neighborhood__Aspect_Ratio()
    Process.Mesh__Heat_Map__Measures__Neighborhood__Neighbors()
    Process.Mesh__Heat_Map__Measures__Neighborhood__Perimeter()
    Process.Mesh__Heat_Map__Measures__Neighborhood__Variability_Radius()
    Process.Mesh__Heat_Map__Measures__Shape__Bending()
    Process.Mesh__Heat_Map__Measures__Shape__Common_Bending()
    Process.Mesh__Heat_Map__Measures__Shape__Common_Neighbors()
    Process.Mesh__Heat_Map__Measures__Shape__Variability_Radius()


    # save the mesh (attributes saved in mesh)
    #                           filename, transform, mesh number
    Process.Mesh__System__Save(mesh, 'no','0')


    return


def do_inter_measures(mesh_0, mesh_1):
    """
    run processes that track changes between meshes
    :param mesh_0: string, filepath of the first mesh (t)
    :param mesh_1: string, filepath of the second mesh (t+1)
    :return: null
    """
    # load meshes
    Process.Mesh__System__Load(os.path.join(file_path, 'meshes', mesh_0), 'no', 'no', '0')
    Process.Mesh__System__Load(os.path.join(file_path, 'meshes', mesh_1), 'no', 'no', '1')
    Process.Stack__System__Set_Current_Stack('Main', '0')

    # set parents active on the alternate mesh
    root = Tk()
    w = Label(root, text="Hello, world!")
    w.pack()

    root.mainloop()

    # run desired processes

    # save the mesh (attributes saved in mesh)
    #                           filename, transform, mesh number
    Process.Mesh__System__Save(mesh, 'no','0')
    Process.Mesh__System__Save(mesh, 'no', '1')

    return

def do_intra_display(mesh):
    """
    save snapshots for all desired measures
    :param mesh: string, filepath of the mesh
    :return: null
    """
    # load meshes
    Process.Mesh__System__Load(os.path.join(file_path, 'meshes', mesh), 'no', 'no', '0')
    Process.Stack__System__Set_Current_Stack('Main', '0')

    # user adjust arrangement


    # take photos

    return

def do_inter_display(mesh_0, mesh_1):
    # load meshes
    Process.Mesh__System__Load(os.path.join(file_path, 'meshes', mesh_0), 'no', 'no', '0')
    Process.Mesh__System__Load(os.path.join(file_path, 'meshes', mesh_1), 'no', 'no', '1')
    Process.Stack__System__Set_Current_Stack('Main', '0')

    # user adjust arrangement

    # take photos

    return

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

