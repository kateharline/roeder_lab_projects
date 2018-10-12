input = "/Users/kateharline/Documents/roeder_lab/imaging/leaf_live_beta/example";
output = "/Users/kateharline/Documents/roeder_lab/imaging/leaf_live_beta/example";

setBatchMode(true);
list = getFileList(input);
for (i = 0; i < list.length; i++)
		logService.info(list[i]);
        action(input, output, list[i]);
setBatchMode(false);


function action(input, output, filename) {
		
        run("LSM Reader", "open="+filename);
        run("Split Channels");
        selectWindow("C1-" + filename);
        saveAs("Tiff", output + "C1-" + filename);
        selectWindow("C2-" + filename);
        saveAs("Tiff", output + "C2-" + filename);
        selectWindow("C3-" + filename);
        saveAs("Tiff", output + "C3-" + filename);
        close();
}
