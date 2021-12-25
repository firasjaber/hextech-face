from flask import Blueprint, render_template, redirect, flash,request,url_for,send_from_directory
import urllib.request
from werkzeug.utils import secure_filename
import os

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route responsible for handling detection related requests
detector = Blueprint('detector', __name__,
                        template_folder='templates')

# face upload form
@detector.route('/detector')
def upload_form():
	return render_template('upload.html')

# file upload route
@detector.route('/detector', methods=['POST'])
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
		print("here..")
		print(os.path.isdir("uploads"))
		file.save(os.path.join('uploads', filename))
		print("....")
		print('upload_image filename: ' + filename)
		flash('Image successfully uploaded and displayed below')
		return render_template('upload.html', filename=filename)
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)

# result
@detector.route('/detector/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

@detector.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory('uploads/', filename)