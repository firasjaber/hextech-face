import os
from flask import Blueprint, render_template, flash, redirect, request, send_from_directory
from werkzeug.utils import secure_filename
from database.db import insert_face, query_all_faces

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Route responsible for handling faces related requests
faces = Blueprint('faces', __name__,
                  template_folder='templates')


@faces.route('/faces')
def show():
    faces = query_all_faces()
    return render_template('all_faces.html', faces=faces)


@faces.route('/faces/add')
def add_face():
    return render_template('add_face.html')

# file upload route


@faces.route('/faces', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    name = request.form.get('name', "unnamed")
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join('uploads', filename))
        print('upload_image filename: ' + filename)
        insert_face(name, filename)
        flash('Face image uploaded successfully')
        return render_template('upload.html', filename=filename)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)


@faces.route('/faces/<filename>')
def upload(filename):
    return send_from_directory('uploads/', filename)
