import os
import cv2
from playsound import playsound
import face_recognition
import numpy as np
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class FaceRecognitionPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setup_gui()
        
        # Créer les encodages des visages connus et leurs noms
        self.known_face_encodings = []
        self.known_face_names = []
        self.load_known_faces()

        # Initialiser quelques variables
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.process_this_frame = True

        # Démarrer la capture vidéo
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            messagebox.showerror("Erreur", "La caméra n'est pas accessible.")
            self.parent.quit()
            return

        # Démarrer le processus de mise à jour des frames
        self.is_running = True
        self.update_frame()

    def setup_gui(self):
        # Titre
        label_title = tk.Label(self, text="Reconnaissance Faciale", font=("Arial", 30, "bold"))
        label_title.pack(pady=20)

        # Canvas pour l'affichage vidéo
        self.canvas_camera = tk.Canvas(self, bg="#03A9F4", width=720, height=480)
        self.canvas_camera.pack(pady=20)

        # Bouton pour arrêter la caméra et revenir à la page d'accueil
        btn_back = tk.Button(self, text="Retourner à l'Accueil", command=self.back_to_home, font=("Arial", 14))
        btn_back.pack(pady=10)
