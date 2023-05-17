# AI Based Calanus Detection and Measurement
This project creates a tool that allows scientists to provide a set of images of Calanus catch samples as input along with a conversion scale, and automatically detects the Calanus in the images and outputs their length in millimetres in text files that can be used for further analysis of size distribution...
## Description
This tool is a browser-based web application. We used flask as the framework. The backend is based on Opencv
### Frontend

### Backend
#### Detecting
Our model is Opencv format(.onnx). Weights and classes stored under the folder "model". To detect other objects you can train your own model and replace them. 
#### Measuring
We used opencv method "minCircle" to find the length of objects based on contours. You can modify this method to "minAreaRect" to get both length and width of objects.
#### Output format
Each input image will have two outputs: one text file, one labelled image.
Text file contains Three columns: ID, length(mm), confidential score
ID: Order the integer start from 1. 
Length: pixel value times pixel_mm_ratio.
Confidential score: From YOLO model, for user to exam.
labelled image is the raw image with ID on each calanus, user can check the image and drop unwanted observations basing on ID.
## Getting started
### Requirements
### Installation 

## Usage
