from flask import Flask, render_template, request

app = Flask (__name__, static_url_path= '/static')

#decorator for Homepage
@app.route("/")
def homepage():
    return render_template('index.html')

#decorator for calculating ratio with reference object
@app.route ("/calculateRatio", methods= ['POST'])
def calculateRatio():
    #ratio = float(request.form['ratio'])
    return render_template('ratio.html') 


if __name__ == "__main__":
    app.run()