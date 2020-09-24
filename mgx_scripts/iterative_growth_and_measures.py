######## New MorphoGraphX session v2.0 r1-63-ga635c756: 2020-08-27 18:16:00
import os
import logging
import Tkinter, tkFileDialog
import pprint

# fun fun file management shit between dev env of vm build and windows build
data_files = '202003_0715_analysis'
data_files_path = os.path.join('Desktop', data_files)
# https://docs.python.org/2/library/os.html
o_s = os.name
if o_s == 'posix':
    root_path = '/home/kate'
# elif os == '':

# todo add root for windows



deployed = False

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


pprint.pprint(dirs_lib)




i = 0
# open mgx
# load stack 1, stack 2
                                #filename, transform, add, stack number (0 indexed)
Process.Mesh__System__Load(os.path.join(file_path, 'meshes', dirs_lib['meshes'][i]), 'no', 'no', '0')
Process.Mesh__System__Load(os.path.join(file_path, 'meshes', dirs_lib['meshes'][i+1]), 'no', 'no', '1')

#     # set stack 1 as main                   store, stack id
Process.Stack__System__Set_Current_Stack('Main', '0')
Process.Mesh__Heat_Map__Measures__Geometry__Area()
# Process.Mesh__Attributes__Manage_Attributes('0')
# Process.Mesh__Attributes__Save_to_CSV(os.path.join(file_path, 'attributes', dirs_lib['meshes'][i], 'attr.csv'), 'no', 'no', '0')
# Process.Mesh__Attributes__Manage_Attributes('0')
# Process.Mesh__Heat_Map__Heat_Map_Load(os.path.join(file_path, 'attributes', dirs_lib['meshes'][i], 'attr.csv'), '1', '1.0')
# todo maybe add a wait in so that user can arrange the

# # todo check that parent file exists, if not save
#
# if not os.path.exists(os.join(path, 'parents', meshes[i+1])):

#     # maybe do a safety parent save first
#     #                                           filename, save only existing labels
#     Process.Mesh__Lineage_Tracking__Save_Parents(os.path.join(path, 'parents', meshes[i+1]), 'Yes')
#     # save to attr map                          prefix?, attr name
#     Process.Mesh__Lineage_Tracking__Parent_Export_to_Attr_Map('', 'Yes')
#
# #                                           filename, filetype, keep existing parents?
# Process.Mesh__Lineage_Tracking__Load_Parents(os.path.join(path, 'parents', meshes[i]), 'CSV', 'No')
# # set stack 1 as main                   store, stack id
# Process.Stack__System__Set_Current_Stack('Main', '0')
#
#
# # load special axis heat
# # todo check if there is a special axis to load, then load if so
# # todo for each heat map
#
# # if axis                             filename, column, border size (wall colormaps)
# Process.Mesh__Heat_Map__Heat_Map_Load('', '2', '1.0')
#
# # if no axis
# # can you open a dialoque
# # "ok I have marked the axis"
# # run heatmap
# # expore to attr map
# # Process.Mesh__Heat_Map__Operators__Export_Heat_to_Attr_Map('Measure Label Double', 'test', 'Label', 'Label Heat', 'Active Mesh', 'No')
#
#
# # run all measures, <<based on special axis>>
# #                                           exclude slow processes
# Process.Mesh__Heat_Map__Analysis__Cell_Analysis_2D('No')
# #                                      filename
# Process.Mesh__Attributes__Save_to_CSV('')
#
# # 'click' parents in stack 2
# # Process.Mesh__Lineage_Tracking__Parent_Import_from_Attr_Map('Measure Label Int', 'Parents')
#
# # todo set the parents to active, then stack 0
# # run growth pipeline
# Process.Mesh__Heat_Map__Analysis__Growth_Analysis_2D('', 'T2', 'T3', 'Yes')
#
# # export attribute map <<based on on axis>>
# Process.Mesh__Heat_Map__Operators__Export_Heat_to_Attr_Map('Measure Label Double', 'test', 'Label', 'Label Heat', 'Active Mesh', 'No')
# Process.Mesh__Attributes__Save_to_CSV('')
#
# # photos of heatmaps
# Process.Mesh__Heat_Map__Heat_Map_Load('', '2', '1.0')
# Process.Misc__System__Snapshot('snap_test', 'false', '0', '0', '1.0', '95')
#
#
#
#
# Process.Stack__System__Set_Current_Stack('Main', '2')
# Process.Stack__System__Set_Current_Stack('Main', '1')
#
# Process.Mesh__Heat_Map__Heat_Map_Save('')
#
# Process.Misc__System__Snapshot('', 'false', '0', '0', '1.0', '95')
# Process.Misc__System__Snapshot('snap_test', 'false', '0', '0', '1.0', '95')
#
#
#
#
#
