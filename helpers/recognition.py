import face_recognition
from database.db import query_all_faces
import os

def match_face(unknown_face_path):
	faces = query_all_faces()

	unknown_image = face_recognition.load_image_file(f"./uploads/{unknown_face_path}")
	unknown_image_encoding = face_recognition.face_encodings(unknown_image)

	detected = False
	res = {"detected" : False, "person" : "", "original_img" : ""}
	for face in faces:
		path = f'./uploads/{face["face"]}'
		if os.path.isfile(path) == False:
			continue

		known_image = face_recognition.load_image_file(path)

		if len(face_recognition.face_encodings(known_image)) == 0:
			continue

		know_image_encoding = face_recognition.face_encodings(known_image)[0]

		results = face_recognition.compare_faces(unknown_image_encoding, know_image_encoding)	
		if len(results) > 0 and results[0] == True:
			res["detected"] = True
			res["person"] = face["name"]
			res["original_img"] = face["face"]
			break

	return res