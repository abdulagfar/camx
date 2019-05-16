#!/usr/bin/env python3
from tkinter import *
import cv2
import PIL.Image, PIL.ImageTk
import time
from multiprocessing import Process
from datetime import datetime
from face import face_detection
import sent
import threading
import time
import sub
import face_recognition
from tkinter import filedialog
import tkinter.messagebox as tm
from login import Login
import os
class App:
    def __init__(self, window_title,video_source):
        # alert system thread initilzayions
       self.login=Login()
       self.face=face_detection()
       self.initial_time1=0
       self.initial_time2=0
       self.t1=0
       self.t2=0
       self.interval = 1
       self.filename=''
       thread = threading.Thread(target=self.run, args=())
       thread.daemon = True
       thread.start()
       self.thread_path=threading.Thread(target=self.path,args=())
       self.thread_path.deamon=True
       
#*********** window initial ********************************
       self.window = Tk()
       self.window.title(window_title)
       img = Image("photo", file='/home/agfar/Desktop/project/project_v_1.2/icon.png')
       self.window.tk.call('wm','iconphoto',self.window._w, img)
#***************toolbar*********************************
       
       self.toolbar=Frame(self.window)
       self.ck_box2=IntVar()
       self.ck1=Checkbutton(self.toolbar,text="CAM02",font = "Helvetica 12 bold italic",variable=self.ck_box2)
       self.ck1.pack(side=RIGHT)
       self.toolbar.pack(side=TOP,fill=X)
       self.ck_box1=IntVar()
       self.ck1=Checkbutton(self.toolbar,text="CAM01",font = "Helvetica 12 bold italic",variable=self.ck_box1)
       self.ck1.pack(side=RIGHT)
       self.alert=Label(self.toolbar,text="Alert System : ",font = "Helvetica 14 bold italic",fg='black')
       self.alert.pack(side=RIGHT)

       self.log2_butt=Button(self.toolbar,text="Login" ,command=self.login.login_ui)
       self.log2_butt.pack(side=LEFT)
       self.log_butt=Button(self.toolbar,text="Logout" ,command=self.logout)
       self.log_butt.pack(side=LEFT)
       self.p_butt=Button(self.toolbar,text="get path" ,command=self.path)
       self.p_butt.pack(side=LEFT)
       self.footage_butt=Button(self.toolbar,text="View Footages" ,command=self.footage)
       self.footage_butt.pack(side=LEFT)
       
#******************opencv stuffs****************************
       self.video_source = video_source
       self.vid0 = cv2.VideoCapture(0)
       self.vid1 = cv2.VideoCapture(1)
       self.time =datetime.now().replace(microsecond=0)
       self.fourcc1 = cv2.VideoWriter_fourcc(*'XVID')
       self.out1=cv2.VideoWriter("/home/agfar/Desktop/project/project_v_1.1/footage/cam01/"+str(self.time)+".avi",self.fourcc1,20.0,(640,480))
       self.fourcc2 = cv2.VideoWriter_fourcc(*'XVID')
       self.out2=cv2.VideoWriter("/home/agfar/Desktop/project/project_v_1.1/footage/cam02/"+str(self.time)+".avi",self.fourcc2,20.0,(640,480))

        
    #    if not self.vid0.isOpened():
    #        raise ValueError("Unable to open video source", 0)
       
#**************video space in tkinter***************************************
       self.width = self.vid0.get(cv2.CAP_PROP_FRAME_WIDTH)
       self.height = self.vid0.get(cv2.CAP_PROP_FRAME_HEIGHT)
       self.canvas = Canvas(self.window, width = self.width, height =self.height)
       self.canvas2 = Canvas(self.window, width = self.width, height =self.height )
       self.canvas.pack(side="left",fill=X)
       self.canvas2.pack(side="left",fill=X)




       self.delay = 5
       self.update()      
       
       self.window.mainloop()


  #*******************path disply*************************************     

    def path(self):
        if self.login.login==True:
            self.filename =  filedialog.askopenfilename(initialdir = "",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
            self.face.path(self.filename)
        else:
            tm.showerror("Login error", "need to login to view path")
            self.login.login_ui()




#********** footage display************************************
    def footage(self):
        if self.login.login==True:
            os.system('xdg-open "%s"' %'footage')
        else:
            tm.showerror("Login error", "need to login to view footage")
            self.login.login_ui()

        

    def thrd(self):

        
        self.thread_path.start()




    def run(self):
    #**************alert system thread**********************************88
        while True:
            if(self.t1!=self.initial_time1 and self.ck_box1.get()==1):
                sent.SendMail("alert_img/img1.jpg")
                self.t1=self.initial_time1
            if(self.t2!=self.initial_time2 and self.ck_box2.get()==1):
                sent.SendMail("alert_img/img2.jpg")
                self.t2=self.initial_time2
            time.sleep(self.interval)
            



    def update(self):
        # Get a frame from the video source
        
        ret0, frame0,frame1 = self.get_frame()
       

        if ret0:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame0))
            self.photo2 = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame1))
            self.canvas.create_image(0, 0, image = self.photo, anchor = NW)
            self.canvas2.create_image(0, 0, image = self.photo2, anchor = NW)

        self.window.after(self.delay, self.update)







#log out from the user
    def logout(self):
        self.login.login=False
    

        

    def get_frame(self):
        if self.vid0.isOpened():
            ret0, frame0 = self.vid0.read()
            ret1, frame1 = self.vid1.read()
            date=datetime.now().replace(microsecond=0)
            if ret0:
                #put text on each frame
                cv2.putText(frame0,str(date),(385,20), cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(2,36,85),2)
                cv2.putText(frame1,str(date),(385,20), cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(2,36,85),2)
                cv2.putText(frame0,"CAM 01",(20,20), cv2.FONT_HERSHEY_TRIPLEX,.7,(0,0,0),2)
                cv2.putText(frame1,"CAM 02",(20,20), cv2.FONT_HERSHEY_TRIPLEX,.7,(0,0,0),2)
                self.initial_time1,self.initial_time2=self.face.face_rec(frame0,frame1,self.initial_time1,self.initial_time2)
                # store video frame by frame
                self.out1.write(frame0)
                self.out2.write(frame1)

                # Return a boolean success flag and the current frame converted to BGR
                return (ret0, cv2.cvtColor(frame0, cv2.COLOR_BGR2RGB),cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB))
            else:
                return (ret0, None,None)
        else:
            return (ret0, None,None)
    
       

        
     

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid0.isOpened():
            self.vid0.release()
            self.vid1.release()

def run ():
    App( "FACE RECOGNITION IN REAL-WORLD SURVEILLANCE VIDEOS WITH DEEP LEARNING METHODS",0)

    

