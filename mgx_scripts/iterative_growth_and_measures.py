######## New MorphoGraphX session v2.0 r1-63-ga635c756: 2020-08-27 18:16:00
import os
#from Tkinter import *
#import tkFileDialog
import pprint
import sys
import json
import platform

####### DIR MANAGEMENT ########

# https://docs.python.org/2/library/os.html
o_s = os.name
if o_s == 'posix':
	# if vmware
    root_path = '/home/kateharline/Desktop/finals'

    if platform.release() in ['4.15.0-118-generic', '4.15.0-20-generic']:
        # mgx1
	    root_path = '/home/aroeder/Desktop/Kate'
    if platform.release() in ['5.13.0-28-generic', '5.13.0-30-generic']:
        # mgx3
	    root_path = '/home/kh694/Desktop/Kate/finals'

elif o_s == 'nt':
    root_path = 'C:\\Users\\katha\\Desktop'

# hack add current dir to sys path so python can import personal modules https://stackoverflow.com/questions/338768/python-error-importerror-no-module-named
# sys.path.insert(0,os.path.join(root_path, 'Desktop', 'roeder_lab_projects', 'mgx_scripts'))

# import funcs as f

# todo add root for windows

# workaround to use tkinter https://github.com/googleapis/oauth2client/issues/642
if not hasattr(sys, 'argv'):
    sys.argv  = ['']

######### USER INPUT ##########

# variables for control flow
file_selector = False


# fun fun file management between dev env of vm build and windows build
data_files_path = 'jawD_2-7'

# attributes to save
#save_attr = ['/Geometry/Area', '/Geometry/Aspect Ratio', '/Geometry/Average Radius', '/Geometry/Junction Distance', '/Geometry/Length Major Axis', '/Geometry/Length Minor Axis', '/Geometry/Maximum Radius', '/Geometry/Minimum Radius', '/Geometry/Perimeter', '/Lobeyness/Circularity', '/Lobeyness/Lobeyness', '/Lobeyness/Rectangularity', '/Lobeyness/Solidarity', '/Lobeyness/Visibility Pavement', '/Lobeyness/Visibility Stomata', '/Neighborhood/Area', '/Neighborhood/Aspect Ratio', '/Neighborhood/Neighbors', '/Neighborhood/Perimeter', '/Neighborhood/Variability Radius', '/Shape/Bending', '/Shape/Common Bending', '/Shape/Common Neighbors', '/Shape/Variability Radius', 'd_Area']
#save_attr = 'Label Double d_Area, Label Double Geometry/Area'
# if distance measures 'Medial-Lateral','Proximal-Distal','Proximal-Distal_sp'

# which measures to display and how

params_dict = {'gen_measures': False,
               'inter_measures':False,
               'intra_measures':False,
               #'distance_measures': ['Proximal-Distal', 'Proximal-Distal_lamina', 'Medial-Lateral'],
               #'distance_measures': ['Margin'],
               'distance_measures':[],
               # probably for 2021 Label Double Medial-Lateral_Distance_Distance, Proximal-Distal_Distance_Distance, Proximal-Distal_Distance_sp_Distance
               'save_attr':'Label Double d_Area, Label Double d_Proliferation, Label Double Geometry/Area, Label Double Geometry/Aspect Ratio, Label Double Geometry/Average Radius, Label Double Geometry/Junction Distance, Label Double Geometry/Length Major Axis, Label Double Geometry/Length Minor Axis, Label Double Geometry/Maximum Radius, Label Double Geometry/Minimum Radius, Label Double Geometry/Perimeter, Label Double Geometry/Circularity, Label Double Lobeyness/Circularity, Label Double Lobeyness/Lobeyness, Label Double Lobeyness/Solidarity, Label Double Lobeyness/Visibility Pavement, Label Double Lobeyness/Visibility Stomata, Label Double Location/Cell Distance, Label Double Medial-Lateral_Distance, Label Double Neighborhood/Area, Label Double Neighborhood/Aspect Ratio, Label Double Neighborhood/Neighbors, Label Double Neighborhood/Perimeter, Label Double Neighborhood/Variability Radius, Label Double Network/Neighbors, Label Double Proximal-Distal_Distance, Label Double Margin_Distance, Label Double Proximal-Distal_lamina_Distance, Label Double Shape/Bending, Label Double Shape/Common Bending, Label Double Shape/Variability Radius, Label Tensor PDGs, Label Double aniso_angle_max, Label Tensor Curvature, Label Double Stomata_Distance',
               #'save_attr':'',
               #'inter_display': ['d_Area', 'd_Proliferation', 'PDGs', 'PD-PDG_align'],
               'inter_display': [],
               'inter_ranges':[['1','3'],['1','3']],
               'intra_display': [],
               'intra_ranges':[],
               #'gen_display':['mesh_signal', 'mesh_border', 'mesh_cells'],
               'gen_display':[],
               'distance_measure_step':0,
               'intra_display_step':0,
               'inter_display_step':0,
               'radii':['66.988', '166.821', '289.932', '462.853', '672.005', '922.935', '972.600'],
               #'custom_axis_spec':['Proximal-Distal_Distance', 'max'],
               'custom_axis_spec':[]
}

