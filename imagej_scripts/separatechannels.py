# import python packages
import os

# import imagej packages
from ij import IJ
from ij import WindowManager as WM

# change these w each run #
<<<<<<< HEAD
input_path = '/Volumes/SHARE/leaf1_day_stacks'
=======
input_path = 'C:\\Users\\katha\\Desktop\\first_leaf_analy'
>>>>>>> 371182f7b1e4c6f6618e84e82a7f4b0975743e83

# probably don't change -- unless you are changing code functionality
start_extension = '.lsm'
new_extension = '.tif'

def load(path):
    IJ.open(path)
    img = WM.getCurrentImage()
    return img

def process(filename, output_path):
    IJ.run("Split Channels")
    # the number of channels is one (orig image) less than the number of images opened
    num_channels = WM.getImageCount()
    for i in range(0, num_channels):
        curr_img = WM.getCurrentImage()
        IJ.saveAs("Tiff", os.path.join(output_path, 'C-'+ str(i+1) + '_' + filename))
        #IJ.run("Image...  ", "outputfile=" + os.path.join(output_path, 'C-'+ str(i+1) + '_' + filename[:-4] + ".tif") + " display="+filename[:-4]+ ".tif")
        #print( "outputfile=" + os.path.join(output_path, 'C-'+ str(i+1) + '_' + filename[:-4] + ".tif") + " display="+filename[:-4]+ ".tif")
        curr_img.close()
    return

def batch_process(extension, source_dir):
    for folder, subs, files in os.walk(source_dir):
        output_path = os.path.join(folder, 'channels_separated')
        for filename in files:
            if filename.endswith(extension):
                if not os.path.exists(output_path):
                    os.makedirs(output_path)
                img = load(os.path.join(folder, filename))
                process(filename, output_path)
                # img.close()
    return

batch_process(start_extension, input_path)


# open("/Volumes/SHARE/leaf1_day_stacks/pAR393xpLH13_3_5_d1a.lsm");
#run("Split Channels");
#selectWindow("C2-pAR393xpLH13_3_5_d1a.lsm");
#run("Image...  ", "outputfile=/Volumes/SHARE/leaf1_day_stacks/C2-pAR393xpLH13_3_5_d1a_test.tif display=C2-pAR393xpLH13_3_5_d1a_test.tif");
#saveAs("Tiff", "/Volumes/SHARE/leaf1_day_stacks/d1a_test.tif");
