#packages
import cv2
from flask import Flask, render_template, request, send_file, flash
import os, shutil
import subprocess
from werkzeug.utils import secure_filename

#Defining upload folder path to store uploaded raw calanus image
UPLOAD_FOLDER = os.path.join('static/root', 'raw')

#Defining path for files related to backend
BACKEND_FOLDER = os.path.join('static', 'root')

#Defining allowed image extensions
ALLOWED_EXTENSIONS = {'jpg'}


#Defining path for Flask's static folder 
app = Flask (__name__, static_url_path= '/static')

#Configuring UPLOAD_FOLDER 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Configuring backend folder that contains backend relevant functionalities and files
app.config['BACKEND_FOLDER'] = BACKEND_FOLDER

#Defining secret key to enable session
app.secret_key = 'calanus'

#function validates ratio input
def validateRatio(ratio):
    ratio = ratio.strip()

    #check if empty
    if ratio == '':
        return False 
    
    #try converting to float
    try:
        float(ratio)
        return True
    
    except ValueError:
        return False

    
def validateImageSize(imgFile):
    img = cv2.imread(imgFile) 
    
    if img.shape[0] <= 2400:
        return False
    
    if img.shape[1] <= 2400:
        return False
    
    return True

#function deletes the contents of "raw", "result", "split" folders and "Results.zip" file
def clearFolders():
    rawPath= os.path.join(app.config['BACKEND_FOLDER'], 'raw')
    resultPath = os.path.join(app.config['BACKEND_FOLDER'], 'result')

    #deleting contents of "raw" folder 
    for filename in os.listdir(rawPath): 
        filePath = os.path.join(rawPath, filename)  
        try:
            if os.path.isfile(filePath):
                os.remove(filePath)  
            elif os.path.isdir(filePath):  
                 shutil.rmtree(filePath)    
        except Exception as e:  
            print(f"Error deleting {filePath}: {e}")
    
    #deleting contents of "result" folder
    for filename in os.listdir(resultPath): 
        filePath = os.path.join(resultPath, filename)  
        try:
            if os.path.isfile(filePath):
                os.remove(filePath)  
            elif os.path.isdir(filePath):  
                 shutil.rmtree(filePath)   
        except Exception as e:  
            print(f"Error deleting {filePath}: {e}")

    
    #deleting Results.zip 
    zipPath = "Results.zip"
    try:
        if os.path.isfile(zipPath):
            os.remove(zipPath)  
        elif os.path.isdir(zipPath):  
            shutil.rmtree(zipPath)  
    except Exception as e:  
        print(f"Error deleting {filePath}: {e}")


#decorator for Homepage
@app.route("/", methods=['GET', 'POST'])
def homepage():
    clearFolders()
    return render_template('index.html')

#decorator for uploading calanus image and performing detection and measurement  
@app.route("/calanusImageUpload", methods=['GET', 'POST'])
def calanusImageUpload():
    if request.method == 'POST':
        #Functionality of "Find Ratio" button
        if request.form['submit'] =='Find Ratio':
            return render_template('ratio.html')
        
        #Functionality of "Run" button
        elif request.form['submit'] =='Run':

            #Getting list of uploaded files
            uploadedRawImgs = request.files.getlist("rawCalanusImage")

            #Iterating through each file in the file list and saving them in "raw" folder

            for imgFile in uploadedRawImgs:
                #Check if no image has been uploaded
                if imgFile.filename == '':
                    flash('Please upload an image')
                    return render_template('index.html')
            
                 #Extracting uploaded data file name
                imgFilename = secure_filename(imgFile.filename)

                #Uploading file to the "raw" folder inside "static" folder
                imgFile.save(os.path.join(app.config['UPLOAD_FOLDER'], imgFilename))
            
            #Saving the value of calculated ratio
            calculatedRatio = request.form['ratio']

            #Check if ratio has been provided
            if not validateRatio(calculatedRatio):
                flash('Ratio must be a number')
                return render_template('index.html')

            #Validate image size 
            uploadPath = app.config['UPLOAD_FOLDER']
            uploadFiles = [file for file in os.listdir(uploadPath)]
            valid = 0

            for filename in uploadFiles: 
                filePath = os.path.join(uploadPath, filename)  
                
                if validateImageSize(filePath):
                    valid += 1

                #Remove invalid files
                else:
                    try:
                        if os.path.isfile(filePath):
                            os.remove(filePath)  
                            
                    except Exception as e:  
                        print(f"Error deleting {filePath}: {e}")

            #If no valid images, do nothing
            if valid == 0:
                flash('Image width and height must be larger than 2400 pixels')
                return render_template('index.html')


            #Running Backend functionalities by running main.py and passing calculatedRatio value to main.py
            backend_path = os.path.join(app.config['BACKEND_FOLDER'], 'main.py')
            subprocess.run(["python", backend_path, calculatedRatio])  
            return render_template('downloadResult.html')
         
        else:
            return render_template('index.html')

#decorator for calculating ratio with reference object
@app.route ("/calculateRatio", methods= ['POST'])
def calculateRatio():
    return render_template('ratio.html') 


@app.route('/downloadResult', methods =['GET', 'POST'])
#decorator for downloading result files
def downloadResult():
    downloadPath = os.path.join(app.config['BACKEND_FOLDER'], 'result')
    zipResult = shutil.make_archive('Results', 'zip', downloadPath)
    return send_file(zipResult,as_attachment=True,download_name='results.zip')

if __name__ == "__main__":
    app.run()