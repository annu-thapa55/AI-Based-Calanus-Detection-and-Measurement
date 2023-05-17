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
        <li><a href="#running-the-application">Running the Application</a></li>
        <li><a href="#output">Output</a></li>
      </ul>
    <li><a href="#customization">Customization</a></li>
  </ol>
</details>

## Description
This project offers an AI-based solution to automatic Calanus detection and length estimation which lets users upload one or more images and a millimetre-to-pixel ratio and outputs a list of all the detected lengths in millimetres in a text file for each image, as well as the corresponding detections and measurements visualised on the image. The system has been developed by training a [YOLOv5 model](https://github.com/ultralytics/yolov5) to recognise Calanus and using a variety of computer vision methods from OpenCV to estimate the length of the detected Calanus. The resulting tool has been integrated into a user-friendly web application based on Flask.

### Built With
* [![Flask][Flask-image]][Flask-url]
* [![OpenCV][OpenCV-image]][OpenCV-url]

### Performance 
* 95.8% precision and 92% recall for Calanus detection
* Less than 10% error rate for more than 95% of length estimations
* A speed of 1.32 images per minute for very high resolution images

## Getting Started
### Requirements
If packages need to be installed manually, they should be listed here...
### Installation 
Cloning the repo, command for installing requirements if we have a requirements.txt file...
1. Clone the repo
```
git clone https://github.com/annu-thapa55/AI-Based-Calanus-Detection-and-Measurement.git
```
Or use https://download-directory.github.io/ to download it.

2. Install requirements
```
pip install -r requirements.txt
```

## Usage
### Running the Application
To start the application, do...


Write something about sample images 

Add additional sections that demonstrate how to use the app, including images

### Output
Include images

Each input image will have two outputs: one text file, one labelled image.
Text file contains Three columns: ID, length(mm), confidential score
ID: Order the integer start from 1. 
Length: pixel value times pixel_mm_ratio.
Confidential score: From YOLO model, for user to exam.
labelled image is the raw image with ID on each calanus, user can check the image and drop unwanted observations basing on ID.

### Find Ratio 

## Customization
Our model is Opencv format(.onnx). Weights and classes stored under the folder "model". To detect other objects you can train your own model and replace them. 
We used opencv method "minCircle" to find the length of objects based on contours. You can modify this method to "minAreaRect" to get both length and width of objects.


<!-- MARKDOWN LINKS & IMAGES -->
[Flask-image]: https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white
[Flask-url]: https://flask.palletsprojects.com/
[OpenCV-image]: https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white
[OpenCV-url]: https://opencv.org/
