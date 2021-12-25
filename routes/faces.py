from flask import Blueprint

# Route responsible for handling faces related requests
faces = Blueprint('faces', __name__,
                        template_folder='templates')

@faces.route('/faces')
def show():
    return "Faces module"