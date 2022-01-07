from flask import Blueprint, render_template, redirect, flash,request,url_for,send_from_directory
import urllib.request
from werkzeug.utils import secure_filename
import os
from helpers.email import sendEmail

from helpers.recognition import match_face

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route responsible for handling detection related requests
detector = Blueprint('detector', __name__,
                        template_folder='templates')

# face upload form
@detector.route('/detector')
def upload_form():
	return render_template('detector.html')

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
		print(os.path.isdir("uploads"))
		file.save(os.path.join('uploads', filename))
		face_detected = match_face(filename)
		if face_detected["detected"]:
			flash("Face detected !")
		else:
			flash("Face not found !")
			sendEmail()
		print(face_detected)
		return render_template('detector.html', filename=filename, face_detected=face_detected)
	else:
		flash('Allowed image types are -> png, jpg, jpeg, gif')
		return redirect(request.url)


@detector.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory('uploads/', filename)