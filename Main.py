import customtkinter as ctk
import tkinter
import json
import os
import sys
from time import sleep
import bcrypt
import ctypes
from tkinter import font as tkFont
#----------loading saved usernames/passwords----->

file_path = '.\Profiles.json'

if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
    with open(file_path, "r") as f:
        users = json.load(f)
else:
    users = {}

#----------Functions----->

ctk.set_appearance_mode("dark")
authenticated = False

def home_package():
    setting_page.pack_forget()
    About_page.pack_forget()
    home_page.pack(anchor="e",fill="both", expand=True)

def About_package():
    if authenticated == True:
        setting_page.pack_forget()
        home_page.pack_forget()
        About_page.pack(fill="both", expand=True)
    else:
        sign_error.configure(text="Please Sign Up/Login first!",text_color="red")
        login_error.configure(text="Please Sign Up/Login first!",text_color="red")

def setting_package():
    if authenticated == True:
        home_page.pack_forget()
        About_page.pack_forget()
        setting_page.pack(fill="both", expand=True)
    else:
        sign_error.configure(text="Please Sign Up/Login first!",text_color="red")
        login_error.configure(text="Please Sign Up/Login first!",text_color="red")
        
#----------Sign Up && Login functionality------>

def sign_in():
    global users, authenticated
    user = sign_user.get()
    password = sign_pass.get()
    if user in users:
        sign_error.configure(text="User already exists",text_color="red")
        sign_user.focus()
        return
    elif user == "":
        sign_error.configure(text="Please enter a username",text_color="red")
        sign_user.focus()
        return
    elif password == "":
        sign_error.configure(text="Please enter a password",text_color="red")
        sign_pass.focus()
        return
    elif user == password:
        sign_error.configure(text="Username and password cannot be the same",text_color="red")
        sign_user.focus()
        return
    elif len(user) < 4:
        sign_error.configure(text="Username must be at least 4 characters long",text_color="red")
        sign_user.focus()
        return
    elif len(password) < 8:
        sign_error.configure(text="Password must be at least 8 characters long",text_color="red")
        sign_pass.focus()
        return
    elif not any(char in "!@#$%^&*()_+-=[]{}|:;'\"<>,./?~" for char in password):
        sign_error.configure(text="Password must contain at least one special character",text_color="red")
        sign_pass.focus()
        return
    elif not any(char.isdigit() for char in password):
        sign_error.configure(text="Password must contain at least one number",text_color="red")
        sign_pass.focus()
        return
    elif not any(char.isupper() for char in password):
        sign_error.configure(text="Password must contain at least one uppercase letter",text_color="red")
        sign_pass.focus()
        return
    elif not any(char.islower() for char in password):
        sign_error.configure(text="Password must contain at least one lowercase letter",text_color="red")
        sign_pass.focus()
        return
    else:
        hashed_pass = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
        users[user] = hashed_pass.decode('utf-8')
        with open(file_path, "w") as f:
            json.dump(users, f, indent=4)
        sign_content.pack_forget()
        authenticated = True

show = False

def show_pass():
    global show
    if show == False:
        sign_pass.configure(show="")
        login_pass.configure(show="")
        show = True
        pass_show_button.configure(text="👁")
        show_button.configure(text="👁")
    elif show == True:
        sign_pass.configure(show="*")
        login_pass.configure(show="*")
        show = False
        show_button.configure(text="🙈")
        pass_show_button.configure(text="🙈")

def login():
    global users, authenticated
    user = login_user.get()
    pw = login_pass.get()
    if user in users:
        stored_hash = users[user].encode('utf-8')
        if bcrypt.checkpw(pw.encode('utf-8'), stored_hash):
            login_content.pack_forget()
            authenticated = True
        else:
            login_error.configure(text="Invalid username or password",text_color="red")
            login_user.focus()
            return
    else:
        login_error.configure(text="Invalid username or password",text_color="red")
        return

def login_package():
    pass_show_button.pack_forget()
    show_button.pack()
    sign_content.pack_forget()
    login_content.pack(pady=(50,0))

def sign_package():
    show_button.pack_forget()
    pass_show_button.pack()
    login_content.pack_forget()
    sign_content.pack(pady=(50,0))

def custom_label(master, **kwargs):
    return ctk.CTkLabel(master,font=custom_font, **kwargs)

def custom_button(master, **kwargs):
    return ctk.CTkButton(master,font=custom_font2, **kwargs)

#---------Main App----->

app = ctk.CTk()
app.title('app?? I guess?')
app.geometry('700x650')

#----------Loading Fonts----->

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(".")

font_path = os.path.join(base_path, "App", "Outfit-Medium.ttf")

if sys.platform == "win32":
    ctypes.windll.gdi32.AddFontResourceExW(font_path, 0x10, 0)

font_family = "Outfit Medium"  

