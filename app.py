from flask import Flask
from routes.detector import detector
from routes.faces import faces
app = Flask(__name__)

app.secret_key = "secret key"

app.register_blueprint(detector)
app.register_blueprint(faces)

@app.route("/")
def hello():
  return "index route"

if __name__ == "__main__":
  app.run()
