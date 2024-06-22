The DAIDEM Metric:

Contact Todd Gillette (tgillett@gmu.edu) with questions concerning using or modifying the metric.
Developed in collaboration with Kerry Brown and Dr. Giorgio Ascoli
Gillette, T. A., Brown, K. M., & Ascoli, G. A. (2011). The DIADEM Metric: Comparing Multiple Reconstructions of the Same Neuron. Neuroinformatics, 9(2-3): 233-45.

The DIADEM metric is implemented as a command line Java program run from a JAR file. This requires that you have Java installed on your computer. Java is available at http://www.java.com/ where you will be directed to the appropriate version for your operating system. The metric can score one gold standard reconstruction against one test reconstruction, or several of each at one time, depending on the values of the first two parameters. Expected units in the SWC files are pixels for X and Y, and images for Z (the same units as those in the provided manual reconstructions). This archive contains the following files:

	DiademMetric.jar - The metric program to be used on all data sets.

	JSAP-2.1.jar - A Java library required by the metric.

	ExampleGoldStandard.swc - An example gold standard reconstruction for testing (instructions for use further down on this page).

	ExampleTest.swc - An example test reconstruction to score against the ExampleGoldStandard.swc file.

	readme.txt - This file

	api.txt - A primitive API for the DiademMetric Java class.

Source code can be downloaded from http://diademchallenge.org/docs/DiademMetricSource.zip or http://diademchallenge.org/docs/DiademMetricSource.tar. A basic API is contained in this directory. The command line parameter descriptions along with comments in the source should provide a fair amount of context for understanding the methods at least within DiademMetric.java.

The DiademMetric.jar will function on any operating system with the appropriate version of Java installed. To run the metric, unzip/extract the files from the zip file and then use the following command from the directory in which you have saved/downloaded the Diadem Metric files:

java -jar DiademMetric.jar -G [GoldStandardFilename] -T [TestReconstructionFilename] -D [data set number]

