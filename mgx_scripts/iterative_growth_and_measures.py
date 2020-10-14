######## New MorphoGraphX session v2.0 r1-63-ga635c756: 2020-08-27 18:16:00
import os
from Tkinter import *
import tkFileDialog
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

# import funcs as f

# todo add root for windows

# workaround to use tkinter https://github.com/googleapis/oauth2client/issues/642
if not hasattr(sys, 'argv'):
    sys.argv  = ['']

######### USER INPUT ##########

# variables for control flow
file_selector = False
inter_measures = False
intra_measures = False
# distance_measures = []
distance_measures = ['Proximal-Distal', 'Medial-Lateral']
parents_as_csvs = False

# attributes to save
save_attr = ['/Geometry/Area', '/Geometry/Aspect Ratio', '/Geometry/Average Radius', '/Geometry/Junction Distance', '/Geometry/Length Major Axis', '/Geometry/Length Minor Axis', '/Geometry/Maximum Radius', '/Geometry/Minimum Radius', '/Geometry/Perimeter', '/Lobeyness/Circularity', '/Lobeyness/Lobeyness', '/Lobeyness/Rectangularity', '/Lobeyness/Solidarity', '/Lobeyness/Visibility Pavement', '/Lobeyness/Visibility Stomata', '/Neighborhood/Area', '/Neighborhood/Aspect Ratio', '/Neighborhood/Neighbors', '/Neighborhood/Perimeter', '/Neighborhood/Variability Radius', '/Shape/Bending', '/Shape/Common Bending', '/Shape/Common Neighbors', '/Shape/Variability Radius', 'd_Area']

# which measures to display and how
inter_display = {'heats':[],'pdg':False}
intra_display = []
intra_ranges = []
inter_ranges = []

# fun fun file management shit between dev env of vm build and windows build
data_files = '202003_0715_demo'
data_files_path = os.path.join('Desktop', data_files)

if file_selector:
    # allow user dialogue to pick path when ready https://stackoverflow.com/questions/9319317/quick-and-easy-file-dialog-in-python
    w = Tk()

    # root.filename = tkFileDialog.askdirectory(initialdir = root_path,title = "Select experiment directory")
    # print (root.filename)
    # main_path = root.filename
    filename = tkFileDialog.askdirectory(title="Select experiment directory")
    w.destroy()
    main_path = filename
    print (main_path)
    # root.mainloop()
else:
    # main directory
    main_path = os.path.join(root_path, data_files_path)


# make all missing folders to avoid throwing errors https://stackoverflow.com/questions/1274405/how-to-create-new-folder
require_folders = ['meshes', 'parents', 'attributes', 'snaps']

for i in range(1, len(require_folders)):
    if not os.path.exists(os.path.join(main_path, require_folders[i])):
        os.makedirs(os.path.join(main_path, require_folders[i]))

######### FUNCTIONS  #########
def walk(file_path):
    '''
    # get list of files in dir https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
    :param file_path: string
    :return: dictionary of key:folders (string) and values:contents (list of strings)
    '''

    dirs_dict = {}

    for (dirpath, dirnames, filenames) in os.walk(file_path):
        # meshes.extend(filenames)
        dot_dir = dirpath.split(os.sep)[-1]
        # clean up dirs list so that meshes are in date order and only load those types of files
        # https://docs.python.org/2/howto/sorting.html
        filenames.sort()

        if 'MorphoGraphX.py' in filenames:
            filenames.remove('MorphoGraphX.py')
        ##### option to define additional file selection rules


        dirs_dict[dot_dir] = filenames
    return dirs_dict

def user_dialog(message):
    # https://docstore.mik.ua/orelly/other/python2/1.7.htm
    root = Tk()
    Label(root, text=message).pack()
    Button(root, text='Yes', command=root.destroy).pack()
    root.focus_set()
    root.wait_window()
    root.mainloop()


def do_distance_measures(mesh, types):
    """
    allow user to input cell based axes for measures of distance within a mesh
    :param mesh: string denoting path to mesh to be used
    :param types: list of strings, which axes to measure
    :return: none
    """
    # load mesh
    Process.Mesh__System__Load(os.path.join(main_path, 'meshes', mesh), 'no', 'no', '0')
    Process.Stack__System__Set_Current_Stack('Main', '0')

    for i in range(0,len(types)):
        # user define cells
        user_dialog('Done setting axis?')

        # measure distance                                      wall weight, restrict connectivity
        Process.Mesh__Heat_Map__Measures__Location__Cell_Distance('Euclidean', 'No')
        # save as attributes

        Process.Mesh__Heat_Map__Operators__Export_Heat_to_Attr_Map('Measure Label Double', types[i] + '_Distance', 'Label',
                                                               'Label Heat', 'Active Mesh', 'No')

    # save the mesh (attributes saved in mesh)
    #                           filename, transform, mesh number
    Process.Mesh__System__Save(mesh, 'no', '0')


