# AI Based Calanus Detection and Measurement
This project creates a tool that allows scientists to provide a set of images of Calanus catch samples as input along with a conversion scale, and automatically detects the Calanus in the images and outputs their length in millimetres in text files that can be used for further analysis of size distribution...
## Description

### Built With
* [![Flask][Flask-image]][Flask-url]
* [![OpenCV][OpenCV-image]][OpenCV-url]

This tool is a browser-based web application. We used flask as the framework. The backend is based on Opencv


Our model is Opencv format(.onnx). Weights and classes stored under the folder "model". To detect other objects you can train your own model and replace them. 

We used opencv method "minCircle" to find the length of objects based on contours. You can modify this method to "minAreaRect" to get both length and width of objects.


## Getting Started
### Requirements
If packages need to be installed manually, they should be listed here...
### Installation 
Cloning the repo, command for installing requirements if we have a requirements.txt file...
1. Clone the repo
```
git clone https://github.com/annu-thapa55/AI-Based-Calanus-Detection-and-Measurement.git
```
2. Install requirements
```
pip install -r requirements.txt
```

## Usage
### Running the Application
To start the application, do...

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


<!-- MARKDOWN LINKS & IMAGES -->
[Flask-image]: https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white
[Flask-url]: https://flask.palletsprojects.com/
[OpenCV-image]: https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white
[OpenCV-url]: https://opencv.org/