custom_font = ctk.CTkFont(family=font_family,size=30)
custom_font2 = ctk.CTkFont(family=font_family,size=14)
#-------------------Side bar----->

sidebar_page = ctk.CTkFrame(app,fg_color="#525362",corner_radius=0)
sidebar_page.pack(side="left",fill="y")

home_button = custom_button(sidebar_page,text="Home",fg_color="#9FA9AF",command=home_package)
home_button.pack(padx=5,pady=4)

setting_button = custom_button(sidebar_page,text="Setting",fg_color="#9FA9AF",command=setting_package)
setting_button.pack(padx=5,pady=4)

about_button = custom_button(sidebar_page, text="About",fg_color="#9FA9AF",command=About_package)
about_button.pack(padx=5,pady=4)


#----------------------Pages----->

#--------Home Page----->
home_page = ctk.CTkFrame(app,fg_color="#323342",corner_radius=0)
home_page.pack(fill="both",expand=True)

home_label = custom_label(home_page,text="Welcome to  Home Page")
home_label.pack(pady=(100,0))

#--------Settings Page----->

setting_page = ctk.CTkFrame(app,fg_color="#323342",corner_radius=0)

setting_label = custom_label(setting_page,text="Welcome to  Setting Page")
setting_label.pack(pady=(100,0))

#--------About Page----->

About_page = ctk.CTkFrame(app,fg_color="#323342",corner_radius=0)

about_label = custom_label(About_page,text="Welcome to  About Page")
about_label.pack(pady=(100,0))

#--------Sign Up Content----->

sign_content = ctk.CTkFrame(home_page,fg_color="#3A0A44",corner_radius=20)
sign_content.pack(pady=(50,0))

sign_label = ctk.CTkLabel(sign_content,font=("Georgia",20),text="Sign Up")
sign_label.pack(padx=70,pady=(45,5))

sign_user = ctk.CTkEntry(sign_content, placeholder_text="Username",fg_color="#545584",width=180,height=33,font=custom_font2
                         ,justify="center",placeholder_text_color="#7677A6",border_width=0,text_color="black")
sign_user.pack(padx=70,pady=(55,0))

sign_error = ctk.CTkLabel(sign_content,text="",font=("Outfit Medium",14),text_color="red")
sign_error.pack(pady=1)

pass_container = ctk.CTkFrame(sign_content,width=320,height=33,fg_color="#3A0A44",border_width=0)
pass_container.pack(padx=(35,0))

sign_pass = ctk.CTkEntry(pass_container, placeholder_text="Password",width=180,height=33,fg_color="#545584",show="*",font=custom_font2
                         ,justify="center",placeholder_text_color="#7677A6",border_width=0,text_color="black",)
sign_pass.pack(side="left")

pass_show_button = ctk.CTkButton(pass_container,text="🙈",font=("arial",20),width=10,height=10,fg_color="transparent",hover=False,command=show_pass,anchor="e")
pass_show_button.pack()

sign_button = custom_button(sign_content,text="Sign Up",command=sign_in)
sign_button.pack(pady=(70,30))

login_option = custom_button(sign_content,text="Already have an account? Login here",text_color="white",fg_color="transparent",hover=False,command=login_package)
login_option.pack(pady=(10,25))

#--------Log In Content----->

login_content = ctk.CTkFrame(home_page,fg_color="#3A0A44",corner_radius=20)


login_label = ctk.CTkLabel(login_content,font=("Georgia",20),text="Log In")
login_label.pack(padx=70,pady=(45,5))

login_user = ctk.CTkEntry(login_content, placeholder_text="Username",fg_color="#545584",width=180,height=33,font=custom_font2
                         ,justify="center",placeholder_text_color="#7677A6",border_width=0,text_color="black")
login_user.pack(padx=70,pady=(55,0))

login_error = ctk.CTkLabel(login_content,text="",font=("Outfit Medium",14),text_color="red")
login_error.pack(pady=1)

pass_container = ctk.CTkFrame(login_content,width=320,height=33,fg_color="#3A0A44",border_width=0)
pass_container.pack(padx=(35,0))

login_pass = ctk.CTkEntry(pass_container, placeholder_text="Password",fg_color="#545584",width=180,height=33,show="*",font=custom_font2
                         ,justify="center",placeholder_text_color="#7677A6",border_width=0,text_color="black")
login_pass.pack(side="left")

show_button = ctk.CTkButton(pass_container,text="🙈",font=("arial",20),width=10,height=10,fg_color="transparent",hover=False,command=show_pass,anchor="e")
show_button.pack()

login_button = custom_button(login_content,text="Log In",command=login)
login_button.pack(pady=(70,30))

sign_option = custom_button(login_content,text="Don't have an account? Sign up here",text_color="white",fg_color="transparent",hover=False,command=sign_package)
sign_option.pack(pady=(10,25))

app.mainloop()