def do_parents_to_attr(parent_file, mesh):
    """
    function to add parents to attributes, esp for old data before parents were automatically saved to attributes file
    :param parent_file: stirng, path to parent csv file
    :param mesh: string, filename of mesh
    :return: null
    """
    # load mesh
    Process.Mesh__System__Load(os.path.join(main_path, 'meshes', mesh), 'no', 'no', '0')
    Process.Stack__System__Set_Current_Stack('Main', '0')
    #
    Process.Mesh__Lineage_Tracking__Load_Parents(parent_file, 'CSV', 'No')
    Process.Mesh__Lineage_Tracking__Parent_Export_to_Attr_Map('Measure Label Int', 'Parents')
    Process.Mesh__System__Save(mesh, 'no', '0')


def do_intra_measures(mesh):
    """
    conduct all single mesh measures, then export attribute map to csv
    :param mesh: string, filepath of the mesh
    :return: null
    """
    # load mesh
    Process.Mesh__System__Load(os.path.join(main_path, 'meshes', mesh), 'no', 'no', '0')
    Process.Stack__System__Set_Current_Stack('Main', '0')
    Process.Mesh__System__View('', 'No', 'Cells', '', 'Label', '', '', '', '', '', '', '', '', '', '', '-1', '-1')

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

    Process.Mesh__Heat_Map__Measures__Geometry__Perimeter()
    Process.Mesh__Heat_Map__Measures__Lobeyness__Circularity()
    Process.Mesh__Heat_Map__Measures__Lobeyness__Lobeyness()
    Process.Mesh__Heat_Map__Measures__Lobeyness__Rectangularity()
    Process.Mesh__Heat_Map__Measures__Lobeyness__Solidarity()
    Process.Mesh__Heat_Map__Measures__Lobeyness__Visibility_Pavement()
    Process.Mesh__Heat_Map__Measures__Lobeyness__Visibility_Stomata()
    Process.Mesh__Heat_Map__Measures__Neighborhood__Area()
    Process.Mesh__Heat_Map__Measures__Neighborhood__Aspect_Ratio()
    Process.Mesh__Heat_Map__Measures__Neighborhood__Perimeter()
    Process.Mesh__Heat_Map__Measures__Neighborhood__Variability_Radius()
    Process.Mesh__Heat_Map__Measures__Neighborhood__Neighbors()
    Process.Mesh__Heat_Map__Measures__Shape__Bending()
    Process.Mesh__Heat_Map__Measures__Shape__Common_Bending()
    Process.Mesh__Heat_Map__Measures__Shape__Common_Neighbors()
    Process.Mesh__Heat_Map__Measures__Shape__Variability_Radius()


    # save the mesh (attributes saved in mesh)
    #                           filename, transform, mesh number
    pp.pprint('is saving working '+mesh)
    Process.Mesh__System__Save(mesh, 'no','0')



def do_inter_measures(mesh_0, mesh_1, i_0):
    """
    run processes that track changes between meshes
    :param mesh_0: string, filepath of the first mesh (t)
    :param mesh_1: string, filepath of the second mesh (t+1)
    :return: null
    """
    # load meshes

    Process.Mesh__System__Load(os.path.join(main_path, 'meshes', mesh_1), 'no', 'no', '1')
    Process.Mesh__System__Load(os.path.join(main_path, 'meshes', mesh_0), 'no', 'no', '0')
    # mesh 0 show cell labels, mesh 1 show parent labels
    Process.Stack__System__Set_Current_Stack('Main', '0')
    Process.Mesh__System__View('', 'No', 'Cells', '', 'Label', '', '', '', '', '', '', '', '', '', '', '-1', '-1')
    Process.Stack__System__Set_Current_Stack('Main', '1')
    Process.Mesh__System__View('', 'Yes', 'Cells', '', 'Label', '', '', '', '', '', '', '', '', '', '', '-1', '-1')

    # todo "try" load parents with view, if not saved in attributes, then load from csv

    # if there are parent csvs in the parents folder
    if dirs_dict['parents']:
        print('saving parents to attr')
        do_parents_to_attr(dirs_dict['parents'][i_0], mesh_1)
    # run desired processes

    # Process.Mesh__Heat_Map__Analysis__Growth_Analysis_2D('pAR393xpLH13', 'd1', 'd2', 'No')
    Process.Mesh__Heat_Map__Heat_Map('/Geometry/Area', 'No', 'Sum', 'Yes', 'Decreasing', 'Ratio', 'No', 'Yes')
    Process.Mesh__Heat_Map__Operators__Export_Heat_to_Attr_Map('Measure Label Double', 'd_Area', 'Label', 'Label Heat', 'Active Mesh', 'No')
    Process.Mesh__Lineage_Tracking__Heat_Map_Proliferation('No')
    Process.Mesh__Heat_Map__Operators__Export_Heat_to_Attr_Map('Measure Label Double', 'Proliferationd'+str(i_0+1)+ 'd'+str(i_0+2), 'Label',
                                                               'Label Heat', 'Active Mesh', 'No')

    Process.Stack__System__Set_Current_Stack('Main', '0')
    Process.Mesh__Cell_Axis__PDG__Check_Correspondence('No', 'No', 'No')
    Process.Mesh__Cell_Axis__Cell_Axis_Export_To_Attr_Map('Measure Label Tensor', 'Cell Axis PDG')
    Process.Stack__System__Set_Current_Stack('Main', '1')
    Process.Mesh__Cell_Axis__Cell_Axis_Export_To_Attr_Map('Measure Label Tensor', 'Cell Axis PDG')
    Process.Mesh__Cell_Axis__PDG__Compute_Growth_Directions()

    # save the mesh (attributes saved in mesh)
    #                           filename, transform, mesh number
    Process.Mesh__System__Save(mesh_0, 'no','0')
    Process.Mesh__System__Save(mesh_1, 'no', '1')


