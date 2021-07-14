# import python packages
import os

# import imagej packages
from ij import IJ
from ij import WindowManager as WM

# change these w each run #
input_path = 'C:\\Users\\katha\\Desktop\\demo'

# probably don't change -- unless you are changing code functionality
start_extension = '.lsm'
new_extension = '.tif'

def load(path):
    IJ.run("Bio-Formats Importer", "open="+path+" autoscale color_mode=Default display_ome-xml rois_import=[ROI manager] split_channels view=Hyperstack stack_order=XYCZT");

    img = WM.getCurrentImage()
    return img

def process(filename, output_path):
    # the number of channels is one (orig image) less than the number of images opened
    curr_img = WM.getCurrentImage()
        # add scale bar to image
    #IJ.run("Scale Bar...", "width=50 height=20 font=18 color=White background=None location=[Lower Right] hide overlay");
    # save scale bar to stack
    #IJ.run("Flatten");

    num_channels = WM.getImageCount()
    for i in range(0, num_channels):
        curr_img = WM.getCurrentImage()
        IJ.run("Bio-Formats Exporter", "save="+ os.path.join(output_path, '_channel_'+str(i)+'_' + filename[:-4]+new_extension)+" write_each_channel export compression=Uncompressed");

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
    return

batch_process(start_extension, input_path)


