
import customtkinter
import pymongo
from pymongo import MongoClient
import os
from tkinter import messagebox
cluster = MongoClient("mongodb+srv://pietro:pietro123@cluster0.us5r2h2.mongodb.net/?retryWrites=true&w=majority")
db = cluster["Blackjack"]
collection = db["users"]

class LoginPage(customtkinter.CTk):

    WIDTH = 300
    HEIGHT = 180

    def __init__(self):
        super().__init__()
        
        self.title("Login")
        self.geometry(f"{LoginPage.WIDTH}x{LoginPage.HEIGHT}")
        self.iconbitmap("Assets/Icon/jack_of_spades.ico")
        self.resizable(0,0)
        # setup grid (5x3)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(6, weight=1)

        self.title = customtkinter.CTkLabel(master=self, text="Login", font=("Arial", 20))
        self.title.grid(row=1, column=1, sticky="ew")

        self.username = customtkinter.CTkEntry(master=self, placeholder_text ="Username")
        self.username.grid(row=3, column=1, sticky="ew")
        self.username.bind("<Return>", lambda event: self.password.focus())

        self.password = customtkinter.CTkEntry(master=self, placeholder_text ="Password", show = '*')
        self.password.grid(row=5, column=1, sticky="ew")
        self.password.bind("<Return>", self.login)

    def login(self, *args):
        self.username_active = self.username.get()
        password = self.password.get()
        if collection.find_one({"username": self.username_active}):
            if collection.find_one({"username": self.username_active})["password"] == password:
                self.destroy()
                
            else:
                messagebox.showerror("Error", "Wrong Password")
        else:
            insert = {"username": self.username_active, "password": password, "fiches": "100"}
            collection.insert_one(insert)
            self.destroy()
        self.fiches_active = collection.find_one({"username": self.username_active})["fiches"]

    def update_fiches(self, fiches):
        collection.update_one({"username": self.username_active}, {"$set": {"fiches": fiches}})

        
