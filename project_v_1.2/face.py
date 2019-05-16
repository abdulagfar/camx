#video capturing and facerecognition module

import face_recognition
import cv2 
import os
from face_recognition.face_recognition_cli import image_files_in_folder
import db 
import datetime
from multiprocessing import Process
from tkinter import filedialog
import tkinter

class face_detection:
    def __init__(self):
        self.db=db.pathdb()
        my_dir = '/home/agfar/Desktop/project/project_v_1.1/img_db/'
        self.known_face_encodings = []
        self.known_face_names = []
        image_database=os.listdir(my_dir)
        image_database.sort()
        print("read and encode all the images .which are allready in database")
        for i in image_database:
            print(i)
            image = my_dir + i
            image = face_recognition.load_image_file(image)
            try:
                loc=face_recognition.face_locations(image)
                image_encoding = face_recognition.face_encodings(image,loc)[0]
                self.known_face_encodings.append(image_encoding)
                self.known_face_names.append(str(i[:-4]))
            except Exception:
                print(f"error in{i}")


    def face_rec(self,frame0,frame1,initial_time1,initial_time2):
                f1=frame0
                f2=frame1
                t=datetime.datetime.now()
                process_this_frame = True

                small_frame0 = cv2.resize(frame0, (0, 0), fx=0.25, fy=0.25)
                small_frame1 = cv2.resize(frame1, (0, 0), fx=0.25, fy=0.25)

                frame0 = small_frame0[:, :, ::-1]
                frame1 = small_frame1[:, :, ::-1]

                if process_this_frame:
                    #cheking the frame whether a face is enconderd
                    face_locations0 = face_recognition.face_locations(frame0)
                    face_encodings0 = face_recognition.face_encodings(frame0, face_locations0)
                    face_locations1 = face_recognition.face_locations(frame1)
                    face_encodings1 = face_recognition.face_encodings(frame1, face_locations1)

                    if not face_locations0:
                        pass
                        # print("no face IN CAM 1")
                    else:
                        if (abs(t.minute-initial_time1)>1):
                            initial_time1=t.minute
                            cv2.imwrite('/home/agfar/Desktop/project/project_v_1.1/alert_img/img1.jpg',f1)

                    if not face_locations1:
                        pass
                        # print("no face IN CAM 2")
                    else:
                        if (abs(t.minute-initial_time2)>1):
                            initial_time2=t.minute
                            cv2.imwrite('/home/agfar/Desktop/project/project_v_1.1/alert_img/img2.jpg',f2)
                    
#***************database related to path****************************
                    self.encode(face_encodings0,face_locations0,f1,"cam01")
                    self.encode(face_encodings1,face_locations1,f2,"cam02")
                    

                    
                return initial_time1,initial_time2;



    def encode(self,face_encodings,face_locations,frame,cam):
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"
    
            if True in matches:
                first_match_index = matches.index(True)
                name = self.known_face_names[first_match_index]
                self.db.add_time(int(name),cam)
                # print(f"{name} added")
                
                
            else:
                for (top, right, bottom, left)in face_locations:
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4
                    name=int(self.known_face_names[-1])+1
                    crop=frame[(top-50):(bottom+50),(left-50):(right+50)]
                    cv2.imwrite("/home/agfar/Desktop/project/project_v_1.1/img_db/"+str(name)+".jpg",crop)
                    self.known_face_names.append(str(name))
                    self.known_face_encodings.append(face_encoding)
                    self.db.add_time(name,cam)
                    # print(f"{name} added(new)")

    def path(self,filename):
        name="unknown"
        known_face_names=self.known_face_names
        known_face_encodings=self.known_face_encodings
        face_to_find_path=cv2.imread(filename)
        face_locations = face_recognition.face_locations(face_to_find_path)
        face_encodings = face_recognition.face_encodings(face_to_find_path, face_locations)
        matches=[]
        for face_encoding in face_encodings:
                matches=face_recognition.compare_faces(known_face_encodings, face_encoding)
                name="unknown"
                
                print(matches)
        if True in matches:
                first_match_index = matches.index(True)
                name = str(known_face_names[first_match_index])
        if name!="unknown":
            try:
                self.db.get_path(name)
            except Exception:
                print("error") 
        else:
            print("not avilable")  
