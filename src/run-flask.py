from flask import Flask, render_template, request, redirect, \
    send_from_directory, url_for
from json import dumps, load

from os.path import abspath, join
from werkzeug import secure_filename

from parsepdf import getPDFText
from funnel import Funnel

app = Flask(__name__)
app.secret_key = "fhdsbfdsnjfbj"


################################### Home page ###################################

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')


################################### File Upload ###################################

UPLOAD_FOLDER = abspath('samples/cache/') + '/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['pdf'])


def allowed_file(filename):

    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/uploads', methods=['GET', 'POST'])
def upload_file():

    if request.method == 'POST':
        inputfile = request.files['file']
        if inputfile and allowed_file(inputfile.filename):
            filename = secure_filename(inputfile.filename)
            inputfile.save(join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))

    return render_template('upload.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):

    parsed = getPDFText(UPLOAD_FOLDER + filename)
    data = Funnel(parsed).FossilFuel(3)[:5]
    data = [i[1] for i in data]
    return render_template('data.html', data=data)


# @app.route('/success', methods=['GET', 'POST'])
# def get_uri():
#     print request.form
#     if request.method == 'POST':
#         data = dict((key, request.form.getlist(key)) for key in
#                     request.form.keys()).keys()[0]
#         data = Sprinkler(data)
#         return render_template('success.html', data=data)
#     else:
#         data = "URL ERROR"
#         return render_template('success.html', data=data)


@app.route('/uploads/<filename>/view')
def ViewPDF(filename):

    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/success', methods=['GET', 'POST'])
def get_json_information():

    if request.method == 'GET':

        with open('data1.json') as data_file:
            data = load(data_file)

        json_obj = dumps(data)

        return render_template('success.html', data=json_obj)


################################### main ###################################

if __name__ == "__main__":
    app.run(debug=True)