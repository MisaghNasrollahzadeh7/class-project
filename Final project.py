
import tkinter
import sqlite3
import json
from Fusers import *
#------------------------------------MAIN---------------------------------
win=tkinter.Tk()
win.title("Login Panel")
win.geometry("450x450")
win.configure(bg='light blue')
lblUser=tkinter.Label(win,text="username:",font="tahoma,bold 20",fg="black",bg="light blue")
lblUser.pack()
txtUser=tkinter.Entry(win,width=40,highlightthickness=4,highlightcolor='black')
txtUser.pack()
lblPass=tkinter.Label(win,text="password:",font="tahoma,bold 20",fg="black",bg="light blue")
lblPass.pack()
txtPass=tkinter.Entry(win,width=40,highlightthickness=4,highlightcolor='black')
txtPass.pack()
lblMsg=tkinter.Label(win,text="",bg="light blue")
lblMsg.pack()
btnLogin=tkinter.Button(win,text="Login",font="tahoma,bold 16",width=8,bg="black",fg="orange",
                        command=lambda: Login(txtPass,txtUser,lblMsg,btnLogin,btnshop,btncart))
btnLogin.pack()
btnSignup=tkinter.Button(win,text="Signup",font="tahoma,bold 16",width=8,bg="black",fg="orange",
                         command=signup)
btnSignup.pack()
btnshop=tkinter.Button(win,text="shop",font="tahoma,bold 16",width=8,bg="black",fg="orange",
                       command=shop,state='disabled')
btnshop.pack()
btncart=tkinter.Button(win,text="shopping cart",font="tahoma,bold 16",width=16,bg="black",fg="orange",
                       command=showcart,state='disabled')
btncart.pack()
btnadmin=tkinter.Button(win,text="ADMIN",font="bold 20",width=16,bg="black",fg="red",command=admin)
btnadmin.pack()
win.mainloop()
















