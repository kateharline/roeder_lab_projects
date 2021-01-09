######## New MorphoGraphX session v2.0 r1-63-ga635c756: 2020-08-27 18:16:00
import os
#from Tkinter import *
#import tkFileDialog
import pprint
import sys

####### DIR MANAGEMENT ########

# https://docs.python.org/2/library/os.html
o_s = os.name
if o_s == 'posix':
    root_path = '/home/kate'
elif o_s == 'nt':
    root_path = 'C:\\Users\\katha\\'

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
distance_measures = []
# distance_measures = ['Proximal-Distal', 'Medial-Lateral']
parents_as_csvs = False

# attributes to save
#save_attr = ['/Geometry/Area', '/Geometry/Aspect Ratio', '/Geometry/Average Radius', '/Geometry/Junction Distance', '/Geometry/Length Major Axis', '/Geometry/Length Minor Axis', '/Geometry/Maximum Radius', '/Geometry/Minimum Radius', '/Geometry/Perimeter', '/Lobeyness/Circularity', '/Lobeyness/Lobeyness', '/Lobeyness/Rectangularity', '/Lobeyness/Solidarity', '/Lobeyness/Visibility Pavement', '/Lobeyness/Visibility Stomata', '/Neighborhood/Area', '/Neighborhood/Aspect Ratio', '/Neighborhood/Neighbors', '/Neighborhood/Perimeter', '/Neighborhood/Variability Radius', '/Shape/Bending', '/Shape/Common Bending', '/Shape/Common Neighbors', '/Shape/Variability Radius', 'd_Area']
#save_attr = []
save_attr = 'Label Double d_Area, Label Double Geometry/Area'

# which measures to display and how
inter_display = ['d_Area']
#inter_display = []
inter_ranges = [[1,3]]
intra_display = ['Geometry/Area']
#intra_display = []
intra_ranges = [[0,1900]]


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

def load_mesh(mesh, stack, parents):
    '''
    utility function to load mesh into a standard view
    :param mesh: string, filename of mesh
    :param stack: int 0 or 1, which stack to load mesh into
    :param parents: str yes or no, display parents or cell labels
    :return:
    '''
    Process.Mesh__System__Load(os.path.join(main_path, 'meshes', mesh), 'no', 'no', stack)
    Process.Stack__System__Set_Current_Stack('Main', stack)
    Process.Mesh__System__View('', parents, 'Cells', '', 'Label', '', '', '', '', '', '', '', '', '', '', '-1', '-1')
    Process.Mesh__Cell_Axis__Cell_Axis_Clear()


def step_check(path, filename):
    '''
    function to track where you are in a process to exit and re-enter
    :param path: string path to data files, where step tracking file will be saved
    :param filename: string, name of the file where the step will be tracked
    :return: none
    '''
    step_file = os.path.join(path, filename)

    step = 0

    if os.path.exists(step_file):
        with open(step_file, 'r') as f:
            last_step = f.read()
            step = int(last_step) + 1
        with open(step_file, 'w') as f:
            f.write(str(step))


    else:
        with open(step_file, 'w') as f:
            f.write(str(step))

    return step