def do_display(mesh, measures, ranges, attr_dict, main_path):
    """
    save snapshots for all desired measures
    :param mesh: string, filepath of the mesh
    :param measures: list of strings, names of measures to be displayed
    :param ranges: list of tuples, sets of ranges for each measure to be displayed
    :param attr_dict:
    :return: null
    """
    # load meshes
    Process.Mesh__System__Load(os.path.join(main_path, 'meshes', mesh), 'no', 'no', '0')
    Process.Stack__System__Set_Current_Stack('Main', '0')

    # user adjust arrangement
    user_dialog('Done arranging meshes, start a snappin?')


    for i in range(0,len(measures)):
        #load heatmap
        # todo check with new code from Richard
        #                                                                           filename, column name?, border size
        Process.Mesh__Heat_Map__Heat_Map_Load(
            attr_dict['attributes'][i], measures[i], '1.0')
        Process.Mesh__Heat_Map__Heat_Map_Set_Range(ranges[i][0], ranges[i][1])
        # take photos
        Process.Misc__System__Snapshot(os.path.join(main_path, 'snaps', attr_dict['attributes'][i], " ".join(measures[i].split())), 'false', '0', '0',
                                       '1.0', '95')

        # if PDG
        # Process.Mesh__Cell_Axis__Cell_Axis_Import_From_Attr_Map('PDG', 'Measure Label Tensor /Cell Axis PDG')
                                                         # heatmap, scaleheat, heat min, max, show axis, color +, color -
        # Process.Mesh__Cell_Axis__PDG__Display_Growth_Directions('StretchMax', 'Auto', '1', '3', 'Both', 'white', 'red',
                                             # line width, line scale, line offset, threshold, custon dir, min dist vtx
        #                                                         '2.0', '2.0', '0.1', '0.0', 'No', '1.0')
        # Process.Mesh__System__View('No', '', '', '', '', '', '', 'No', 'Border', '', '', '', '', '', '', '-1', '-1')

####### FILES ##########
pp = pprint.PrettyPrinter()
dirs_dict = walk(main_path)
pp.pprint(dirs_dict)
attr_dict = walk(os.path.join(main_path, 'attributes'))
pp.pprint(attr_dict)

############ EXECTUE MEASURES #################

# single mesh measures
for i in range(0,len(dirs_dict['meshes'])):
    if distance_measures:
        do_distance_measures(dirs_dict['meshes'][i], distance_measures)

    if intra_measures:
        do_intra_measures(dirs_dict['meshes'][i])

        savepath = os.path.join(main_path, 'attributes', dirs_dict['meshes'][i][:-5] + '_attr.csv')

        pprint.pprint(savepath)
        Process.Mesh__Attributes__Save_to_CSV(savepath, save_attr)

    if intra_display:
        attr_dict = walk(os.path.join(main_path, 'attributes'))
        do_display(dirs_dict['meshes'][i], intra_ranges, intra_ranges, attr_dict, main_path)

# for older meshes need to save parents to attr
if parents_as_csvs:
    parents_dict = walk(os.path.join(main_path, 'parents'))
    pp.pprint(parents_dict)
    for i in range(0, len(dirs_dict['meshes'])-1):
        do_parents_to_attr(dirs_dict['meshes'][i+1], parents_dict['parents'][i])

# change measures
for i in range(0, len(dirs_dict['meshes'])-1):

    if inter_measures:
        do_inter_measures(dirs_dict['meshes'][i],dirs_dict['meshes'][i+1], i)

        savepath = os.path.join(main_path, 'attributes', dirs_dict['meshes'][i][:-5] + '_attr')

        pprint.pprint(savepath)
        Process.Mesh__Attributes__Save_to_CSV(savepath, save_attr)

    if inter_display['heats']:
        attr_dict = walk(os.path.join(main_path, 'attributes'))
        do_display(dirs_dict['meshes'][i+1], inter_display, inter_ranges, attr_dict, main_path)
