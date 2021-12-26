import sqlite3

DB_PATH = "./db.sq3"

conn = sqlite3.connect(DB_PATH,check_same_thread=False)
cur = conn.cursor()

def create_table():
	sql_create_person = """ CREATE TABLE IF NOT EXISTS PERSON (
														PersonID INTEGER PRIMARY KEY AUTOINCREMENT, 
														Name varchar(200) NOT NULL
													); """
	sql_create_face = """ CREATE TABLE IF NOT EXISTS FACE (
													FaceID INTEGER PRIMARY KEY AUTOINCREMENT, 
													PersonID int  NOT NULL ,
													filename varchar(200)  NOT NULL ,
													FOREIGN KEY(PersonID) REFERENCES PERSON(PERSONID)
												); """
	## CREATE TABLES
	print("creating tables...")
	cur.execute(sql_create_person)
	cur.execute(sql_create_face)
	print("tables created")

def seed_database():
	print("seeding the database...")
	current_data = query_person_faces()
	if (len(current_data) == 0):
		cur.execute("INSERT INTO PERSON(Name) VALUES ('Trump')")
		cur.execute("INSERT INTO PERSON(Name) VALUES ('Obama')")
		cur.execute("INSERT INTO PERSON(Name) VALUES ('Biden')")
		cur.execute("INSERT INTO FACE(PersonID,filename) VALUES (1,'trump.jpeg')")
		cur.execute("INSERT INTO FACE(PersonID,filename) VALUES (2,'obama.jpeg')")
		cur.execute("INSERT INTO FACE(PersonID,filename) VALUES (2,'obama_smile.jpeg')")
		cur.execute("INSERT INTO FACE(PersonID,filename) VALUES (3,'biden.jpeg')")
		conn.commit()
		print("seeding done")
	else:
		print("database already seeded")
	

def query_person_faces():
	persons = []
	for row in cur.execute('SELECT * from PERSON;'):
		persons.append(row)
	
	data = []
	for p in persons:
		faces = []
		for row in cur.execute('SELECT filename FROM FACE WHERE PersonID = ?',str(p[0])):
			faces.append(row[0])
		person = {
			"name" : p[1],
			"faces" : faces
		}
		data.append(person)
	return data

def query_all_faces():
	persons = []
	for row in cur.execute('SELECT PERSON.Name, FACE.filename from PERSON,FACE WHERE PERSON.PersonID = FACE.PersonID;'):
		person = {
			"name": row[0],
			"face": row[1]
		}
		persons.append(person)

	return persons	

def insert_face(name,filename):
	cur.execute('INSERT INTO PERSON(Name) VALUES (?)',(name,))
	conn.commit()
	cur.execute("SELECT * FROM PERSON WHERE Name = ?",(name,))
	person = cur.fetchall()[0]
	cur.execute('INSERT INTO FACE(PersonID,filename) VALUES(?,?)',(person[0],filename,))
	conn.commit()

def drop_tables():
	print("dropping databases")
	cur.execute("DROP TABLE IF EXISTS PERSON")
	cur.execute("DROP TABLE IF EXISTS FACE")
	print("databases dropped")

def init():
	#drop_tables()
	create_table()
	seed_database()


def close():
	conn.close()

