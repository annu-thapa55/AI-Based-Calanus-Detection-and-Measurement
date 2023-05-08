Read this file to understand merging of backend and front end:

Packages to be installed:
-Install Flask:
	pip install flask
-Install werkzeug
	Pip install werkzeug
-Install opencv
	pip install opencv-python
-Install Flask-Reuploaded
	pip install Flask-Reuploaded

structure:
|--static
	|--Images	(contains images used in html files and other app images)
	|--root	(contains necessary files for backend functionalities)
		|--model	(stores weights and class file)
    		|--raw	(stores all the uploaded raw images of Calanus)
    		|--result	(will store outputs, including visual images and text files)
    		|--split	(will store all split raw calanus images. This folder will have several folder under it.
    		|--main.py  (main backend functionalities)
|--templates	(contains all html files)
|--app.py		(main front-end functionalites using Fask)

How to Run:
-Traverse to the folder containing "app.py" file from command prompt. 
-Type "python app.py" in command prompt and hit enter.
-Copy the resultant localhost link from command prompt to the browser. Example: http://127.0.0.1:5000/

Virtual Environment for the project:
-Refer to "setup.docx" for virtual environment creation for the project. 

-------------------------------------------------------------------------------------------
Put some random files in folders "raw", "result" and "split" for structure purpose as github
does not upload empty folders with commit command. These folders are emptied as per the 
necessities while running the app.
-------------------------------------------------------------------------------------------

