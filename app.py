from flask import Flask, render_template,send_file

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

#very app.route has coresponding url, that's the one for the link of download
@app.route('/download_file')
#once click the link will triger the function
def download_file():
    path = "download.png"
    return send_file(path,as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)