#hack add to end
params_dict['intra_display'] = params_dict['intra_display'] +params_dict['gen_display']
params_dict['gen_display'] = []


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
    Process.Mesh__System__View('Yes', parents, 'Cells', '', 'Wall Heat', '', '', 'Yes', 'Cells', '', '', '', '', '', '', '-1', '-1')
    Process.Mesh__Selection__Select_All()
    Process.Mesh__Selection__Invert_Selection()
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

def get_params(path, filename, params_dict):
    '''
    function to track where you are in a process to exit and re-enter
    :param path: string path to data files, where step tracking file will be saved
    :param filename: string, name of the file where the params dict will be tracked
    :param params_dict: dict of params
    :return: none
    '''
    step_file = os.path.join(path, filename)

    if os.path.exists(step_file):
        with open(step_file, 'r') as f:
            params_dict = json.load(f)

    else:
        set_params(path, filename, params_dict)

    return params_dict


def set_params(path, filename, params_dict):
    '''
    function to track where you are in a process to exit and re-enter
    :param path: string path to data files, where step tracking file will be saved
    :param filename: string, name of the file where the params dict will be tracked
    :param params_dict: dict of params
    :return: none
    '''
    step_file = os.path.join(path, filename)

    with open(step_file, 'w') as f:
        json.dump(params_dict, f)



