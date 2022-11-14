from flask import Flask
import os
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/cluster/'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
'''
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	

@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_image():
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		#print('upload_image filename: ' + filename)
		flash('Image successfully uploaded and displayed below')
		return render_template('upload.html', filename=filename)
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
	print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)
	#return redirect(url_for('uploads/'+ filename), code=301)

'''

'''

@app.route('/')
def display_all():
	#hists = os.listdir(UPLOAD_FOLDER)
	display_i2c =  { 'I9_grp.jpeg': [4, 5], 'I2_mic.jpeg': [10] }
	


	#print(hists)
	#hists = [UPLOAD_FOLDER + file for file in hists]


	return render_template('report.html', display_i2c = display_i2c , UPLOAD_FOLDER = UPLOAD_FOLDER)

'''

@app.route('/', methods = ["POST", "GET"])
def display_all():
	display_i2c =  { 'I9_grp.jpeg': [4, 5], 'I2_mic.jpeg': [10] }

	if request.method == "POST":
		
		c2name = {}
		for val in [4,5,10]:
			print(request.form)
			c2name[val] = request.form[str(val)]
		#print(c2name)
		

		return render_template('success.html')


	return render_template('report.html', display_i2c = display_i2c , UPLOAD_FOLDER = UPLOAD_FOLDER)


if __name__ == "__main__":

	display_i2c =  { 'I9_grp.jpeg': [4, 5], 'I2_mic.jpeg': [10] }
	
	app.run(debug = True)

