# import python packages
import os

# import imagej packages
from ij import IJ
from ij import WindowManager as WM

# change these w each run #
input_path = '/Users/kateharline/Documents/roeder_lab/imaging/leaf_live_beta/example'

# probably don't change -- unless you are changing code functionality
new_extension = '.tiff'

if not os.path.exists(input_path + '/channels_separated')
	os.makedirs(input_path + '/channels_separated')

def batch_process(extension, source_dir, output_dir):
	for filename in os.listdir(source_dir):
		if filename.endswith(extension):
			continue
		img = load(source_dir + filename)

		save(output_dir + filename + '.' + new_extension)
		
#volume = IJ.openImage()