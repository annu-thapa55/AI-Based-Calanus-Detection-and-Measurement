# AI Based Calanus Detection and Measurement
A Flask web application that automatically detects and measures Calanus in images with the use of object detection and other computer vision techniques.

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#description">Description</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
        <li><a href="#performance">Performance</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#requirements">Requirements</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#find-ratio">Find Ratio</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
      <ul>
        <li><a href="#starting-the-application">Starting the Application</a></li>
        <li><a href="#how-to-use">How to Use</a></li>
        <li><a href="#output">Output</a></li>
      </ul>
  </ol>
</details>

## Description
This project offers an AI-based solution to automatic Calanus detection and length estimation which lets users upload one or more images and a millimetre-to-pixel ratio and outputs a list of all the detected lengths in millimetres in a text file for each image, as well as the corresponding detections and measurements visualised on the image. The system has been developed by training a [YOLOv5s model](https://github.com/ultralytics/yolov5) to recognise Calanus and using a variety of computer vision methods from OpenCV to estimate the length of the detected Calanus. The resulting tool has been integrated into a user-friendly web application based on Flask.

Information about the training process can be found [here](https://github.com/annu-thapa55/AI-Based-Calanus-Detection-and-Measurement/blob/main/yolov5/yolov5s_training.ipynb).

### Built With
* [![Flask][Flask-image]][Flask-url]
* [![OpenCV][OpenCV-image]][OpenCV-url]

### Performance 
* 95.8% precision and 92% recall for Calanus detection
* Less than 10% error rate for more than 95% of length estimations
* A speed of 1.32 images per minute for very high resolution images

## Getting Started
### Prerequisites
* [Python ≥ 3.9](https://www.python.org/downloads/)
### Installation 
1. Clone the repo if you have git.
```
git clone https://github.com/annu-thapa55/AI-Based-Calanus-Detection-and-Measurement.git
```
Or press Code➝Download ZIP.

2. Navigate to the location of the requirements file on your system and install the requirements.
```
cd PATH_TO_PROJECT
pip install -r requirements.txt
```

## Usage
### Starting the Application
There are multiple ways of starting the application.
#### With RUN.cmd Script
1. If you have Windows, you can double-click the provided RUN.cmd file to open the application.

#### With Command Line
1. Open the command line interface.
2. Navigate to the folder containing the app.py file.
```
cd PATH_TO_PROJECT
```
3. Enter the following command:
```
python app.py
```
4. Open your browser and go to the localhost URL for the web app as specified below:
```
http://127.0.0.1:5000
```
### How to Use
1. Enter the known millimeter/pixel ratio of the images you plan to upload to the application. 
2. Upload one or more images in JPG format.
3. Press the "Run" button and wait for the analysis to complete.
4. Download your results.  

If you want to test the application but do not have any images, you can find some sample images for analysis [here](https://github.com/annu-thapa55/AI-Based-Calanus-Detection-and-Measurement/tree/main/sample-images/raw-images).

<p align="center">
<img src="https://github.com/annu-thapa55/AI-Based-Calanus-Detection-and-Measurement/assets/41973043/0105e3e7-b354-46b5-a6d5-209a933d6628" width="700"/>
</p>

#### Find Ratio 
If you do not know the ratio already, you can press the "Unknown Ratio". 
Here, you can upload an image with a reference object of a known length in millimeters and compute the millimeter/pixel ratio.
1. Upload an image with a reference object. 
2. Place a point at the start of the object and another at the end of it.
3. Enter the known length in millimeters between the two points.
4. When you are ready, press the "Calculate" button to find the ratio and go back to the home page where the ratio is saved.

Sample images with references objects have been provided [here](https://github.com/annu-thapa55/AI-Based-Calanus-Detection-and-Measurement/tree/main/sample-images/ratio-images).

<p align="center">

<p align="center">
<img src="https://github.com/annu-thapa55/AI-Based-Calanus-Detection-and-Measurement/assets/41973043/3348f57a-3057-4957-ad64-13bbba31ad5a" width="700"/>
</p>

### Output
The output after running the analysis is a zip folder. This folder will contain a text file (.txt) for every input image. In the text file, each detected and measured Calanus will be listed on a row with the following information:

<p align="center"><i>ID,length_in_mm,confidence</i></p>

Where ID is a unique identifier given to the object, length_in_mm is the estimated length converted to millimeters based on the provided ratio, and confidence is the confidence that the detected object is a Calanus. 

Furthermore, the input image(s) is also provided in the zip with the length estimation visualised as enclosing circles around each detected Calanus, along with its ID. 

<p align="center">
<img src="https://github.com/annu-thapa55/AI-Based-Calanus-Detection-and-Measurement/assets/41973043/847db595-cbd7-41ed-a0b9-e7d8c1066b9b" width="500"/>
</p>

<!-- MARKDOWN LINKS & IMAGES -->
[Flask-image]: https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white
[Flask-url]: https://flask.palletsprojects.com/
[OpenCV-image]: https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white
[OpenCV-url]: https://opencv.org/
