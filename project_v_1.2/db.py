import mysql.connector
from datetime import datetime
import re
import matplotlib.pyplot as plt
class pathdb:
    def __init__(self):
        self.db=mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="project"
            )
        self.c =self.db.cursor()
        self.sqlcommand="insert into path values(%s,%s,%s,%s)"
        
        
    def add_time(self,id,cam):
        # print("in add time")
        # self.cam=str(cam)
        minute=0
        self.id=id
        self.c.execute("select min from path where id=%s and cam=%s order by time desc",(self.id,cam))
        initial_time=self.c.fetchall()
        if initial_time:
            minute =initial_time[0][0] 
             
        new_time=datetime.now().replace(microsecond=0)  
        if not(int(minute)==int(new_time.minute)):
            self.entry=(self.id,str(cam),str(new_time),new_time.minute)
            self.c.execute(self.sqlcommand,self.entry)
            self.db.commit()
            print("/////////////////////////////////////////////////////////////////////////////////////")
            print(f"id : {self.id} detected in {cam} and is added to database with time : {new_time} ")
            
    def get_path(self,id):
        self.c.execute(f"select * from path where id={id}")
        data=self.c.fetchall()
        x=[]
        y=[]
        for d in data:
            x.append(d[2])
            y.append(d[1])
        
        plt.plot(x, y,".-")
        plt.xticks(rotation=90)
        # plt.annotate(str(y),x,y)
        plt.show()



            
    