def do_distance_measures(meshes, types, path, step):
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
        Process.Mesh__Heat_Map__Operators__Export_Heat_to_Attr_Map('Measure Label Double', types[(step - 1) % len(types)] + '_Distance', 'Label', 'Label Heat', 'Active Mesh', 'No')
        
        # save the mesh (attributes saved in mesh)
        #                           filename, transform, mesh number
        Process.Mesh__System__Save(os.path.join(path, 'meshes', meshes[(step - 1) // len(types)]), 'no', '0')

        if step < total_steps:
            if not (step % len(types)):
                # load new mesh because done all measures
                load_mesh(os.path.join(meshes_path, meshes[(step ) // len(types)]), 0, 'No')

            sys.exit('Select cells for ' + types[step % len(types)] + ' axis then re-run script')

    # when done doing steps, return empty types list so this function will be skipped over
    return []

def do_gen_measures(meshes, parents, main_path, intra_measures, inter_measures, radii):


    for i in range(0, len(meshes)):
        # load mesh
        load_mesh(meshes[i], 0, 'no')

        if intra_measures:
            do_intra_measures(meshes[i], radius=radii[i])

        if i < len(meshes) - 1:
            if inter_measures:
                load_mesh(meshes[i+1], 1, 'Yes')
                do_inter_measures(meshes[i], meshes[i + 1], i)

    return False

def do_save_attr(meshes, main_path, save_attr):
    '''

    :param meshes: list of mesh filenames
    :param main_path: string save path
    :param save_attr: string of attribute names to save
    :return:
    '''
    for i in range(0, len(meshes)):
        # load mesh
        load_mesh(meshes[i], 0, 'no')
        savepath = os.path.join(main_path, 'attributes', meshes[i][:-5] + '_attr.csv')
        Process.Mesh__Attributes__Save_to_CSV(savepath, save_attr)
        # Process.Mesh__Attributes__Save_to_CSV_Extended(savepath, 'Empty', '', '', '', '')

    return ''

def do_parents_to_attr(parent_file, mesh):
    """
    function to add parents to attributes, esp for old data before parents were automatically saved to attributes file
    :param parent_file: stirng, path to parent csv file
    :param mesh: string, filename of mesh
    :return: null
    """
    #

    Process.Mesh__Lineage_Tracking__Load_Parents(os.path.join(main_path, 'parents', parent_file), 'CSV', 'No')
    Process.Mesh__Lineage_Tracking__Parent_Export_to_Attr_Map('Measure Label Int', 'Parents')
    Process.Mesh__System__Save(mesh, 'no', '1')


def do_intra_measures(mesh, radius, path=main_path):
    """
    conduct all single mesh measures, then export attribute map to csv
    :param mesh: string, filepath of the mesh
    :return: null
    """

    # run desired processes
    Process.Mesh__Heat_Map__Measures__Geometry__Area()
    Process.Mesh__Heat_Map__Measures__Geometry__Aspect_Ratio()
    Process.Mesh__Heat_Map__Measures__Geometry__Average_Radius()
                                                            # min or max, direct junctions (yes) or also neighbors (no)
    Process.Mesh__Heat_Map__Measures__Geometry__Junction_Distance('Min', 'No', 'Yes')
    # todo check that it will measure and save both as attributes
    Process.Mesh__Heat_Map__Measures__Geometry__Junction_Distance('Max', 'No', 'Yes')
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


    Process.Mesh__Heat_Map__Measures__Network__Neighbors()


    Process.Mesh__Heat_Map__ToBeDeleted__Measures__Neighborhood__Aspect_Ratio()
    Process.Mesh__Heat_Map__ToBeDeleted__Measures__Neighborhood__Area()
    Process.Mesh__Heat_Map__ToBeDeleted__Measures__Neighborhood__Perimeter()
    Process.Mesh__Heat_Map__ToBeDeleted__Measures__Neighborhood__Variability_Radius()
    Process.Mesh__Heat_Map__ToBeDeleted__Measures__Neighborhood__Neighbors()
    Process.Mesh__Heat_Map__ToBeDeleted__Measures__Shape__Bending()
    Process.Mesh__Heat_Map__ToBeDeleted__Measures__Shape__Common_Bending()
    Process.Mesh__Heat_Map__ToBeDeleted__Measures__Shape__Common_Neighbors()
    Process.Mesh__Heat_Map__ToBeDeleted__Measures__Shape__Variability_Radius()
    Process.Mesh__Heat_Map__ToBeDeleted__Measures__Shape__Stomata_Area()

    Process.Mesh__Cell_Axis__Curvature__Compute_Tissue_Curvature(radius, 'No')
    # save the mesh (attributes saved in mesh)
    #                           filename, transform, mesh number
    Process.Mesh__System__Save(os.path.join(path, 'meshes', mesh), 'no','0')



def do_inter_measures(mesh_0, mesh_1, i_0, path=main_path):
    """
    run processes that track changes between meshes
    :param mesh_0: string, filepath of the first mesh (t)
    :param mesh_1: string, filepath of the second mesh (t+1)
    :return: null
    """

    # if there are parent csvs in the parents folder
    if dirs_dict['parents']:
        do_parents_to_attr(dirs_dict['parents'][i_0], mesh_1)

    # run desired processes
    Process.Stack__System__Set_Current_Stack('Main', '0')
    # Process.Mesh__Heat_Map__Analysis__Growth_Analysis_2D('pAR393xpLH13', 'd1', 'd2', 'No')
    Process.Mesh__Heat_Map__Heat_Map('Geometry/Area', 'No', 'Sum', 'Yes', 'Increasing', 'Ratio', 'Yes', 'No')
    Process.Mesh__Heat_Map__Operators__Export_Heat_to_Attr_Map('Measure Label Double', 'd_Area', 'Label', 'Label Heat', 'Active Mesh', 'No')
    Process.Mesh__Lineage_Tracking__Heat_Map_Proliferation('Yes')
    Process.Mesh__Heat_Map__Operators__Export_Heat_to_Attr_Map('Measure Label Double', 'd_Proliferation', 'Label',
                                                               'Label Heat', 'Active Mesh', 'No')
    Process.Mesh__Cell_Axis__PDG__Check_Correspondence('No', 'No', 'No')
    Process.Mesh__Cell_Axis__PDG__Compute_Growth_Directions()

    # save the mesh (attributes saved in mesh)
    #                           filename, transform, mesh number
    Process.Mesh__System__Save(os.path.join(path, 'meshes', mesh_0), 'no','0')
    Process.Mesh__System__Save(os.path.join(path, 'meshes', mesh_1), 'no', '1')
    Process.Mesh__System__Reset('1')



# function called after check corr, PDG run
# inputs: axis (string), direction of alignment
# custom spec is list of strings needed to specify direction customization
def do_custom_pdg(meshes, path, custom_spec, attrs):
    '''

    :param meshes: list of string names of meshes
    :param path: string save path
    :param custom_spec: list of values needed to specify custom direction
    0                           1
    [ name of direction heatmap, max or min alingment
    :param attrs: list of attr file names
    :return: False when done so this will be skipped when complete
    '''
    for i in range(0, len(meshes) -1):
        load_mesh(meshes[i], 0, 'no')
        load_mesh(meshes[i + 1], 1, 'Yes')

        Process.Stack__System__Set_Current_Stack('Main', '0')
        Process.Mesh__Cell_Axis__Cell_Axis_Import_From_Attr_Map('PDG', 'Measure Label Tensor', 'PDGs', 'No')
        # load directions
        Process.Mesh__Heat_Map__Heat_Map_Load(os.path.join(path, 'attributes', attrs[i]), custom_spec[0], '1.0')
        Process.Mesh__Cell_Axis__Custom__Create_Heatmap_Directions('Yes', 'no')
        # redisplay PDGs for calc
        if custom_spec[1] == 'max':
            Process.Mesh__Cell_Axis__PDG__Display_Growth_Directions('StretchMax', 'Auto', '1', '3', 'StrainMax', 'black', 'red',
                                                                  '3', '4', '0.1', '0', 'No', '1.0')
            # calc custom angles and save to attr map
            Process.Mesh__Cell_Axis__Custom__Custom_Direction_Angle('Max', 'X')
            Process.Mesh__Heat_Map__Operators__Export_Heat_to_Attr_Map('Measure Label Double', 'aniso_angle_max', 'Label',
                                                                   'Label Heat', 'Active Mesh', 'No')
        else:
            Process.Mesh__Cell_Axis__PDG__Display_Growth_Directions('StretchMin', 'Auto', '1', '3', 'StrainMin', 'black',
                                                                    'red',
                                                                    '3', '4', '0.1', '0', 'No', '1.0')
            # calc custom angles and save to attr map
            Process.Mesh__Cell_Axis__Custom__Custom_Direction_Angle('Min', 'X')
            Process.Mesh__Heat_Map__Operators__Export_Heat_to_Attr_Map('Measure Label Double', 'aniso_angle_min', 'Label',
                                                                       'Label Heat', 'Active Mesh', 'No')
       # hopefully this will be saved to attr map
        Process.Mesh__System__Save(os.path.join(path, 'meshes', meshes[i]), 'no','0')
        Process.Mesh__System__Save(os.path.join(path, 'meshes', meshes[i+1]), 'no', '1')
        Process.Mesh__System__Reset('1')

    return []


def do_display(meshes, measures, ranges, attr_dict, path, is_inter, step, custom_axis_spec=None):
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
    # reset meshes for clean images
    # Process.Mesh__System__Reset('0')
    # Process.Mesh__System__Reset('1')
    # user adjust arrangement

    # old dialog strategy
    # user_dialog('Done arranging meshes, start a snappin?')

    # new strategy based on writing to file

    # check files
    meshes_path = os.path.join(path, 'meshes')

    total_steps = len(meshes)

    type_message = 'intra-mesh'
    if is_inter:
        total_steps = len(meshes) - 1
        type_message = 'inter-mesh'

    if step == 0:

        if is_inter:
            load_mesh(dirs_dict['meshes'][step+1], 1, 'Yes')

        load_mesh(dirs_dict['meshes'][step], 0, 'No')
        Process.Mesh__System__View('Yes', 'No', 'Cells', '', 'Wall Heat', '', '', 'No', '', '', '', '', '',
                                   '', '', '-1', '-1')

        # todo set main mesh
        sys.exit('Arrange mesh(es) as desired for images of ' + type_message + ' measures then re-run script')

    else:

        for i in range(0,len(measures)):


            if measures[i] == 'PDGs':
                Process.Mesh__Cell_Axis__Cell_Axis_Import_From_Attr_Map('PDG', 'Measure Label Tensor', 'PDGs', 'No')
                                                 # heatmap, scaleheat, heat min, max, show axis, color +, color -
                Process.Mesh__Cell_Axis__PDG__Display_Growth_Directions('StretchMax', 'Auto', ranges[i][0], ranges[i][1], 'StrainMax',
                                                                        'black', 'red', '3', '4', '0.1', '1', 'No',
                                                                        '1.0')
                Process.Mesh__System__View('No', 'No', 'Cells', '', '', '', '', 'No', 'Border', '', '', '', '', '', '', '-1', '-1')

            if measures[i] == 'PD-PDG_align':
                Process.Mesh__Cell_Axis__Cell_Axis_Import_From_Attr_Map('PDG', 'Measure Label Tensor', 'PDGs', 'No')
                Process.Mesh__Cell_Axis__PDG__Display_Growth_Directions('StretchMax', 'Auto', ranges[i][0], ranges[i][1], 'StrainMax',
                                                                        'black', 'red',
                                                                        '3', '4', '0.1', '1', 'No', '1.0')
                Process.Mesh__Heat_Map__Heat_Map_Load(
                    os.path.join(path, 'attributes', attr_dict['attributes'][step - 1]), 'aniso_angle_max', '1.0')
                Process.Mesh__System__View('Yes', '', '', '', 'Label Heat', '', '', 'No', 'Border', '', '', '', '', '',
                                           '', '-1', '-1')

            # snap basic features of mesh
            elif measures[i] == 'mesh_signal':
                Process.Mesh__System__View('Yes', 'No', 'Cells', '', 'Wall Heat', '', '', 'No', '', '', '', '', '',
                                           '','','-1', '-1')


            elif measures[i] == 'mesh_border':
                Process.Mesh__System__View('No', 'No', 'Cells', '', '', '', '', 'No', 'Border', '', '', '', '',
                                           '','', '-1', '-1')

            elif measures[i] == 'mesh_cells':
                Process.Mesh__System__View('No', 'No', 'Cells', '', '', '', '', 'No', 'Cells', '', '', '', '',
                                           '', '', '-1', '-1')

            elif measures[i] == 'stack':
                # manage
                if dirs_dict.has_key('stacks'):
                    if len(dirs_dict['stacks']) == len(meshes):
                        Process.Stack__System__Clear_Main_Stack('0')
                        Process.Stack__System__Open(os.path.join(main_path, 'stacks', dirs_dict['stacks'][step-1]),
                    'Main', '0', '/label')
                        Process.Mesh__System__View('No', '', '', '', '', '', '', 'No', '', '', '', '', '', '', '', '-1',
                                                   '-1')
                    else:
                        print ('Wrong number of stacks')
                else:
                    print('Missing stacks')



            else:
                #load heatmap
                #
                #                                                                      filename, column name?, border size
                Process.Mesh__Heat_Map__Heat_Map_Load(
                    os.path.join(path, 'attributes', attr_dict['attributes'][step -1]), measures[i], '1.0')
                Process.Mesh__Heat_Map__Heat_Map_Set_Range(ranges[i][0], ranges[i][1])
                # nice viz parameters
                Process.Mesh__System__View('Yes', 'No', 'Cells', '', 'Label Heat', '', '', '', 'Border', '', '', '', '', '',
                                           '', '-1', '-1')
            # take photos
            snap_path = os.path.join(path, 'snaps',
                                     attr_dict['attributes'][step -1][:-8] + "_".join(measures[i].split('/')) + '.png')
            Process.Misc__System__Snapshot(snap_path, 'false', '0', '0',
                                           '1.0', '95')
            Process.Stack__System__Clear_Main_Stack('0')

        if step < total_steps:

            # load new mesh because done all measures
            if is_inter:
                load_mesh(os.path.join(meshes_path, meshes[step+1]), 1, 'Yes')

            load_mesh(os.path.join(meshes_path, meshes[step]), 0, 'No')

            sys.exit('Arrange mesh(es) as desired for images of ' + type_message + ' measures then re-run script')


    # when done doing steps, return empty types list so this function will be skipped over
    return []



####### FILES ##########
pp = pprint.PrettyPrinter()
print(main_path)
dirs_dict = walk(main_path)


############ EXECUTE MEASURES #################

pp.pprint(dirs_dict)

params_dict = get_params(main_path,'params.txt',params_dict)

if params_dict['distance_measures']:
    step = params_dict['distance_measure_step']
    params_dict['distance_measure_step'] = step + 1
    set_params(main_path, 'params.txt',params_dict)
    params_dict['distance_measures'] = do_distance_measures(dirs_dict['meshes'], params_dict['distance_measures'], main_path, step)
    set_params(main_path, 'params.txt',params_dict)

# measures
if params_dict['gen_measures']:
    params_dict['gen_measures'] = do_gen_measures(dirs_dict['meshes'], dirs_dict['parents'], main_path, params_dict['intra_measures'], params_dict['inter_measures'], params_dict['radii'])
    set_params(main_path, 'params.txt', params_dict)


# recalculate attr if saved
# ordering currently a bit weird bc you would need to save attr in order to do custom axis
# but the save attr doesn't work entirely as expected so better to break
attr_dict = walk(os.path.join(main_path, 'attributes'))

if params_dict['custom_axis_spec']:
    params_dict['custom_axis_spec'] = do_custom_pdg(dirs_dict['meshes'], main_path, params_dict['custom_axis_spec'], dirs_dict['attributes'])
    set_params(main_path, 'params.txt', params_dict)

if params_dict['save_attr']:
    params_dict['save_attr'] = do_save_attr(dirs_dict['meshes'], main_path, params_dict['save_attr'])
    set_params(main_path, 'params.txt', params_dict)
# add gen display to end so don't have to be too careful with range indices for other intra_display
params_dict['intra_display'] = params_dict['intra_display'] + params_dict['gen_display']

# displaying meshes
if params_dict['intra_display']:
    step = int(params_dict['intra_display_step'])
    params_dict['intra_display_step'] = step + 1
    set_params(main_path, 'params.txt', params_dict)
    pp.pprint(params_dict)
    params_dict['intra_display'] = do_display(dirs_dict['meshes'], params_dict['intra_display'], params_dict['intra_ranges'], attr_dict, main_path, False, step)
    pp.pprint(params_dict)
    set_params(main_path, 'params.txt', params_dict)

if params_dict['inter_display']:
    step = params_dict['inter_display_step']
    params_dict['inter_display_step'] = step + 1
    set_params(main_path, 'params.txt', params_dict)
    params_dict['inter_display'] = do_display(dirs_dict['meshes'], params_dict['inter_display'], params_dict['inter_ranges'], attr_dict, main_path, True, step)
    set_params(main_path, 'params.txt', params_dict)
    
# done, delete params_dict
os.remove(os.path.join(main_path,'params.txt'))