def do_distance_measures(meshes, types, path):
    """
    allow user to input cell based axes for measures of distance within a mesh
    :param meshes: list of strings denoting path to meshes to be used
    :param types: list of strings, which axes to measure
    :param path: string data files path where the status txt file should be saved
    :return: bool, there are measures left?
    """
    # old dialog method
    # user_dialog('Done setting axis?')

    # check files
    step = step_check(path, 'distance_steps.txt')
    meshes_path = os.path.join(path, 'meshes')

    total_steps = len(meshes)*len(types)
    # print ('meshes[step // len(types)] ' + meshes[step // len(types)])


    # branch - save location exit python, run cell distance and save heat then load new mesh or just load first mesh
    if step == 0:
        load_mesh(os.path.join(meshes_path, meshes[step]), 0, 'No')
        sys.exit('Select cells for '+ types[step % len(types)]+ ' axis then re-run script')

    else:
        # measure distance                                      wall weight, restrict connectivity
        Process.Mesh__Heat_Map__Measures__Location__Cell_Distance('Euclidean', 'No')
        # save as attributes
        Process.Mesh__Heat_Map__Operators__Export_Heat_to_Attr_Map('Measure Label Double', types[(step - 1) % len(types)] + '_Distance', 'Label',
                                                               'Label Heat', 'Active Mesh', 'No')
        # save the mesh (attributes saved in mesh)
        #                           filename, transform, mesh number
        Process.Mesh__System__Save(os.path.join(path, 'meshes', meshes[(step - 1) // len(types)]), 'no', '0')

        if step < total_steps:
            if not (step % len(types)):
                # load new mesh because done all measures
                load_mesh(os.path.join(meshes_path, meshes[(step + 1) // len(types)]), 0, 'No')

            sys.exit('Select cells for ' + types[step % len(types)] + ' axis then re-run script')
        else:
            os.remove(os.path.join(path, 'distance_steps.txt'))

    # when done doing steps, return empty types list so this function will be skipped over
    return types[:]



def do_parents_to_attr(parent_file, mesh):
    """
    function to add parents to attributes, esp for old data before parents were automatically saved to attributes file
    :param parent_file: stirng, path to parent csv file
    :param mesh: string, filename of mesh
    :return: null
    """
    # load mesh
    load_mesh(mesh, 0, 'Yes')

    #

    Process.Mesh__Lineage_Tracking__Load_Parents(os.path.join(main_path, 'parents', parent_file), 'CSV', 'No')
    Process.Mesh__Lineage_Tracking__Parent_Export_to_Attr_Map('Measure Label Int', 'Parents')
    Process.Mesh__System__Save(mesh, 'no', '0')


def do_intra_measures(mesh):
    """
    conduct all single mesh measures, then export attribute map to csv
    :param mesh: string, filepath of the mesh
    :return: null
    """
    # load mesh
    load_mesh(mesh, 0, 'No')
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

    # if there are parent csvs in the parents folder
    if dirs_dict['parents']:
        print('saving parents to attr')
        do_parents_to_attr(dirs_dict['parents'][i_0], mesh_1)

    # load meshes
    load_mesh(mesh_1, 1, 'Yes')
    load_mesh(mesh_0, 0, 'No')
    # todo "try" load parents with view, if not saved in attributes, then load from csv

    # run desired processes

    # Process.Mesh__Heat_Map__Analysis__Growth_Analysis_2D('pAR393xpLH13', 'd1', 'd2', 'No')
    Process.Mesh__Heat_Map__Heat_Map('Geometry/Area', 'No', 'Sum', 'Yes', 'Increasing', 'Ratio', 'Yes', 'No')
    Process.Mesh__Heat_Map__Operators__Export_Heat_to_Attr_Map('Measure Label Double', 'd_Area', 'Label', 'Label Heat', 'Active Mesh', 'No')
    Process.Mesh__Lineage_Tracking__Heat_Map_Proliferation('Yes')
    Process.Mesh__Heat_Map__Operators__Export_Heat_to_Attr_Map('Measure Label Double', 'd_Proliferation'+str(i_0+1)+ 'd'+str(i_0+2), 'Label',
                                                               'Label Heat', 'Active Mesh', 'No')

    Process.Stack__System__Set_Current_Stack('Main', '0')
    Process.Mesh__Cell_Axis__PDG__Check_Correspondence('No', 'No', 'No')
    Process.Mesh__Cell_Axis__Cell_Axis_Export_To_Attr_Map('Measure Label Tensor', 'Cell Axis PDG')
    Process.Stack__System__Set_Current_Stack('Main', '1')
    Process.Mesh__Cell_Axis__Cell_Axis_Export_To_Attr_Map('Measure Label Tensor', 'Cell Axis PDG')
    Process.Stack__System__Set_Current_Stack('Main', '0')
    Process.Mesh__Cell_Axis__PDG__Compute_Growth_Directions()

    # save the mesh (attributes saved in mesh)
    #                           filename, transform, mesh number
    Process.Mesh__System__Save(mesh_0, 'no','0')
    Process.Mesh__System__Save(mesh_1, 'no', '1')


def do_display(meshes, measures, ranges, attr_dict, path, is_inter, pdg=None):
    """
    save snapshots for all desired measures
    :param meshes: list of strings, paths to meshes
    :param measures: list of strings, names of measures to be displayed
    :param ranges: list of tuples, sets of ranges for each measure to be displayed
    :param attr_dict: string, path to attributes file
    :param path: string, path to top dir for saving
    :param pdg: list can pass for special pdg display values
    param: inter: bool displaying intermeasures or intra
    :return: null
    """

    # user adjust arrangement

    # old dialog strategy
    # user_dialog('Done arranging meshes, start a snappin?')

    # new strategy based on writing to file

    # check files
    step = step_check(path, 'display_steps.txt')
    meshes_path = os.path.join(path, 'meshes')

    total_steps = len(meshes) + 1

    if is_inter:
        total_steps = len(meshes)

    if step == 0:
        if is_inter:
            load_mesh(dirs_dict['meshes'][step+1], 1, 'Yes')

        load_mesh(dirs_dict['meshes'][step], 0, 'No')

        # todo set main mesh
        sys.exit('Arrange meshes as desired for image of' + measures[0] + 'then re-run script')

    else:

        for i in range(0,len(measures)):
            if measures[i] == 'Cell Axis PDG':
                Process.Mesh__Cell_Axis__Cell_Axis_Import_From_Attr_Map('PDG', 'Measure Label Tensor Cell Axis PDG')
                                                                 # heatmap, scaleheat, heat min, max, show axis, color +, color -
                Process.Mesh__Cell_Axis__PDG__Display_Growth_Directions('StretchMax', 'Auto', ranges[i][0], ranges[i][1], 'Both', 'white', 'red',
                                                     # line width, line scale, line offset, threshold, custon dir, min dist vtx
                                                                        '2.0', '2.0', '0.1', '0.0', 'No', '1.0')
                Process.Mesh__System__View('No', '', '', '', '', '', '', 'No', 'Border', '', '', '', '', '', '', '-1', '-1')
            else:
                #load heatmap
                #                                                                           filename, column name?, border size
                Process.Mesh__Heat_Map__Heat_Map_Load(
                    os.path.join(path, 'attributes', attr_dict['attributes'][(step -1) % 2]), measures[i], '1.0')
                Process.Mesh__Heat_Map__Heat_Map_Set_Range(ranges[i][0], ranges[i][1])
                # nice viz parameters
                Process.Mesh__System__View('Yes', 'No', 'Cells', '', 'Label Heat', '', '', '', 'Border', '', '', '', '', '',
                                           '', '-1', '-1')
            # take photos
            snap_path = os.path.join(path, 'snaps',
                                     attr_dict['attributes'][step -1][:-8] + "_".join(measures[i].split('/')) + '.png')
            Process.Misc__System__Snapshot(snap_path, 'false', '0', '0',
                                           '1.0', '95')

        if step < total_steps:

            # load new mesh because done all measures
            if is_inter:
                load_mesh(os.path.join(meshes_path, meshes[(step + 1) // 2]), 1, 'Yes')

            load_mesh(os.path.join(meshes_path, meshes[step  // 2]), 0, 'No')

            sys.exit('Arrange meshes as desired for image of ' + measures[i] + ' then re-run script')
        else:
            os.remove(os.path.join(path, 'display_steps.txt'))

    # when done doing steps, return empty types list so this function will be skipped over
    return measures[:]



####### FILES ##########
pp = pprint.PrettyPrinter()
print(main_path)
dirs_dict = walk(main_path)
parents_dict = walk(os.path.join(main_path, 'parents'))


############ EXECTUE MEASURES #################

if distance_measures:
    distance_measures = do_distance_measures(dirs_dict['meshes'], distance_measures, main_path)

# todo ? set distance_measures to empty list so this gets skipped once done

# for older meshes need to save parents to attr
# change measures
for i in range(0, len(dirs_dict['meshes'])-1):

    if parents_as_csvs:
        do_parents_to_attr(dirs_dict['meshes'][i + 1], parents_dict['parents'][i])

    if inter_measures:
        do_inter_measures(dirs_dict['meshes'][i],dirs_dict['meshes'][i+1], i)


# single mesh measures
for i in range(0, len(dirs_dict['meshes'])):

    if intra_measures:
        do_intra_measures(dirs_dict['meshes'][i])

    if save_attr:
        # load mesh only when it isn't already loaded
        if not intra_measures:
            load_mesh(dirs_dict['meshes'][i], 0, 'No')

        savepath = os.path.join(main_path, 'attributes', dirs_dict['meshes'][i][:-5] + '_attr.csv')
        Process.Mesh__Attributes__Save_to_CSV(savepath, save_attr)

# displaying meshes
attr_dict = walk(os.path.join(main_path, 'attributes'))


if intra_display:
    do_display(dirs_dict['meshes'], intra_display, intra_ranges, attr_dict, main_path, False)

if inter_display:
    do_display(dirs_dict['meshes'], inter_display, inter_ranges, attr_dict, main_path, True)
