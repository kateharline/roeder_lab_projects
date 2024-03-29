
import os
import platform

####### DIR MANAGEMENT ########

# https://docs.python.org/2/library/os.html
o_s = os.name
if o_s == 'posix':
	# if vmware
	root_path = '/home/kateharline/Desktop/li_paper/methods_video'

	if platform.release() in ['4.15.0-118-generic', '4.15.0-20-generic']:
		# mgx1
		root_path = '/home/aroeder/Desktop/Kate'

# windows
elif o_s == 'nt':
	root_path = 'C:\\Users\\katha\\Desktop'

data_files_path = 'resize'
stacks_path = 'tiffs'

main_path = os.path.join(root_path, data_files_path)

voxel_sizes = ['0.415133', '0.415133', '0.5']

def resize(stack, voxel_sizes, stacks_path):
	Process.Stack__System__Open(os.path.join(stacks_path, stack), 'Main', '0', '', 'No')
	Process.Stack__Canvas__Change_Voxel_Size(voxel_sizes[0], voxel_sizes[1], voxel_sizes[2])
	Process.Stack__System__Save(os.path.join(stacks_path, stack), 'Main', '0', '5', '/label')
	Process.Stack__System__Clear_Main_Stack('0')


def resizer(stacks, voxel_sizes, stacks_path):
	for s in stacks:
		resize(s, voxel_sizes, stacks_path)


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

# get file names
stacks = walk(os.path.join(main_path, stacks_path))
print(stacks)

# iterate through files and resize
resizer(stacks[stacks_path], voxel_sizes, os.path.join(main_path, stacks_path))
