from flask import Blueprint

# Route responsible for handling detection related requests
detector = Blueprint('detector', __name__,
                        template_folder='templates')

@detector.route('/detector')
def show():
    return "Face Detector module"