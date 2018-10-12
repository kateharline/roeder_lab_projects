# import python packages
import os

# import imagej packages
from ij import IJ
from ij import WindowManager as WM

# change these w each run #
input_path = '/Users/kateharline/Documents/roeder_lab/imaging/leaf_live_beta/example'
num_channels = 2

# probably don't change -- unless you are changing code functionality
start_extension = '.lsm'
new_extension = '.tif'
output_path = input_path + '/channels_separated/'

if not os.path.exists(output_path):
	os.makedirs(output_path)

def load(path):
	IJ.open(path)
	img = WM.getCurrentImage()
	return img

def process(filename, output_path):
	IJ.run("Split Channels")
	for i in range(0, num_channels):
		curr_img = WM.getCurrentImage()
		IJ.saveAs("Tiff", output_path + 'C-'+ str(i+1) + filename)
		curr_img.close()
	return
	
def batch_process(extension, source_dir, output_dir):
	for filename in os.listdir(source_dir):
		if filename.endswith(extension):
			img = load(source_dir + '/'+ filename)
			process(filename, output_path)
			img.close()
	return

batch_process(start_extension, input_path, output_path)
