README.TXT
==============================================================================================

GETTING STARTED
----------------------------------------------------------------------------------------------
PREREQUISITES

- Python >= 3.9 

INSTALL REQUIREMENTS

Use command line to navigate to the location of requirements.txt and install the requirements:
- cd PATH_TO_PROJECT
- pip install -r requirements.txt
==============================================================================================

USAGE
----------------------------------------------------------------------------------------------
STARTING THE APPLICATION

A) WITH RUN.cmd SCRIPT:
- If you have Windows and your security settings permit it, double-click RUN.cmd

B) WITH COMMAND LINE:
- Open the command line interface
- Navigate to the folder containing the app.py file: cd PATH_TO_PROJECT
- Enter the following command: python app.py
- Open your browser and go to: http://127.0.0.1:5000

HOW TO USE

1. Enter the known millimeter/pixel ratio of the images you plan to upload to the application
2. Upload one or more images in JPG format
3. Press the "Run" button and wait for the analysis to complete
4. Download your results

FIND RATIO 

If you do not know the ratio already, you can press the "Unknown Ratio". 
Here, you can upload an image with a reference object of a known length in millimeters 
and compute the millimeter/pixel ratio.

1. Upload an image with a reference object
2. Place a point at the start of the object and another at the end of it
3. Enter the known length in millimeters between the two points
4. When you are ready, press the "Calculate" button to find the ratio and go back to the 
   home page where the ratio is saved
==============================================================================================

OUTPUT
----------------------------------------------------------------------------------------------

The output is a zip file containing a .txt file for every input image with each detected
and measured Calanus listed on a row with the following information:

ID,length_in_mm,confidence

ID is a unique identifier given to the object, length_in_mm is the estimated length converted 
to millimeters based on the provided ratio, and confidence is the confidence that the 
detected object is a Calanus.

The input image(s) is also provided in the zip with the length estimation visualised as 
enclosing circles around each detected Calanus, along with its ID.
==============================================================================================