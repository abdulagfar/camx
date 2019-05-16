import tkinter
from tkinter import filedialog
import cv2
import face_recognition
import db
import os

db=db.pathdb()
my_dir = './img/' 
known_face_encodings = []
known_face_names = []
image_database=os.listdir(my_dir)
image_database.sort()
for i in image_database:
    print(i)
    image = my_dir + i
    image = face_recognition.load_image_file(image)
    image_encoding = face_recognition.face_encodings(image)[0]
    known_face_encodings.append(image_encoding)
    known_face_names.append(str(i[:-4]))
    # print(image_encoding)

filename =  filedialog.askopenfilename(initialdir = "/home/Desktop/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
    
face_to_find_path=cv2.imread(filename)
face_locations = face_recognition.face_locations(face_to_find_path)
face_encodings = face_recognition.face_encodings(face_to_find_path, face_locations)
matches=[]
for face_encoding in face_encodings:
            matches=face_recognition.compare_faces(known_face_encodings, face_encoding)
            name="unknown"
print(matches)
if True in matches:
        # print ("hai")
        first_match_index = matches.index(True)
        name = str(known_face_names[first_match_index])

if name!="unknown":
    db.get_path(name)

            







