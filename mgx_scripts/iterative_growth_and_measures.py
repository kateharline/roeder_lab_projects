######## New MorphoGraphX session v2.0 r1-63-ga635c756: 2020-08-27 18:16:00
from os import walk

# main directory
path = 'C:/Users/katha/Desktop/analysis/processing_2_3/mgx/20200307_0715_mgx_meshes_view_files/'

# get list of files in dir https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
f = []


# open mgx
# load stack 1, stack 2
Process.Mesh__System__Load('d1_pAR393xpLH13_mesh_seg.mgxm', 'no', 'no', '0')
Process.Mesh__System__Load('C:/Users/katha/Desktop/analysis/processing_2_3/mgx/20200307_0715_mgx_meshes_view_files/d2_pAR393xpLH13_mesh.mgxm', 'no', 'no', '1')

# set stack 1 as main
Process.Stack__System__Set_Current_Stack('Main', '0')

# load special axis heat
Process.Mesh__Heat_Map__Heat_Map_Load('', '2', '1.0')

# run all measures, <<based on special axis>>
Process.Mesh__Heat_Map__Analysis__Cell_Analysis_2D('No')
Process.Mesh__Heat_Map__Operators__Export_Heat_to_Attr_Map('Measure Label Double', 'test', 'Label', 'Label Heat', 'Active Mesh', 'No')
Process.Mesh__Attributes__Save_to_CSV('')

# 'click' parents in stack 2
# Process.Mesh__Lineage_Tracking__Parent_Import_from_Attr_Map('Measure Label Int', 'Parents')


# run growth pipeline
Process.Mesh__Heat_Map__Analysis__Growth_Analysis_2D('', 'T2', 'T3', 'Yes')

# export attribute map <<based on on axis>>
Process.Mesh__Heat_Map__Operators__Export_Heat_to_Attr_Map('Measure Label Double', 'test', 'Label', 'Label Heat', 'Active Mesh', 'No')
Process.Mesh__Attributes__Save_to_CSV('')

# photos of heatmaps
Process.Mesh__Heat_Map__Heat_Map_Load('', '2', '1.0')
Process.Misc__System__Snapshot('snap_test', 'false', '0', '0', '1.0', '95')




Process.Stack__System__Set_Current_Stack('Main', '2')
Process.Stack__System__Set_Current_Stack('Main', '1')

Process.Mesh__Heat_Map__Heat_Map_Save('')
Process.Mesh__Lineage_Tracking__Save_Parents('', 'Yes')
Process.Mesh__Lineage_Tracking__Load_Parents('', 'CSV', 'No')
Process.Misc__System__Snapshot('', 'false', '0', '0', '1.0', '95')
Process.Misc__System__Snapshot('snap_test', 'false', '0', '0', '1.0', '95')





