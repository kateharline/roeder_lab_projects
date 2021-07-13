# import python packages
import os

# import imagej packages
from ij import IJ
from ij import WindowManager as WM

# change these w each run #
<<<<<<< HEAD
input_path = 'C:\\Users\\katha\\Desktop\\temp2'
=======
input_path = '/Users/kateharline/Desktop/20210129_screening_jawDxpMZ12'
>>>>>>> fdc7804c533b6f781600532f5e67d5bdb6574253


# probably don't change -- unless you are changing code functionality
start_extension = '.lsm'
new_extension = '.tif'

def load(path):
    IJ.open(path)
    img = WM.getCurrentImage()
    return img

def process(filename, output_path):
	# if multiple channels
    #IJ.run("Make Composite");
    IJ.run("Z Project...", "projection=[Max Intensity]");
    # the number of channels is one (orig image) less than the number of images opened
    
    # add scale bar to image
    IJ.run("Scale Bar...", "width=50 height=20 font=18 color=White background=None location=[Lower Right] hide overlay");
    # save scale bar to stack
    IJ.run("Flatten");
    
    IJ.saveAs("Tiff", os.path.join(output_path, 'maxint_w_scale' + filename))
    # close all the images 
    num_channels = WM.getImageCount()
    for i in range(0, num_channels):
    	curr_img = WM.getCurrentImage()
    	curr_img.close()
    return

def batch_process(extension, source_dir):
    for folder, subs, files in os.walk(source_dir):
        output_path = os.path.join(folder, 'max_int_w_scale')
        for filename in files:
            if filename.endswith(extension):
                if not os.path.exists(output_path):
                    os.makedirs(output_path)
                img = load(os.path.join(folder, filename))
                process(filename, output_path)
    return

batch_process(start_extension, input_path)
