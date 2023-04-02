from flask import Flask, request, render_template
import os

app = Flask(__name__, template_folder='template',static_folder='/Users/harshitbatra/Documents/',  static_url_path='/Users/harshitbatra/Documents/')

# Set the upload folder and allowed file types
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}
app.config['UPLOAD_FOLDER'] = "/Users/harshitbatra/Documents/"

# Check if the uploaded file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Render the HTML template with the upload form
@app.route('/')
def index():
    return render_template('upload.html')

# Handle the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Check if a file was uploaded
    if 'file' not in request.files:
        return 'No file uploaded'
    
    file = request.files['file']
    
    # Check if the file is allowed
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image_url= os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # return 'File uploaded successfully'
        print("print "+ image_url)
        return render_template('test.html',image_url = image_url)
    return 'Invalid file type'

# @app.route('/main')
# def main():
#     return render_template('test.html')

@app.route('/send_to_opencv', methods=['POST'])
def send_to_opencv():
    imgData = request.json
    # Process the image data with OpenCV
    return jsonify({'result': 'success'})

if __name__ == '__main__':
    app.run(debug=True)
