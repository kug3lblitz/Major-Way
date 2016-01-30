from os.path import abspath, join

from flask import Flask, render_template, request, redirect, \
	send_from_directory, url_for
from werkzeug import secure_filename

# from flask_forms import ContactForm

from parsepdf import getPDFText
from funnel import Funnel, Sprinkler

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
	# return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
	parsed = getPDFText(UPLOAD_FOLDER + filename)
	data = Funnel(parsed).FossilFuel(3)[:6]
	data = [i[1] for i in data]
	return render_template('data.html', data=data)


@app.route('/uploads/<filename>/view')
def ViewPDF(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/uploads/<filename>/data')
def ViewData(filename):
	return send_from_directory('', 'data.json')


@app.route('/success', methods=['GET', 'POST'])
def get_uri():

	print request.form

	if request.method == 'POST':
		
		data = dict((key, request.form.getlist(key)) for key in request.form.keys()).keys()[0]
		data = Sprinkler(data)
		return render_template('success.html', data=data)

	else:

		data = "URL ERROR"
		return render_template('success.html', data=data)

################################### Errors ###################################

# @app.errorhandler(404)
# def page_not_found(e):
# 	return render_template('404.html'), 404

################################### main ###################################

if __name__ == "__main__":
	app.run(debug=True)
