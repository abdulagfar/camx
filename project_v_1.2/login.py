from tkinter import *
import tkinter.messagebox as tm


class Login(Frame):
    def __init__(self):
        self.login=False
    def login_ui(self):
        self.root=Tk()
        self.root.title("Login")
        # img = Image("photo", file='/home/agfar/Desktop/project/project_v_1.2/login.png')
        # self.root.tk.call('wm','iconphoto',self.root._w, img)
        # self.root.iconbitmap("icon.ico")

        
        self.label_username = Label(self.root, text="Username")
        self.label_password = Label(self.root, text="Password")

        self.entry_username = Entry(self.root)
        self.entry_password = Entry(self.root, show="*")

        self.label_username.pack()
        self.entry_username.pack()
        self.label_password.pack()
        self.entry_password.pack()


        self.logbtn = Button(self.root, text="Login", command=self._login_btn_clicked)
        self.logbtn.pack()

      
        self.root.mainloop()
    def _login_btn_clicked(self):
        # print("Clicked")
        username = self.entry_username.get()
        password = self.entry_password.get()

        # print(username, password)

        if username == "admin" and password == "123":
            self.login=True
            self.root.destroy()
            
        else:
            tm.showerror("Login error", "Incorrect username")





