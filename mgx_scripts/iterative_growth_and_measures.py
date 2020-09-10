######## New MorphoGraphX session v2.0 r1-63-ga635c756: 2020-08-27 18:16:00
import os
import logging
import Tkinter, tkFileDialog


# fun fun file management shit between dev env of vm build and windows build
data_files = '202003_0715_analysis'
data_files_path = os.path.join('Desktop', data_files)
# https://docs.python.org/2/library/os.html
o_s = os.name
if o_s == 'posix':
    root_path = '/home/kate'
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

print('file path '+ file_path)

# get list of files in dir https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
meshes = []


fs = os.walk(file_path)
print('what\'s going on with the os walk' +len(fs))
print('dirpath ' + dirpath)
print('dirnames ' + dirnames)
print('filenames ' + filenames)


# make dirs to save

for (dirpath, dirnames, filenames) in os.walk(path):
    meshes.extend(filenames)

    break


# https://stackoverflow.com/questions/1274405/how-to-create-new-folder

if not os.path.exists(os.path.join(path, 'parents')):
    os.makedirs(os.path.join(path, 'parents'))

if not os.path.exists(os.path.join(path, 'attributes')):
    os.makedirs(os.path.join(path, 'attributes'))


i = 0
# open mgx
# load stack 1, stack 2
                                #filename, transform, add, stack number (0 indexed)
Process.Mesh__System__Load(os.path.join(path, 'meshes', meshes[i]), 'no', 'no', '0')
Process.Mesh__System__Load(os.path.join(path, 'meshes', meshes[i+1]), 'no', 'no', '1')


# # todo check that parent file exists, if not save
#
# if not os.path.exists(os.join(path, 'parents', meshes[i+1])):
#     # set stack 1 as main                   store, stack id
#     Process.Stack__System__Set_Current_Stack('Main', '1')
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
