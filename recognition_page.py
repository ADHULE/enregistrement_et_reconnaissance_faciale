import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
import os

class FaceRecognition(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#2c3e50")

        # Titre de la page
        label_title = tk.Label(self, text="Liste des Détenus", font=("Arial", 24, "bold"), bg="#2c3e50", fg="#ecf0f1")
        label_title.pack(pady=20)

        # Table pour afficher les détenus et leurs photos
        table_frame = tk.Frame(self, bg="#34495e")
        table_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        # Récupérer et afficher la liste des détenus
        self.display_detainees(table_frame)

        # Bouton retour à la page principale
        button_back = tk.Button(self, text="Retour", command=lambda: controller.show_frame("HomePage"), bg="#e74c3c", fg="white", font=("Arial", 14), padx=20, pady=10)
        button_back.pack(pady=20)

    def connect_to_db(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="face_recognition"
            )
            return conn
        except mysql.connector.Error as err:
            messagebox.showerror("Erreur", f"Erreur de connexion à la base de données : {err}")
            return None

    def display_detainees(self, frame):
        conn = self.connect_to_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nom, prenom, numero, image, date FROM detenu")
            rows = cursor.fetchall()
            conn.close()

            for i, row in enumerate(rows):
                for j, value in enumerate(row):
                    if j == 5:  # Colonne des photos
                        photo_frame = tk.Frame(frame, bg="#ecf0f1")
                        photo_frame.grid(row=i, column=j, sticky="nsew", padx=5, pady=5)
                        if value:  # Vérifier si la colonne image n'est pas vide
                            photos = value.split(",")  # Supposons que les chemins des photos sont stockés séparés par des virgules
                            for photo in photos:
                                if os.path.exists(photo):
                                    img = Image.open(photo)
                                    img.thumbnail((50, 50))  # Redimensionner l'image
                                    img_tk = ImageTk.PhotoImage(img)
                                    label = tk.Label(photo_frame, image=img_tk, bg="#ecf0f1")
                                    label.image = img_tk  # Empêcher la collecte des ordures
                                    label.pack(side=tk.LEFT)
                    else:
                        # Vérifier si la colonne contient une date
                        if isinstance(value, str) and len(value.split(",")) > 1:
                            # Traiter comme des images séparées par des virgules
                            photos = value.split(",")
                            photo_frame = tk.Frame(frame, bg="#ecf0f1")
                            photo_frame.grid(row=i, column=j, sticky="nsew", padx=5, pady=5)
                            for photo in photos:
                                if os.path.exists(photo):
                                    img = Image.open(photo)
                                    img.thumbnail((50, 50))  # Redimensionner l'image
                                    img_tk = ImageTk.PhotoImage(img)
                                    label = tk.Label(photo_frame, image=img_tk, bg="#ecf0f1")
                                    label.image = img_tk  # Empêcher la collecte des ordures
                                    label.pack(side=tk.LEFT)
                        else:
                            tk.Label(frame, text=value, font=("Arial", 12), bg="#ecf0f1", fg="#2c3e50", padx=10, pady=5).grid(row=i, column=j, sticky="nsew")
