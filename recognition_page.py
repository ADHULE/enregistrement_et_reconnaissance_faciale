import os
import cv2
from playsound import playsound
import face_recognition
import numpy as np
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class FaceRecognition(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#2c3e50")
       
        # Configuration des éléments de l'interface
        self.setup_gui()

        # Créer les encodages des visages connus et leurs noms
        self.known_face_encodings = []
        self.known_face_names = []
        self.face_info = {}  # Dictionnaire pour stocker les informations sur les visages

        # Charger les visages connus
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
            self.controller.destroy()
            return

        # Démarrer le processus de mise à jour des frames
        self.is_running = True
        self.update_frame()

        # Fermer correctement l'application
        self.controller.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_gui(self):
        # Titre
        self.label_title = tk.Label(self, text="Application de Reconnaissance Faciale", font=("Arial", 30, "bold"), bg="#3e4149", fg="#ffcc00")
        self.label_title.pack(pady=20)

        # Cadre principal pour organiser tous les éléments
        self.main_frame = tk.Frame(self, bg="#3e4149")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Sous-cadre pour les éléments de la caméra et l'affichage des images
        self.camera_frame = tk.Frame(self.main_frame, bg="#3e4149")
        self.camera_frame.pack(fill=tk.BOTH, expand=True)

        # Configurer la disposition en grille pour le cadre de la caméra
        self.camera_frame.grid_rowconfigure(0, weight=1)
        self.camera_frame.grid_columnconfigure(0, weight=2)
        self.camera_frame.grid_columnconfigure(1, weight=1)

        # Canvas pour l'affichage vidéo
        self.canvas_camera = tk.Canvas(self.camera_frame, bg="#03A9F4", width=720, height=480)
        self.canvas_camera.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Cadre pour afficher les visages reconnus
        self.photo_frame = tk.Frame(self.camera_frame, bg="#E0FFFF", bd=2, relief=tk.SUNKEN)
        self.photo_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Label pour afficher la photo du visage reconnu
        self.recognized_face_label = tk.Label(self.photo_frame, bg="#2c3e50")
        self.recognized_face_label.pack(pady=20)

        # Label pour afficher les informations du visage reconnu
        self.recognized_face_info_label = tk.Label(self.photo_frame, bg="#2c3e50", font=("Arial", 14))
        self.recognized_face_info_label.pack()

        # Sous-cadre pour le bouton de retour
        self.button_frame = tk.Frame(self.main_frame, bg="#3e4149")
        self.button_frame.pack(pady=20)

        # Bouton pour retourner à la page principale
        self.back_button = tk.Button(self.button_frame, text="Retour à l'accueil", command=lambda: self.controller.show_frame("HomePage"), bg="#ff4757", fg="white", font=("Arial", 14), padx=20, pady=10)
        self.back_button.pack()

    def load_known_faces(self):
        # Implémentez la logique pour charger les visages connus
        pass

    def update_frame(self):
        # Implémentez la logique pour mettre à jour les frames de la vidéo
        pass

    def on_closing(self):
        self.is_running = False
        self.cap.release()
        self.controller.destroy()

# Exemple d'utilisation
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    app = FaceRecognition(root, root)  # Remplacez None par votre contrôleur réel si nécessaire
    app.pack(fill=tk.BOTH, expand=True)
    root.mainloop()