The input files (described next in the next section) are of the SWC format, as described in the background section of the DIADEM Challenge website (http://diademchallenge.org, or see the NeuronLand specification http://www.neuronland.org/NLMorphologyConverter/MorphologyFormats/SWC/Spec.html). While multiple trees may be included in an SWC file, the DIADEM metric will only use the first. You will see a warning when multiple trees are detected in one file. Any violations of the SWC format will produce an error message describing the violation.
This sample command includes the required parameters (a working example is provided at the end of this page). Required and non-required parameters are described below. Using an incorrect set of parameters will result in a description of allowable parameters and types. Parameters added in the post-competition version are described after the example below.

Parameters:
-G / --gold-standard
Required. The gold standard reconstruction filename or directory name is required and is commonly the manual reconstruction. If a file name is entered, a file name must be entered for the test data parameter and both files must have .swc extensions. If a directory is entered, a directory must be entered for the test data parameter. Files and directories can be entered with a local (e.g. manualRecon1.swc) or global path (e.g. C:/reconstructions/manualRecon1.swc or /reconstructions/manualRecon1.swc depending on your system).

-T / --test-data
Required. The test reconstruction filename or directory name is also required and is commonly the automated reconstruction that is being tested. If a file name is entered, a file name must be entered for the gold standard parameter and both files must have .swc extensions. If a directory is entered, a directory must be entered for the gold standard parameter. Files and directories can be entered with a local (e.g. automaticRecon1.swc) or global path (e.g. C:/reconstructions/automaticRecon1.swc or /reconstructions/automaticRecon1.swc depending on your system).

-D / --dataset
Not required, default 0. This parameter was required during the DIADEM competition, but in the post-competition version the user may ignore it and explicitly set the various threshold parameters.
1. Cerebellar Climbing Fibers
2. Hippocampal CA3 Interneuron
3. Neocortical Layer 6 Axons
4. Neuromuscular Projection Fibers
5. Olfactory Projection Fibers
6. Visual Cortical Axons

-m / --misses
Not required, default 'false'. Boolean parameter which when true will produce a list of node positions that are scored as misses, as well as excess nodes that appear in the automated reconstruction but not in the gold standard.

Output:
The program will output the final score according to the rules described on the Metric Description page.

Example:
Run the metric on the sample swc files included in DiademMetric.zip:
 java -jar DiademMetric.jar -G ExampleGoldStandard.swc -T ExampleTest.swc -D 5 -m true
Below are the results you should see:
 Score: 0.987

 Nodes that were missed (position and weight):
 (143.56,237.16,46.733) 2
 (139.21,238.6,48.066) 1
 (418.35,163.83,40.641) 1

 Extra nodes in test reconstruction (position and weight):
 (403.51,158.6,37) 1
 (400.35,161.83,38.998) 1
 (401.3,159.26,32.202) 1

Additional Parameters:
The following parameters are new to the post-competition release. Thresholds, the XY/Z (pixels/image) ratio, and the spur size parameter are all set to dataset-specific values but can be overridden via the command line parameters below or via the API function calls (yet to be released) for those interested in incorporating the metric into their code. Failure to select a dataset and specific parameter values (i.e. thresholds, XY/Z ratio, and spur size) will result in the use of default values that may not be appropriate for your specific data.

-w / --weight-scheme
Not required, default '1': Weight by degree. This parameter requires a number that identifies a weight scheme. The current set of schemes is limited to a uniform weighting scheme and a few variations on weight by degree:
1.	Weight by degree
2.	Uniform weight
3.	Square root of degree
4.	Harmonic mean of a node's subtrees' degree

-x / --xy-threshold
Not required, default '1'. This parameter requires a number that sets the XY Euclidean distance threshold for node location. Units should be based on whatever units are used in the entered SWC files, and should be consistent with all other threshold parameters (e.g. spur length).

-R / --xy-z-ratio
Not required, default '1'. This parameter requires a number representing the XY/Z Ratio, that is the number of XY pixels per Z image. This allows the Z-threshold to be entered in terms of images and then converted to pixels.

-Z / --z-threshold
Not required, default '1'. This parameter requires a number that sets the Z Euclidean distance threshold (in images) for node location. If a dataset is not selected (-D/--dataset) this parameter should be set, however currently that is not enforced.

-t / --terminal-threshold
Not required, default '0'. This parameter requires a number that, if greater than 0, multiplies the Euclidean distance threshold for searching for a terminal match. When this process is taken, the longer path must come within the Euclidean distance threshold of the shorter path's end point, and the path lengths from that point must fall within the path length error threshold.

-p / --terminal-path-threshold
Not required, default '1.0'. This parameter sets a limit on how much shorter the test reconstruction path can be relative to the gold standard path for a gold standard terminal node. If set to 0 while the terminal threshold is greater than 0, longer test paths can be matched, but longer gold standard terminal paths cannot be matched. A value less than 1 will allow the gold standard terminal node to be matched to a test node with a shorter path length.

--xy-path-thresh
Not required, default '0.08'. This determines the amount of allowable path error in the XY plane, relative to the total gold standard path length (in three dimensions).

--z-path-thresh
Not required, default '0.20'. This determines the amount of allowable path error in the Z dimension, relative to the total gold standard path length (in three dimensions).

-r / --remove-spurs
Note required, default '0'. The distance under which a node's branch will not count toward the score. However, such nodes can still be matched. By default there are no spurs.

-c / --list-continuations
Not required, default 'false'. If true, the program will output a list of nodes that were found to be continuations.

-d / --list-distant-matches
Not required, default 'false'. If true, the program will output a list of nodes that were found to be distant matches. Distant matches are defined as nodes that are scored as continuations but have a test node within three times the normal threshold distance that have the same local connectivity. Such a case may occur where the angle of bifurcation is very small, making a determination of the bifurcation location difficult along the neurite.

--z-path
Not required, default 'true'. If set to false, the program will ignore the Z-component of Euclidean distance matching and path length matching. Of the default datasets, the parameter is only set to false for the Neuromuscular Projection Fiber set.

--excess-nodes
Not required, default 'true'. If set to false, the metric will not count excess nodes against the final score. By default excess nodes do count against the final score.

-M / --microns
Not required, default 'false'. Boolean parameter that converts the dataset-specific thresholds to microns. If you use your own thresholds, this parameter has no effect.
The following parameters are available in the “test mode”. This can only be set by editing the static variable “mode” (at the top of DiademMetric.java) and setting it to 0 prior to compiling. The program can then be exported to a new DiademMetric.jar using the DiademMetricManifest.txt. Be sure to include all java files in the data, domain, and utils packages.

-X / --X
Not required, default '0'. In the test mode, this variable will lead to specific output for any node within threshold distance of the position given by the -X and -Y parameters.

-Y / --Y
Same as, and used in conjunction with, -X.

--debug
Not required, default 'false'. If true, a variety of additional information will be printed to the terminal.

* Valid Boolean parameters are described in the Java Simple Argument Parser (JSAP) API - http://martiansoftware.com/jsap/doc/javadoc/