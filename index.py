import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import PoseModule as pm
import numpy as np
import sqlite3
from passlib.hash import bcrypt
from datetime import datetime
import re
from database import Database
import io
from tkinter import filedialog
class PersonalAITrainer:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal AI Trainer")
        self.root.geometry('1000x650')
        self.root.state('zoomed')
        self.root.config(background="#eff5f6")
        

        self.detector = pm.poseDetector()
        self.count = 0
        self.dir = 0
        self.exercise_type = None
        self.current_frame = None  # Variable to keep track of the current frame
        self.user = None  # Variable to keep track of the current frame
        
        # Connect to the database
        self.db_instance = Database()
        
        self.home_page()
        
    def register_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        email = self.email_entry.get()
        
        
        hashed_password = bcrypt.hash(password)
        cursor = self.db_instance.db_connection.cursor()
        cursor.execute('''
            SELECT id, password FROM users WHERE username = ?
        ''', (username,))
        user_data = cursor.fetchone()
        
        if  user_data :
            self.error_label.config(text="user already exists")
            self.error_label.place(x=650, y=200)
            print("user already exists")
            return
        
        if self.validate_input(username=username,email=email,password=password):
            
            cursor = self.db_instance.db_connection.cursor()
            hashed_password = bcrypt.hash(password)
            cursor.execute('''
                INSERT INTO users (username, password, email) VALUES (?, ?, ?)
            ''', (username, hashed_password, email))
            self.db_instance.db_connection.commit()
            self.error_label.config(bg='green',text="registered Successfully")
            print("registered Successfully")
            
            user_id = self.authenticate_user(username, password)

            if user_id:
                print(f"User {username} logged in.")
                self.user = {'id': user_id, 'username': username}
                self.db_instance.update_profile_image(self.user['id'],"images/user-default.png")
                self.delete_page()
                self.home_page()
    
    def authenticate_user(self, username, password):
        cursor = self.db_instance.db_connection.cursor()
        cursor.execute('''
            SELECT id, password FROM users WHERE username = ?
        ''', (username,))
        user_data = cursor.fetchone()
        if user_data and bcrypt.verify(password, user_data[1]):
            return user_data[0]
        return None
    
    def login_page1(self):
        # ========================================================================
        # ============================background image============================
        # ========================================================================
        self.bg_frame = Image.open('images/background.jpg')
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = Label(self.root, image=photo)
        self.bg_panel.image = photo
        self.bg_panel.pack(fill='both', expand='yes')
        # ====== Login Frame =========================
        self.lgn_frame = Frame(self.root, bg='#040405', width=950, height=600)
        self.lgn_frame.place(x=200, y=30)

        # ========================================================================
        # ========================================================
        # ========================================================================
        self.txt = "WELCOME"
        self.heading = Label(self.lgn_frame, text=self.txt, font=('yu gothic ui', 25, "bold"), bg="#040405",
                             fg='white',
                             bd=5,
                             relief=FLAT)
        self.heading.place(x=80, y=30, width=300, height=30)

        # ========================================================================
        # ============ Left Side Image ================================================
        # ========================================================================
        self.side_image = Image.open('images/vector1.png')
        photo = ImageTk.PhotoImage(self.side_image)
        self.side_image_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.side_image_label.image = photo
        self.side_image_label.place(x=5, y=100)

        # ========================================================================
        # ============ Sign In Image =============================================
        # ========================================================================
        self.sign_in_image = Image.open('images/hyy.png')
        photo = ImageTk.PhotoImage(self.sign_in_image)
        self.sign_in_image_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.sign_in_image_label.image = photo
        self.sign_in_image_label.place(x=620, y=130)

        # ========================================================================
        # ============ Sign In label =============================================
        # ========================================================================
        self.sign_in_label = Label(self.lgn_frame, text="Sign In", bg="#040405", fg="white",
                                    font=("yu gothic ui", 17, "bold"))
        self.sign_in_label.place(x=650, y=240)
        
        # ========================================================================
        # ============ Error label =============================================
        # ========================================================================
        self.error_label = Label(self.lgn_frame, text="", bg="#040405", fg="red",
                                    font=("yu gothic ui", 10, "bold"))
        self.error_label.place(x=600, y=270)
        

        # ========================================================================
        # ============================username====================================
        # ========================================================================
        self.username_label = Label(self.lgn_frame, text="Username", bg="#040405", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.username_label.place(x=550, y=300)

        self.username_entry = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#6b6a69",
                                    font=("yu gothic ui ", 12, "bold"), insertbackground = '#6b6a69')
        self.username_entry.place(x=580, y=335, width=270)

        self.username_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.username_line.place(x=550, y=359)
        # ===== Username icon =========
        self.username_icon = Image.open('images/user.png')
        photo = ImageTk.PhotoImage(self.username_icon)
        self.username_icon_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.username_icon_label.image = photo
        self.username_icon_label.place(x=550, y=332)

        # ========================================================================
        # ============================login button================================
        # ========================================================================
        self.lgn_button = Image.open('images/btn1.png')
        photo = ImageTk.PhotoImage(self.lgn_button)
        self.lgn_button_label = Label(self.lgn_frame, image=photo, bg='#040405')
        self.lgn_button_label.image = photo
        self.lgn_button_label.place(x=550, y=450)
        self.login_button = Button(self.lgn_button_label, text='LOGIN', font=("yu gothic ui", 13, "bold"), width=25, bd=0,
                            bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white',command=lambda: self.login(self.username_entry.get(),self.password_entry.get()))
        self.login_button.place(x=20, y=10)
        # ========================================================================
        # ============================Forgot password=============================
        # ========================================================================
        self.forgot_button = Button(self.lgn_frame, text="Forgot Password ?",
                                    font=("yu gothic ui", 13, "bold underline"), fg="white", relief=FLAT,
                                    activebackground="#040405"
                                    , borderwidth=0, background="#040405", cursor="hand2")
        self.forgot_button.place(x=630, y=510)
        # =========== Sign Up ==================================================
        self.sign_label = Label(self.lgn_frame, text='I haven\'t account ', font=("yu gothic ui", 11, "bold"),
                                relief=FLAT, borderwidth=0, background="#040405", fg='white')
        self.sign_label.place(x=550, y=560)

        self.signup_img = Image.open('images/signup.png').resize((111,35))
        self.signup_img = ImageTk.PhotoImage(self.signup_img)
        self.signup_button_label = Button(self.lgn_frame, image=self.signup_img, bg='#98a65d', cursor="hand2",
                                          borderwidth=0, background="#040405", activebackground="#040405",command=self.show_register_page)
        self.signup_button_label.place(x=670, y=555, width=111, height=35)

        # ========================================================================
        # ============================password====================================
        # ========================================================================
        self.password_label = Label(self.lgn_frame, text="Password", bg="#040405", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.password_label.place(x=550, y=380)

        self.password_entry = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#040405", fg="#6b6a69",
                                    font=("yu gothic ui", 12, "bold"), show="*", insertbackground = '#6b6a69')
        self.password_entry.place(x=580, y=416, width=244)

        self.password_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.password_line.place(x=550, y=440)
        # ======== Password icon ================
        self.password_icon = Image.open('images/password.png')
        photo = ImageTk.PhotoImage(self.password_icon)
        self.password_icon_label = Label(self.lgn_frame, image=photo, bg='#000000')
        self.password_icon_label.image = photo
        self.password_icon_label.place(x=550, y=410)
        # ========= show/hide password ==================================================================
        self.show_image = ImageTk.PhotoImage \
            (file='images\\show1.png')

        self.hide_image = ImageTk.PhotoImage \
            (file='images\\hide1.png')

        self.show_button = Button(self.lgn_frame, image=self.show_image, command=lambda : self.show(self.lgn_frame), relief=FLAT,
                                  activebackground="black"
                                  , borderwidth=0, background="black", cursor="hand2")
        self.show_button.place(x=860, y=420)
    
    def login_page(self):
        # ========================================================================
        # ============================background image============================
        # ========================================================================
        self.bg_frame = Image.open('images/background.jpg')
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = Label(self.root, image=photo)
        self.bg_panel.image = photo
        self.bg_panel.pack(fill='both', expand='yes')
        # ====== Login Frame =========================
        self.lgn_frame = Frame(self.root, bg='#ffffff', width=950, height=600)
        self.lgn_frame.place(x=200, y=30)

        # ========================================================================
        # ========================================================
        # ========================================================================
        self.txt = "WELCOME"
        self.heading = Label(self.lgn_frame, text=self.txt, font=('yu gothic ui', 25, "bold"), bg="#ffffff",
                             fg='black',
                             bd=5,
                             relief=FLAT)
        self.heading.place(x=80, y=30, width=300, height=30)

        # ========================================================================
        # ============ Left Side Image ================================================
        # ========================================================================
        self.side_image = Image.open('images/vector.png')
        photo = ImageTk.PhotoImage(self.side_image)
        self.side_image_label = Label(self.lgn_frame, image=photo, bg='#ffffff')
        self.side_image_label.image = photo
        self.side_image_label.place(x=5, y=100)

        # ========================================================================
        # ============ Sign In Image =============================================
        # ========================================================================
        self.sign_in_image = Image.open('images/hyy.png')
        photo = ImageTk.PhotoImage(self.sign_in_image)
        self.sign_in_image_label = Label(self.lgn_frame, image=photo, bg='#ffffff')
        self.sign_in_image_label.image = photo
        self.sign_in_image_label.place(x=620, y=130)

        # ========================================================================
        # ============ Sign In label =============================================
        # ========================================================================
        self.sign_in_label = Label(self.lgn_frame, text="Sign In", bg="#ffffff", fg="black",
                                    font=("yu gothic ui", 17, "bold"))
        self.sign_in_label.place(x=650, y=240)
        
        # ========================================================================
        # ============ Error label =============================================
        # ========================================================================
        self.error_label = Label(self.lgn_frame, text="", bg="#ffffff", fg="red",
                                    font=("yu gothic ui", 10, "bold"))
        self.error_label.place(x=600, y=270)
        

        # ========================================================================
        # ============================username====================================
        # ========================================================================
        self.username_label = Label(self.lgn_frame, text="Username", bg="#ffffff", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.username_label.place(x=550, y=300)

        self.username_entry = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#ffffff", fg="#000000",
                                    font=("yu gothic ui ", 12), insertbackground = '#6b6a69')
        self.username_entry.place(x=580, y=335, width=270)

        self.username_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.username_line.place(x=550, y=359)
        # ===== Username icon =========
        self.username_icon = Image.open('images/user.png')
        photo = ImageTk.PhotoImage(self.username_icon)
        self.username_icon_label = Label(self.lgn_frame, image=photo, bg='#ffffff')
        self.username_icon_label.image = photo
        self.username_icon_label.place(x=550, y=332)

        # ========================================================================
        # ============================login button================================
        # ========================================================================
        self.lgn_button = Image.open('images/btn1.png')
        photo = ImageTk.PhotoImage(self.lgn_button)
        self.lgn_button_label = Label(self.lgn_frame, image=photo, bg='#ffffff')
        self.lgn_button_label.image = photo
        self.lgn_button_label.place(x=550, y=450)
        self.login_button = Button(self.lgn_button_label, text='LOGIN', font=("yu gothic ui", 13, "bold"), width=25, bd=0,
                            bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white',command=lambda: self.login(self.username_entry.get(),self.password_entry.get()))
        self.login_button.place(x=20, y=10)
        # ========================================================================
        # ============================Forgot password=============================
        # ========================================================================
        self.forgot_button = Button(self.lgn_frame, text="Forgot Password ?",
                                    font=("yu gothic ui", 13, "underline"), fg="black", relief=FLAT,
                                    activebackground="#ffffff"
                                    , borderwidth=0, background="#ffffff", cursor="hand2")
        self.forgot_button.place(x=630, y=510)
        # =========== Sign Up ==================================================
        self.sign_label = Label(self.lgn_frame, text='I haven\'t account ', font=("yu gothic ui", 11, "bold"),
                                relief=FLAT, borderwidth=0, background="#ffffff", fg='black')
        self.sign_label.place(x=590, y=560)

        self.signup_img = Image.open('images/signup.png').resize((111,35))
        self.signup_img = ImageTk.PhotoImage(self.signup_img)
        self.signup_button_label = Button(self.lgn_frame, image=self.signup_img, bg='#98a65d', cursor="hand2",
                                          borderwidth=0, background="#ffffff", activebackground="#ffffff",command=self.show_register_page)
        self.signup_button_label.place(x=720, y=555, width=111, height=35)
        
        

        # ========================================================================
        # ============================password====================================
        # ========================================================================
        self.password_label = Label(self.lgn_frame, text="Password", bg="#ffffff", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.password_label.place(x=550, y=380)

        self.password_entry = Entry(self.lgn_frame, highlightthickness=0, relief=FLAT, bg="#ffffff", fg="#000000",
                                    font=("yu gothic ui", 12), show="*", insertbackground = '#000000')
        self.password_entry.place(x=580, y=416, width=244)

        self.password_line = Canvas(self.lgn_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.password_line.place(x=550, y=440)
        # ======== Password icon ================
        self.password_icon = Image.open('images/password.png')
        photo = ImageTk.PhotoImage(self.password_icon)
        self.password_icon_label = Label(self.lgn_frame, image=photo, bg='#ffffff')
        self.password_icon_label.image = photo
        self.password_icon_label.place(x=550, y=410)
        # ========= show/hide password ==================================================================
        self.show_image = ImageTk.PhotoImage \
            (file='images\\show.png')

        self.hide_image = ImageTk.PhotoImage \
            (file='images\\hide.png')

        self.show_button = Button(self.lgn_frame, image=self.show_image, command=lambda : self.show(self.lgn_frame), relief=FLAT,
                                  activebackground="#ffffff"
                                  , borderwidth=0, background="#ffffff", cursor="hand2")
        self.show_button.place(x=860, y=420)
    
    def register_page(self):
        # ========================================================================
        # ============================background image============================
        # ========================================================================
        self.bg_frame = Image.open('images/background.jpg')
        photo = ImageTk.PhotoImage(self.bg_frame)
        self.bg_panel = Label(self.root, image=photo)
        self.bg_panel.image = photo
        self.bg_panel.pack(fill='both', expand='yes')
        # ====== Login Frame =========================
        self.reg_frame = Frame(self.root, bg='#ffffff', width=950, height=600)
        self.reg_frame.place(x=200, y=30)

        # ========================================================================
        # ========================================================
        # ========================================================================
        self.txt = "WELCOME"
        self.heading = Label(self.reg_frame, text=self.txt, font=('yu gothic ui', 25, "bold"), bg="#ffffff",
                             fg='#000000',
                             bd=5,
                             relief=FLAT)
        self.heading.place(x=80, y=30, width=300, height=30)

        # ========================================================================
        # ============ Left Side Image ================================================
        # ========================================================================
        self.side_image = Image.open('images/vector.png')
        photo = ImageTk.PhotoImage(self.side_image)
        self.side_image_label = Label(self.reg_frame, image=photo, bg='#ffffff')
        self.side_image_label.image = photo
        self.side_image_label.place(x=5, y=100)

        # ========================================================================
        # ============ Sign In Image =============================================
        # ========================================================================
        self.sign_in_image = Image.open('images/hyy.png')
        photo = ImageTk.PhotoImage(self.sign_in_image)
        self.sign_in_image_label = Label(self.reg_frame, image=photo, bg='#ffffff')
        self.sign_in_image_label.image = photo
        self.sign_in_image_label.place(x=620, y=50)

        # ========================================================================
        # ============ Sign In label =============================================
        # ========================================================================
        self.sign_in_label = Label(self.reg_frame, text="Sign Up", bg="#ffffff", fg="#000000",
                                    font=("yu gothic ui", 17, "bold"))
        self.sign_in_label.place(x=650, y=160)
        
        # ========================================================================
        # ============ Error label =============================================
        # ========================================================================
        self.error_label = Label(self.reg_frame, text="", bg="#ffffff", fg="red",
                                    font=("yu gothic ui", 10, "bold"))
        self.error_label.place(x=600, y=200)

        # ========================================================================
        # ============================email=======================================
        # ========================================================================
        self.email_label = Label(self.reg_frame, text="Email", bg="#ffffff", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.email_label.place(x=550, y=220)

        self.email_entry = Entry(self.reg_frame, highlightthickness=0, relief=FLAT, bg="#ffffff", fg="#000000",
                                    font=("yu gothic ui ", 12),insertbackground = '#000000')
        self.email_entry.place(x=580, y=255, width=270)

        self.email_line = Canvas(self.reg_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.email_line.place(x=550, y=279)
        # ===== Username icon =========
        self.email_icon = Image.open('images/email.png')
        photo = ImageTk.PhotoImage(self.email_icon)
        self.email_icon_label = Label(self.reg_frame, image=photo, bg='#ffffff')
        self.email_icon_label.image = photo
        self.email_icon_label.place(x=550, y=252)
        
        # ========================================================================
        # ============================username====================================
        # ========================================================================
        self.username_label = Label(self.reg_frame, text="Username", bg="#ffffff", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.username_label.place(x=550, y=300)

        self.username_entry = Entry(self.reg_frame, highlightthickness=0, relief=FLAT, bg="#ffffff", fg="#000000",
                                    font=("yu gothic ui ", 12), insertbackground = '#000000')
        self.username_entry.place(x=580, y=335, width=270)

        self.username_line = Canvas(self.reg_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.username_line.place(x=550, y=359)
        # ===== Username icon =========
        self.username_icon = Image.open('images/user.png')
        photo = ImageTk.PhotoImage(self.username_icon)
        self.username_icon_label = Label(self.reg_frame, image=photo, bg='#ffffff')
        self.username_icon_label.image = photo
        self.username_icon_label.place(x=550, y=332)

        # ========================================================================
        # ============================login button================================
        # ========================================================================
        self.lgn_button = Image.open('images/btn1.png')
        photo = ImageTk.PhotoImage(self.lgn_button)
        self.lgn_button_label = Label(self.reg_frame, image=photo, bg='#ffffff')
        self.lgn_button_label.image = photo
        self.lgn_button_label.place(x=550, y=450)
        self.register_button = Button(self.lgn_button_label, text='REGISTER', font=("yu gothic ui", 13, "bold"), width=25, bd=0,
                            bg='#3047ff', cursor='hand2', activebackground='#3047ff', fg='white',command=self.register_user)
        self.register_button.place(x=20, y=10)
        # ========================================================================
        # ============================Forgot password=============================
        # ========================================================================
        self.forgot_button = Button(self.reg_frame, text="Forgot Password ?",
                                    font=("yu gothic ui", 13, "underline"), fg="#000000", relief=FLAT,
                                    activebackground="#ffffff"
                                    , borderwidth=0, background="#ffffff", cursor="hand2")
        self.forgot_button.place(x=630, y=510)
        # =========== Sign Up ==================================================
        self.sign_label = Label(self.reg_frame, text='I already have account ', font=("yu gothic ui", 11, "bold"),
                                relief=FLAT, borderwidth=0, background="#ffffff", fg='#000000')
        self.sign_label.place(x=550, y=560)

        self.signup_img = Image.open('images/signin.png').resize((111,35))
        self.signup_img = ImageTk.PhotoImage(self.signup_img)
        self.signup_button_label = Button(self.reg_frame, image=self.signup_img, bg='#98a65d', cursor="hand2",
                                          borderwidth=0, background="#ffffff", activebackground="#ffffff",command=self.show_login_page)
        self.signup_button_label.place(x=720, y=555, width=111, height=35)
        

        # ========================================================================
        # ============================password====================================
        # ========================================================================
        self.password_label = Label(self.reg_frame, text="Password", bg="#ffffff", fg="#4f4e4d",
                                    font=("yu gothic ui", 13, "bold"))
        self.password_label.place(x=550, y=380)

        self.password_entry = Entry(self.reg_frame, highlightthickness=0, relief=FLAT, bg="#ffffff", fg="#000000",
                                    font=("yu gothic ui", 12), show="*", insertbackground = '#000000')
        self.password_entry.place(x=580, y=416, width=244)

        self.password_line = Canvas(self.reg_frame, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.password_line.place(x=550, y=440)
        # ======== Password icon ================
        self.password_icon = Image.open('images/password.png')
        photo = ImageTk.PhotoImage(self.password_icon)
        self.password_icon_label = Label(self.reg_frame, image=photo, bg='#ffffff')
        self.password_icon_label.image = photo
        self.password_icon_label.place(x=550, y=410)
        # ========= show/hide password ==================================================================
        self.show_image = ImageTk.PhotoImage \
            (file='images\\show.png')

        self.hide_image = ImageTk.PhotoImage \
            (file='images\\hide.png')

        self.show_button = Button(self.reg_frame, image=self.show_image, command=lambda: self.show(self.reg_frame), relief=FLAT,
                                  activebackground="#ffffff"
                                  , borderwidth=0, background="#ffffff", cursor="hand2")
        self.show_button.place(x=860, y=420)
    
    def show(self,page,password_entry=None):
        if password_entry is not None:
            self.hide_button = Button(page, image=self.hide_image, command=lambda : self.hide(page,password_entry), relief=FLAT,
                                  activebackground="#ffffff"
                                  , borderwidth=0, background="#ffffff", cursor="hand2")
            password_entry.winfo_x()
            self.hide_button.place(x=850,y=password_entry.winfo_y()+10)
            password_entry.config(show='')
            return
            
        self.hide_button = Button(page, image=self.hide_image, command=lambda : self.hide(page), relief=FLAT,
                                  activebackground="#ffffff"
                                  , borderwidth=0, background="#ffffff", cursor="hand2")
        self.hide_button.place(x=860, y=420)
        self.password_entry.config(show='')

    def hide(self,page,password_entry=None):
        if password_entry is not None:
            self.show_button = Button(page, image=self.show_image, command=lambda : self.show(page,password_entry), relief=FLAT,
                                  activebackground="white"
                                  , borderwidth=0, background="white", cursor="hand2")
            self.show_button.place(x=850,y=password_entry.winfo_y()+10)
            password_entry.config(show='*')
            return
        
        self.show_button = Button(page, image=self.show_image, command=lambda: self.show(page), relief=FLAT,
                                  activebackground="#ffffff"
                                  , borderwidth=0, background="#ffffff", cursor="hand2")
        self.show_button.place(x=860, y=420)
        self.password_entry.config(show='*')

    def show_register_page(self):
        self.delete_page()
        self.register_page()

    def logout(self):
        # Perform any necessary logout actions
        self.user = None  # Clear the user data
        self.show_home_page()  # Redirect to the home page after logout
    
    def login(self,username,password):
        username = username
        password = password
        
        user_id = self.authenticate_user(username, password)

        if user_id:
            print(f"User {username} logged in.")
            self.user = {'id': user_id, 'username': username}
            self.delete_page()
            self.home_page()
        else:
            self.error_label.config(text="Invalid credentials! Please try again.")
            print("Invalid credentials. Please try again.")
                        
    def show_login_page(self):
        self.delete_page()
        self.login_page()
         
    def common_page(self):
        
        # ======================= Header ===================== #
        self.header = Frame(self.root,bg='#009df4')
        self.header.place(x=300,y=0,width=1070, height=60)
        
        
        self.logout_text = Button(self.header,text='Logout',bg='#32cf8e',font=("",13,"bold"),
                                  bd=0, fg ='white', cursor="hand2",activebackground="#32cf8e",command=self.logout)
        self.logout_text.place(x=900 , y= 15)
        # ===================================================== #
        
        # ==================== Sidebar ======================= #
        self.sidebar = Frame(self.root, bg='#ffffff',)
        self.sidebar.place(x = 0, y=0, width=300 , height=700)
        
        # Logo 
        self.logoImage = Image.open('images\\logo.png').resize((200,200))
        photo = ImageTk.PhotoImage(self.logoImage)
        self.logo = Label(self.sidebar, image=photo,bg='#ffffff')
        self.logo.image = photo
        self.logo.place(x=40,y=50)
        
        
        # User Name
        self.name = Label(self.sidebar,text=' Welcome !! '+self.user['username'], bg ="#ffffff",font=("",15,"bold"))
        self.name.place(x=10,y=10)
        
        #Dashboard
        self.dashboardImage = Image.open('images\\dashboard-icon.png')
        photo = ImageTk.PhotoImage(self.dashboardImage)
        self.dashboard = Label(self.sidebar, image=photo,bg='#ffffff')
        self.dashboard.image = photo
        self.dashboard.place(x=35,y=250)
        
        self.dashboard_text = Button(self.sidebar,text='Dashboard',bg = "#ffffff",font=("",13,"bold"),bd=0,cursor='hand2',activebackground="#ffffff",activeforeground="#0064d3",command=lambda:self.indicate(self.dashboard_indicator,self.home_page))
        self.dashboard_text.place(x=80,y= 250)
        # indicator
        self.dashboard_indicator = Label(self.sidebar,text=" ",bg='#ffffff')
        self.dashboard_indicator.place(x = 10,y=250,width = 5,height=30)
        
        #start
        self.startImage = Image.open('images\\start-icon.png')
        photo = ImageTk.PhotoImage(self.startImage)
        self.start = Label(self.sidebar, image=photo,bg='#ffffff')
        self.start.image = photo
        self.start.place(x=30,y=290)
        
        self.start_text = Button(self.sidebar,text='Start Exercise',bg = "#ffffff",font=("",13,"bold"),bd=0,cursor='hand2',activebackground="#ffffff",activeforeground="#0064d3",command=lambda:self.indicate(self.start_indicator,self.choose_exercise_page))
        self.start_text.place(x=80,y= 290)
        
        self.start_indicator = Label(self.sidebar,text=" ",bg='#ffffff')
        self.start_indicator.place(x = 10,y=290,width = 5,height=30)
        
        #Update Profile
        self.updateProfileImage = Image.open('images\\settings-icon.png')
        photo = ImageTk.PhotoImage(self.updateProfileImage)
        self.updateProfile = Label(self.sidebar, image=photo,bg='#ffffff')
        self.updateProfile.image = photo
        self.updateProfile.place(x=35,y=330)
        
        self.updateProfile_text = Button(self.sidebar,text='Update Profile',bg = "#ffffff",font=("",13,"bold"),bd=0,cursor='hand2',activebackground="#ffffff",activeforeground="#0064d3",command=lambda:self.indicate(self.updateProfile_indicator,self.update_profile_page))
        self.updateProfile_text.place(x=80,y= 330)
        
        self.updateProfile_indicator = Label(self.sidebar,text=" ",bg='#ffffff')
        self.updateProfile_indicator.place(x = 10,y=330,width = 5,height=30)
        
        # Exit
        self.exitImage = Image.open('images\\exit-icon.png')
        photo = ImageTk.PhotoImage(self.exitImage)
        self.exit = Label(self.sidebar, image=photo,bg='#ffffff')
        self.exit.image = photo
        self.exit.place(x=35,y=370)
        
        self.exit_text = Button(self.sidebar,text='Exit',bg = "#ffffff",font=("",13,"bold"),bd=0,cursor='hand2',activebackground="#ffffff",activeforeground="#0064d3",command=self.logout)
        self.exit_text.place(x=80,y= 370)
        
        self.exit_indicator = Label(self.sidebar,text=" ",bg='#ffffff')
        self.exit_indicator.place(x = 10,y=370,width = 5,height=30)
        
        # ===================================================== #
              
    def indicate(self,lb,page):
        self.hide_indicator()
        lb.config(bg="#000000")
        self.delete_page()
        self.common_page()
        page()
        
    def delete_page(self):
        for frame in self.root.winfo_children():
            frame.destroy()
               
    def hide_indicator(self):
        self.dashboard_indicator.config(bg="#ffffff")
        self.start_indicator.config(bg="#ffffff")
        self.updateProfile_indicator.config(bg="#ffffff")
        self.exit_indicator.config(bg="#ffffff")
        
    def hide_current_frame(self):
        if self.current_frame:
            self.current_frame.pack_forget()

    def show_frame(self, frame):
        self.hide_current_frame()
        frame.pack(expand=True, fill='both')
        self.current_frame = frame

    def home_page(self):
        self.total_curls = 0
        self.total_push_ups = 0
        self.total_sit_ups = 0

        if not self.user:
            print("User not logged in.")
            self.show_login_page()
            return
        
        self.common_page()
        # ===================== Body ========================= #
        self.heading = Label(self.root,text ="Dashboard",font=("",13,"bold"),fg='#0064d3', bg = '#eff5f6')
        self.heading.place(x=325,y=70)
        # ===================================================== #
        
        # ====================== Body Frame 1========================= #
        self.bodyframe1 = Frame(self.root,bg='#ffffff')

        
        # Create a treeview widget
        tree = ttk.Treeview(self.bodyframe1, columns=('Exercise Type', 'Count', 'Timestamp'), show='headings')
        label_heading = tk.Label(tree, text='Exercise Type', font=("", 13, 'bold'),fg="#000000")
        tree.heading('Exercise Type',text='Exercise Type')
        tree.heading('Count', text='Count',anchor='center')
        tree.column('Count', anchor='center')
        tree.heading('Timestamp', text='Timestamp')
        tree.column('Exercise Type', anchor='center')  # Adjust the padding as needed
        tree.column('Timestamp', anchor='center')

        cursor = self.db_instance.db_connection.cursor()
        cursor.execute('''
            SELECT exercise_type, count, timestamp
            FROM exercise_history
            WHERE user_id = ?
            ORDER BY timestamp DESC
        ''', (self.user['id'],))
        exercise_history = cursor.fetchall()


        # Add horizontal separator lines
        tree.tag_configure("data_row", background="#ffffff",font=("", 13))  # Set your desired color for even rows
        tree.tag_configure("data_row_odd", background="#f0f0f0",font=("", 13))  # Set your desired color for odd rows

        # Modify the loop to set the background color for each row
        for i, exercise in enumerate(exercise_history):
            exercise_type = exercise[0]
            count = exercise[1]
            if exercise_type.lower() == 'curl':
                self.total_curls += count
            elif exercise_type.lower() == 'pushup':
                self.total_push_ups += count
            elif exercise_type.lower() == 'situp':
                self.total_sit_ups += count
                
            timestamp_str = exercise[2]
            timestamp_datetime = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            exercise_with_date = (exercise[0], exercise[1], timestamp_datetime.strftime("%d-%m-%Y"))
            tag = "data_row_odd" if i % 2 != 0 else "data_row"
            tree.insert('', 'end', values=exercise_with_date, tags=(tag,))
        # Display the treeview
        tree.pack(pady=10)
        
        self.bodyframe1.place(x=328,y=110,width = 925 , height = 300)
        
        
        # ====================== Body Frame 2========================= #
        self.bodyframe2 = Frame(self.root,bg='#009aa5')
        self.bodyframe2.place(x=328,y=435,width = 290 , height = 185)
        
        # ====================== Body Frame 3========================= #
        self.bodyframe3 = Frame(self.root,bg='#e21f26')
        self.bodyframe3.place(x=647,y=435,width = 290 , height = 185)
        
        # ====================== Body Frame 4========================= #
        self.bodyframe4 = Frame(self.root,bg='#ffcb1f')
        self.bodyframe4.place(x=963,y=435,width = 290 , height = 185)
        
        # ====================== Curls ================================ #
        self.curlsImage = Image.open('images\\curls-icon.png')
        photo = ImageTk.PhotoImage(self.curlsImage)
        self.curls = Label(self.bodyframe2, image=photo,bg='#009aa5')
        self.curls.image = photo
        self.curls.place(x=170,y=25)
        
        self.curlsCount_text = Label(self.bodyframe2,text=self.total_curls,bg = "#009aa5",fg="#ffffff",font=("",20,"bold"),bd=0)
        self.curlsCount_text.place(x=50,y= 80)
        
        self.curls_text = Label(self.bodyframe2,text='Total Curls',bg = "#009aa5",font=("",13,"bold"),bd=0)
        self.curls_text.place(x=25,y= 150)
        
        # ====================== Push-Ups ================================ #
        self.pushUpsImage = Image.open('images\\push-ups-icon.png')
        photo = ImageTk.PhotoImage(self.pushUpsImage)
        self.pushUps = Label(self.bodyframe3, image=photo,bg='#e21f26')
        self.pushUps.image = photo
        self.pushUps.place(x=170,y=25)
        
        self.pushUpsCount_text = Label(self.bodyframe3,text=self.total_push_ups,bg = "#e21f26",fg="#ffffff",font=("",20,"bold"),bd=0)
        self.pushUpsCount_text.place(x=50,y= 80)
        
        self.pushUps_text = Label(self.bodyframe3,text='Total Push-Ups',bg = "#e21f26",font=("",13,"bold"),bd=0)
        self.pushUps_text.place(x=25,y= 150)
        
        # ====================== Sit-Ups ================================ #
        self.sitUpsImage = Image.open('images\\sit-ups-icon.png')
        photo = ImageTk.PhotoImage(self.sitUpsImage)
        self.sitUps = Label(self.bodyframe4, image=photo,bg='#ffcb1f')
        self.sitUps.image = photo
        self.sitUps.place(x=170,y=25)
        
        self.sitUpsCount_text = Label(self.bodyframe4,text=self.total_sit_ups,bg = "#ffcb1f",fg="#ffffff",font=("",20,"bold"),bd=0)
        self.sitUpsCount_text.place(x=50,y= 80)
        
        self.sitUps_text = Label(self.bodyframe4,text='Total sit-Ups',bg = "#ffcb1f",font=("",13,"bold"),bd=0)
        self.sitUps_text.place(x=25,y= 150)

        # self.show_frame(home_frame)

    def update_profile_page(self):
        self.common_page()
        # ===================== Body ========================= #
        self.heading = Label(self.root,text ="Update Profile",font=("",13,"bold"),fg='#0064d3', bg = '#eff5f6')
        self.heading.place(x=325,y=70)
        # ===================================================== #
        
        # ====================== Body Frame 1========================= #
        self.bodyframe1 = Frame(self.root,bg='#ffffff')

        # profile photo
        self.change_profile_label = tk.Label(self.bodyframe1, text="Change Profile",font=('',13,"bold"),bg="#ffffff")
        self.change_profile_label.place(x=40,y=20)
        
        self.profileImage = self.db_instance.retrieve_profile_image(self.user['id'])
        self.profileImage = Image.open(io.BytesIO(self.profileImage)).resize((150,150))  
        photo = ImageTk.PhotoImage(self.profileImage)
        self.profile = Label(self.bodyframe1, image=photo,bg='#ffffff')
        self.profile.image = photo
        self.profile.place(x=50,y=50)
        
        self.change_profile_button  = Button(self.bodyframe1, text="Change Profile Picture",font=('',13,"bold"),bg='lightgreen',command=self.change_profile_image)
        self.change_profile_button.place(x=50,y=230)
        
        # Change Username
        self.change_username_label = tk.Label(self.bodyframe1, text="Change Username",font=('',13,"bold"),bg="#ffffff")
        self.change_username_label.place(x=40,y=320)
        
        self.label = tk.Label(self.bodyframe1, text="Enter new username:",font=('',13),bg="#ffffff")
        self.label.place(x=50,y=350)

        # self.username_entry = tk.Entry(self.bodyframe1,font=('',13),bg="#eeeeee")
        # self.username_entry.place(x=50,y=390)
        
        self.username_entry = Entry(self.bodyframe1, highlightthickness=0, relief=FLAT, bg="#ffffff",
                                    font=("yu gothic ui", 12, "bold"), insertbackground = '#6b6a69')
        self.username_entry.place(x=50,y=390)

        self.username_line = Canvas(self.bodyframe1, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.username_line.place(x=50,y=420)

        self.change_username_button = tk.Button(self.bodyframe1, text="Change Username" ,font=('',13,"bold"),bg='lightgreen',command=lambda: self.change_username(self.user['id'],self.username_entry.get()))
        self.change_username_button.place(x=50,y=440)
        
        #change password 
        
        self.change_password_label = tk.Label(self.bodyframe1, text="Change Password ",font=('',13,"bold"),bg="#ffffff")
        self.change_password_label.place(x=500,y=20)
        
        self.oplabel = tk.Label(self.bodyframe1, text="Old Password:",font=('',13),bg="#ffffff")
        self.oplabel.place(x=510,y=50)

        # self.opassword_entry = tk.Entry(self.bodyframe1,font=('',13),bg="#eeeeee", show="*", insertbackground = '#6b6a69')
        # self.opassword_entry.place(x=510,y=90)
        
        self.opassword_entry = Entry(self.bodyframe1, highlightthickness=0, relief=FLAT, bg="#ffffff",
                                    font=("yu gothic ui", 12, "bold"), show="*", insertbackground = '#6b6a69')
        self.opassword_entry.place(x=510,y=90)

        self.opassword_line = Canvas(self.bodyframe1, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.opassword_line.place(x=510,y=120)
        
        self.show_image = ImageTk.PhotoImage \
            (file='images\\show.png')

        self.hide_image = ImageTk.PhotoImage \
            (file='images\\hide.png')

        self.show_button = Button(self.bodyframe1, image=self.show_image, command=lambda : self.show(self.bodyframe1,self.opassword_entry), relief=FLAT,
                                  activebackground="white"
                                  , borderwidth=0, background="white", cursor="hand2")
        self.show_button.place(x=850,y=100)
        
        
        self.plabel = tk.Label(self.bodyframe1, text="New Password:",font=('',13),bg="#ffffff")
        self.plabel.place(x=510,y=150)
        
        # self.password_entry = tk.Entry(self.bodyframe1,font=('',13),bg="#eeeeee", show="*", insertbackground = '#6b6a69')
        # self.password_entry.place(x=510,y=190)
        
        self.password_entry = Entry(self.bodyframe1, highlightthickness=0, relief=FLAT, bg="#ffffff",
                                    font=("yu gothic ui", 12, "bold"), show="*", insertbackground = '#6b6a69')
        self.password_entry.place(x=510,y=190)

        self.password_line = Canvas(self.bodyframe1, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.password_line.place(x=510,y=220)
        
        
        self.cplabel = tk.Label(self.bodyframe1, text="Confirm Password:",font=('',13),bg="#ffffff")
        self.cplabel.place(x=510,y=250)

        self.show_button1 = Button(self.bodyframe1, image=self.show_image, command=lambda : self.show(self.bodyframe1,self.password_entry), relief=FLAT,
                                  activebackground="white"
                                  , borderwidth=0, background="white", cursor="hand2")
        self.show_button1.place(x=850,y=200)
        
        # self.cpassword_entry = tk.Entry(self.bodyframe1,font=('',13),bg="#eeeeee", show="*", insertbackground = '#6b6a69')
        # self.cpassword_entry.place(x=510,y=290)
        
        self.cpassword_entry = Entry(self.bodyframe1, highlightthickness=0, relief=FLAT, bg="#ffffff",
                                    font=("yu gothic ui", 12, "bold"), show="*", insertbackground = '#6b6a69')
        self.cpassword_entry.place(x=510,y=290)

        self.cpassword_line = Canvas(self.bodyframe1, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.cpassword_line.place(x=510,y=320)

        self.change_password_button = tk.Button(self.bodyframe1, text="Change Password" ,font=('',13,"bold"),bg='lightgreen',command=lambda: self.change_password(self.user['id'],self.opassword_entry.get(),self.password_entry.get(),self.cpassword_entry.get()))
        self.change_password_button.place(x=510,y=350)
        
        self.error_label = Label(self.bodyframe1, text="", bg="#ffffff", fg="red",
                                    font=("yu gothic ui", 10, "bold"))
        self.error_label.place(x=450, y=480)
        
        self.bodyframe1.place(x=328,y=110,width = 925 , height = 530)
    
    def change_password(self, userid, opassword, password, cpassword):
        if self.validate_password(password):
            if password == cpassword:
                cursor = self.db_instance.db_connection.cursor()
                cursor.execute('''
                    SELECT password FROM users WHERE id = ?
                    ''', (userid,))
                user_data = cursor.fetchone()
                if user_data and bcrypt.verify(opassword, user_data[0]):
                    hashed_new_password = bcrypt.hash(password)
                    self.db_instance.update_password(userid, hashed_new_password)
                    self.error_label.config(text="Password updated!", fg='green')
                    return True
                else:
                    self.error_label.config(text="Incorrect old password", fg='red')
        else:
            self.error_label.config(text="Invalid password", fg='red')
        return False

    def change_username(self,userid,username):
        if self.validate_username(username):
            self.db_instance.update_username(userid,username)
            self.user['username'] = username
            self.indicate(self.updateProfile_indicator,self.update_profile_page)
            self.error_label.config(text="Username updated !",fg='green')
            
            return True
        else:
            # self.error_label.config(text='Username only include alphabets,numbers,and underscore')
            # self.error_label.place(x=550,y=200)
            
            self.error_label.config(text="Invalid username",fg='red')
            print("Invalid username.")
            return
        
    def change_profile_image(self):
        
        # Open a file dialog to select an image file
        file_path = filedialog.askopenfilename(title="Select Profile Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])

        if file_path:
            self.db_instance.update_profile_image(self.user['id'],file_path)
            self.indicate(self.updateProfile_indicator,self.update_profile_page)
            self.error_label.config(text="Profile picture updated!",fg='green')
                      
    def show_choose_exercise_page(self):
        self.release_camera()
        self.choose_exercise_page()

    def choose_exercise_page(self):
        exercises = [
            {"name": "curl", "image_path": "images/curls-icon.png"},
            {"name": "pushup", "image_path": "images/push-ups-icon.png"},
            {"name": "situp", "image_path": "images/sit-ups-icon.png"}
        ]  # Add your exercises here with corresponding image paths

        choose_frame = tk.Frame(self.root, bg='#eff5f6')  # Yellow background
        choose_frame = tk.Frame(self.root, width=1280, height=700, bg='#eff5f6')
        choose_frame.pack_propagate(0)  # Disable automatic resizing
        choose_frame.pack(expand=True, fill='both')
        bodyframe1 = Frame(choose_frame,bg='#ffffff')
        bodyframe1.place(x=328,y=110,width = 925 , height = 540)
        self.common_page()
        heading = Label(choose_frame,text ="Select an Exercise:",font=("",13,"bold"),fg='#0064d3', bg = '#eff5f6')
        heading.place(x=325,y=70)

        # tk.Label(choose_frame, text="Select an Exercise:", font=('Helvetica', 12), background='#ffcc00').pack(pady=60)
        optBtnx = 30
        optBtny = 30
        for exercise in exercises:
            image = Image.open(exercise["image_path"]).resize((100, 100))
            img_tk = ImageTk.PhotoImage(image)

            button = ttk.Button(bodyframe1, text=exercise["name"], image=img_tk, compound=tk.TOP,
                                command=lambda e=exercise: self.show_real_time_detection_page(e["name"]))
            button.image = img_tk
            button.place(x=optBtnx,y=optBtny)
            optBtnx+= 120

        

        self.show_frame(choose_frame)

    def show_real_time_detection_page(self, exercise):
        self.exercise_type = exercise
        self.set_sets_page()  # Call set_sets_page after choosing exercise

    def real_time_detection_page(self, exercise=" "):
        detection_frame = tk.Frame(self.root)
        detection_frame = tk.Frame(self.root, width=1280, height=700)
        detection_frame.pack_propagate(0)  # Disable automatic resizing
        detection_frame.pack(expand=True, fill='both')
        self.common_page()

        self.exercise_title_var = tk.StringVar()
        self.count_var = tk.StringVar()
        
        # count_label = tk.Label(detection_frame, textvariable=self.count_var, font=('Helvetica', 14, 'italic'))
        # count_label.pack(pady=10)

        # Create a label for video display
        self.video_label = tk.Label(detection_frame)
        self.video_label.pack(pady=80)

        self.cap = cv2.VideoCapture(0)  # Use the appropriate video source
        self.update_video()

        self.show_frame(detection_frame)

    def update_video(self):
        self.count_var.set("Counts: "+str(int(self.count)))
        ret, img = self.cap.read()
        if ret:
            img = cv2.resize(img, (1280, 720))
            img = self.detector.findPose(img, False)
            lmList = self.detector.findPosition(img, False)
            
            if len(lmList) != 0:
                if self.exercise_type == "curl":
                    img, count = self.process_curls(img)    
                    # Check if the count has reached the specified number of sets
                    if count >= self.num_sets:
                        self.release_camera()
                        self.congratulations_page()  # Show congratulations page
                        return
                elif self.exercise_type == "pushup":
                    img, count = self.process_pushups(img)    
                    # Check if the count has reached the specified number of sets
                    if count >= self.num_sets:
                        self.release_camera()
                        self.congratulations_page()  # Show congratulations page
                        return
                    
                elif self.exercise_type == "situp":
                    img, count = self.process_situps(img)    
                    # Check if the count has reached the specified number of sets
                    if count >= self.num_sets:
                        self.release_camera()
                        self.congratulations_page()  # Show congratulations page
                        return

            # Convert frame from BGR to RGB
            frame_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # Resize frame to fit the label
            frame_rgb = cv2.resize(frame_rgb, (640, 480))
            # Convert the frame to ImageTk format
            img_tk = ImageTk.PhotoImage(Image.fromarray(frame_rgb))
            # Update the label with the new image
            self.video_label.configure(image=img_tk)
            self.video_label.image = img_tk
            self.root.after(10, self.update_video)  # Schedule the next update
        else:
            print("Video ended or failed to read.")
            self.release_camera()
            self.show_choose_exercise_page()
            
    def process_pushups(self, img):
        angle = self.detector.findAngle(img, 11, 13, 15)
        per = np.interp(angle, (200, 270), (0, 100))
        bar = np.interp(angle, (200, 270), (600, 200))

        bar_color = (255, 255, 255)
        text_color = (0, 0, 255)

        if per == 100:
            bar_color = (0, 255, 0)
            text_color = (0, 255, 0)
            if self.dir == 1:
                self.count += 0.5
                self.dir = 0
        if per == 0:
            if self.dir == 0:
                self.count += 0.5
                self.dir = 1
                
        cv2.rectangle(img, (1100, int(bar)), (1150, 600), bar_color, cv2.FILLED)
        cv2.rectangle(img, (1100, 200), (1150, 600), (255, 0, 0), 3)
        cv2.putText(img, f'{int(per)}%', (1090, 175), cv2.FONT_HERSHEY_DUPLEX, 1, text_color, 1)
        cv2.putText(img, "Count : " + str(int(self.count)), (20, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 100), 1)

        return img, self.count

    def process_situps(self, img):
        angle = max(self.detector.findAngle(img, 12, 24, 26), self.detector.findAngle(img, 11, 23, 25))
        leg_angle = max(self.detector.findAngle(img, 24, 26, 28), self.detector.findAngle(img, 23, 25, 27))
        hand_angle = max(self.detector.findAngle(img, 12, 14, 16, False), self.detector.findAngle(img, 11, 13, 15))
        per = np.interp(angle, (75, 120), (100, 0))
        bar = np.interp(angle, (75, 120), (200, 600))

        bar_color = (255, 255, 255)
        text_color = (0, 0, 255)

        if per == 100 and leg_angle >= 260 and hand_angle >= 35:
            bar_color = (0, 255, 0)
            text_color = (0, 255, 0)
            if self.dir == 1:
                self.count += 0.5
                self.dir = 0
        if per == 0 and leg_angle >= 260 and hand_angle >= 35:
            if self.dir == 0:
                self.count += 0.5
                self.dir = 1

        cv2.rectangle(img, (1100, int(bar)), (1150, 600), bar_color, cv2.FILLED)
        cv2.rectangle(img, (1100, 200), (1150, 600), (255, 0, 0), 3)
        cv2.putText(img, f'{int(per)}%', (1090, 175), cv2.FONT_HERSHEY_DUPLEX, 1, text_color, 1)
        cv2.putText(img, "Count : " + str(int(self.count)), (20, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 100), 1)

        return img, self.count
        
    def process_curls(self, img):
        angle = max(self.detector.findAngle(img, 12, 14, 16) , self.detector.findAngle(img, 11, 13, 15))
        
        per = np.interp(angle, (210, 310), (0, 100))
        bar = np.interp(angle, (210, 310), (600, 200))

        bar_color = (255, 255, 255)
        text_color = (0, 0, 255)
        if per == 100:
            bar_color = (0, 255, 0)
            text_color = (0, 255, 0)
            if self.dir == 1:
                self.count += 0.5
                self.dir = 0
        if per == 0:
            if self.dir == 0:
                self.count += 0.5
                self.dir = 1
        cv2.rectangle(img, (1100, int(bar)), (1150, 600), bar_color, cv2.FILLED)
        cv2.rectangle(img, (1100, 200), (1150, 600), (255, 0, 0), 3)
        cv2.putText(img, f'{int(per)}%', (1090, 175), cv2.FONT_HERSHEY_DUPLEX, 1, text_color, 1)
        cv2.putText(img, "Count : " + str(int(self.count)), (20, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 100), 1)
        
        return (img, self.count)
    
    def show_home_page(self):
        self.release_camera()
        self.home_page()

    def release_camera(self):
        if hasattr(self, 'cap') and self.cap:
            print("Releasing Camera")
            self.cap.release()

    def set_sets_page(self):
        sets_frame = tk.Frame(self.root)
        sets_frame = tk.Frame(self.root, width=1280, height=700)
        sets_frame.pack_propagate(0)  # Disable automatic resizing
        sets_frame.pack(expand=True, fill='both')
        
        bodyframe1 = Frame(sets_frame,bg='#ffffff')
        bodyframe1.place(x=328,y=110,width = 925 , height = 540)
        self.common_page()
        
        heading = Label(sets_frame,text ="Number of Sets:",font=("",13,"bold"),fg='#0064d3', bg = '#eff5f6')
        heading.place(x=325,y=70)
        
        self.sets_entry = Entry(bodyframe1, highlightthickness=0, relief=FLAT, bg="#ffffff",
                                    font=("yu gothic ui", 12, "bold"), insertbackground = '#6b6a69')
        self.sets_entry.place(x=30,y=30)

        self.sets_line = Canvas(bodyframe1, width=300, height=2.0, bg="#bdb9b1", highlightthickness=0)
        self.sets_line.place(x=30,y=60)
        
        self.set_message = Label(bodyframe1,text ="",font=("",13,"bold"),fg='red', bg = '#ffffff')
        self.set_message.place(x=30,y=70)

        self.sets_button = tk.Button(bodyframe1, text="Next" ,font=('',13,"bold"),bg='orange',command=self.validate_sets)
        self.sets_button.place(x=30,y=100)

        self.show_frame(sets_frame)  # Show the sets page

    def congratulations_page(self):
        
        cursor = self.db_instance.db_connection.cursor()
        cursor.execute('''
            INSERT INTO exercise_history (user_id, exercise_type, count)
            VALUES (?, ?, ?)
        ''', (self.user['id'], self.exercise_type, self.num_sets))
        self.db_instance.db_connection.commit()
        
        congrats_frame = tk.Frame(self.root)
        congrats_frame = tk.Frame(self.root, width=1280, height=700)
        congrats_frame.pack_propagate(0)  # Disable automatic resizing
        congrats_frame.pack(expand=True, fill='both')
        
        bodyframe1 = Frame(congrats_frame,bg='#ffffff')
        bodyframe1.place(x=328,y=110,width = 925 , height = 540)
        self.common_page()

        congratulationImage = Image.open('images\\challenge-completed.png').resize((880,500))
        photo = ImageTk.PhotoImage(congratulationImage)
        congratulation = Label(bodyframe1, image=photo,bg='#ffffff')
        congratulation.image = photo
        congratulation.place(x=20,y=20)
        
        congrats = Label(bodyframe1,text = "You are completed set of "+str(self.num_sets)+" "+self.exercise_type,font=("Trebuchet MS",15,"bold italic"),fg='#000000', bg = '#ffffff')
        congrats.place(x=300,y=360)

        self.show_frame(congrats_frame)  # Show the congratulations page

    def start_exercise(self):
        # Retrieve the number of sets entered by the user
        self.num_sets = int(self.sets_entry.get())
        self.count = 0  # Reset exercise count
        self.hide_current_frame()
        self.real_time_detection_page(self.exercise_type)

    def show_home_page(self):
        # Hide the current frame and show the home page
        self.hide_current_frame()
        self.home_page()

    def validate_username(self,username):
        # Allow only alphanumeric characters and underscores
        pattern = re.compile("^[a-zA-Z0-9_]+$")
        return bool(pattern.match(username))

    def validate_email(self,email):
        # Check if the email follows a basic pattern
        pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        return bool(pattern.match(email))

    def validate_password(self,password):
        # Password should be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one digit
        pattern = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$")
        return bool(pattern.match(password))   
     
    def validate_input(self,username, email, password):
        def validate_username(username):
            # Allow only alphanumeric characters and underscores
            pattern = re.compile("^[a-zA-Z0-9_]+$")
            return bool(pattern.match(username))

        def validate_email(email):
            # Check if the email follows a basic pattern
            pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
            return bool(pattern.match(email))

        def validate_password(password):
            # Password should be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one digit
            pattern = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$")
            return bool(pattern.match(password))

        if validate_username(username):
            print("Username is valid.")
            return True
        else:
            self.error_label.config(text='Username only include alphabets,numbers,and underscore')
            self.error_label.place(x=550,y=200)
            print("Invalid username.")
            return

        if validate_email(email):
            print("Email is valid.")
            return True
        else:
            self.error_label.config(text='Invalid email')
            self.error_label.place(x=650,y=200)
            print("Invalid email.")
            return

        if validate_password(password):
            print("Password is valid.")
            return True
        else:
            self.error_label.config(text='Password should be at least 8 characters & \n contain at least 1 uppercase letter,\n 1 lowercase letter, and 1 digit')
            self.error_label.place(x=600,y=200)
            print("Invalid password.")
        
        return True

    def validate_sets(self):
        sets_input = self.sets_entry.get()

        try:
            num_sets = int(sets_input)
            if num_sets > 4 and num_sets < 26:
                # If the input is a valid positive integer, proceed to the next step
                print(f"Number of sets: {num_sets}")
                self.start_exercise()
                # Add your logic here to handle the valid input
            else:
                self.set_message.config(text="Please enter a valid positive number of sets (5-25)")
                print("Please enter a valid positive number of sets.")
        except ValueError:
            self.set_message.config(text="Please enter a valid number.")
            print("Please enter a valid number.")
        
        
if __name__ == "__main__":
    root = tk.Tk()
    app = PersonalAITrainer(root)
    root.mainloop()
