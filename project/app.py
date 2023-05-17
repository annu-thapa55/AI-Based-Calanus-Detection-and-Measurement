#packages
from flask import Flask, render_template, request,send_file
import os,shutil
import subprocess
from werkzeug.utils import secure_filename

#Defining upload folder path to store uploaded raw calanus image
UPLOAD_FOLDER = os.path.join('static/root', 'raw')

#Defining path for files related to backend
BACKEND_FOLDER = os.path.join('static', 'root')

#Defining path for Flask's static folder 
app = Flask (__name__, static_url_path= '/static')

#Configuring upload folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#Configuring backend folder that contains backend relevant functionalities and files
app.config['BACKEND_FOLDER'] = BACKEND_FOLDER

#Defining secret key to enable session
app.secret_key = 'calanus'

#function deletes the contents of "raw" and "result" folders and "Results.zip" file
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

            #Iterating thrugh each file in the file list and saving them in "raw" folder

            for imgFile in uploadedRawImgs:
                #Extracting uploaded data file name
                imgFilename = secure_filename(imgFile.filename)

                #Uploading file to the "raw" folder inside "static" folder
                imgFile.save(os.path.join(app.config['UPLOAD_FOLDER'], imgFilename))
            
            #Saving the value of calculated ratio
            calculatedRatio = request.form['ratio']

            #Running Backend functionalities by running main.py and passing calculatedRatio value to main.py
            backend_path = os.path.join(app.config['BACKEND_FOLDER'], 'main.py')
            subprocess.run(["python", backend_path, calculatedRatio])  
            return render_template('downloadResult.html')
         
        else:
            return render_template('index.html')

#decorator for calculating ratio with reference object
@app.route ("/calculateRatio", methods= ['POST'])
def calculateRatio():
    #ratio = float(request.form['ratio'])
    return render_template('ratio.html') 


@app.route('/downloadResult', methods =['GET', 'POST'])
#decorator for downloading result files
def downloadResult():
    downloadPath = os.path.join(app.config['BACKEND_FOLDER'], 'result')
    zipResult = shutil.make_archive('Results', 'zip', downloadPath)
    return send_file(zipResult,as_attachment=True,download_name='results.zip')

if __name__ == "__main__":
    app.run()
