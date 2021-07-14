# import python packages
import os

# import imagej packages
from ij import IJ
from ij import WindowManager as WM
from ij.io import FileSaver

# change these w each run #
<<<<<<< HEAD
input_path = '/Volumes/SHARE/leaf1_day_stacks/channels_separated'
=======
input_path = 'D:\leaf1_day_stacks\channels_separated'
>>>>>>> 371182f7b1e4c6f6618e84e82a7f4b0975743e83

# probably don't change -- unless you are changing code functionality
start_extension = '.tif'
new_extension = '.tif'

def load(path):
    IJ.open(path)
    img = WM.getCurrentImage()
    return img

def process(filename, output_path):
    # the number of channels is one (orig image) less than the number of images opened
    curr_img = WM.getCurrentImage()
    fs = FileSaver(curr_img)
    # add scale bar to image
    #IJ.run("Scale Bar...", "width=50 height=20 font=18 color=White background=None location=[Lower Right] hide overlay");
    # save scale bar to stack
    #IJ.run("Flatten");
<<<<<<< HEAD
    #IJ.run(curr_img, "Image...  ", "outputfile=" + os.path.join(output_path, filename[:-4] + "_deep.tif") + " display="+ os.path.join(output_path, filename[:-4] + "_deep.tif"))
    #print("outputfile=" + os.path.join(output_path, filename[:-4] + "_deep.tif") + " display="+ os.path.join(output_path, filename[:-4] + "_deep.tif"))
    fs.saveAsTiffStack(os.path.join(output_path, filename[:-4] + "_deep.tif"))
    #print(os.path.join(output_path, filename[:-4] + "_deep.tif"))
    
=======
    IJ.saveAs("Tiff", os.path.join(output_path, 'w_scale_' + filename))
    #IJ.run("Image...  ", "outputfile=D:\\leaf1_day_stacks\\C2-pAR393xpLH13_1_2_d1a-3.tif display=C2-pAR393xpLH13_1_2_d1a-3.tif")
>>>>>>> 371182f7b1e4c6f6618e84e82a7f4b0975743e83
    curr_img.close()
    return

def batch_process(extension, source_dir):
    for folder, subs, files in os.walk(source_dir):
        output_path = os.path.join(folder, 'scale_tiffs')
        for filename in files:
            if filename.endswith(extension):
                if not os.path.exists(output_path):
                    os.makedirs(output_path)
                img = load(os.path.join(folder, filename))
                process(filename, output_path)
                #img.close()
    return

batch_process(start_extension, input_path)
