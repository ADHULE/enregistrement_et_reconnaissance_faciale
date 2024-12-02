import tkinter as tk
from tkinter import PhotoImage, Label, messagebox
from PIL import Image, ImageTk  # Assurez-vous que Pillow est installé
import os
import sys  # Importer sys pour quitter le programme
from CaptureEtAffichePhoto import PhotoBoothApp
from recognition_page import FaceRecognition

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#2c3e50")

        # Titre de l'application
        label_title = tk.Label(self, text="Application de Surveillance et Reconnaissance", font=("Arial", 24, "bold"), bg="#2c3e50", fg="#ecf0f1")
        label_title.pack(pady=20)

        # Cadre principal
        main_frame = tk.Frame(self, bg="#2c3e50")
        main_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        # Cadre pour les logos
        logos_frame = tk.Frame(main_frame, bg="#34495e", bd=5, relief=tk.RIDGE)
        logos_frame.pack(pady=10, padx=10, side=tk.TOP, fill=tk.X)

        # Configurer les colonnes pour uniformiser la largeur
        for i in range(3):  # 3 colonnes
            logos_frame.grid_columnconfigure(i, weight=1)

        # Ajouter les images de l'entreprise
        images_paths = ["logoMoise.jpg", "admin.jpg", "logoMoise3.jpg"]  # Remplacez par les chemins réels des images
        for i, path in enumerate(images_paths):
            self.add_logo(logos_frame, path, i)

        # Cadre pour les boutons de navigation
        button_frame = tk.Frame(main_frame, bg="#34495e", bd=5, relief=tk.RIDGE)
        button_frame.pack(pady=20, padx=20, fill=tk.X)

        # Configurer les lignes et les colonnes pour les rendre responsives
        for i in range(3):  # 3 colonnes
            button_frame.grid_columnconfigure(i, weight=1)

        # Style des boutons
        button_style = {"fg": "white", "font": ("Arial", 14), "padx": 20, "pady": 10}

        # Boutons de navigation avec une largeur fixe
        button_width = 20  # Largeur fixe pour correspondre aux logos

        tk.Button(button_frame, text="Capture d'Image", 
                  command=lambda: controller.show_frame("PhotoBoothApp"), 
                  bg="#3498db", width=button_width, **button_style).grid(row=0, column=0, pady=10, padx=10, sticky="nsew")
        
        tk.Button(button_frame, text="Reconnaissance Faciale", 
                  command=lambda: controller.show_frame("FaceRecognition"), 
                  bg="#1abc9c", width=button_width, **button_style).grid(row=0, column=1, pady=10, padx=10, sticky="nsew")
        
        tk.Button(button_frame, text="OFF", 
                  command=sys.exit, 
                  bg="#e74c3c", width=button_width, **button_style).grid(row=0, column=2, pady=10, padx=10, sticky="nsew")

    def add_logo(self, parent, image_path, column):
        logo_frame = tk.Frame(parent, bg="#34495e", bd=5, relief=tk.RIDGE)
        logo_frame.grid(row=0, column=column, padx=10, pady=10, sticky="nsew")
        logo_label = tk.Label(logo_frame, text="Logo de l'Entreprise", font=("Arial", 18), bg="#34495e", fg="#ecf0f1")
        logo_label.pack(pady=5)

        if os.path.exists(image_path):  # Vérifier si l'image existe
            img = Image.open(image_path)
            img = img.resize((100, 100), Image.LANCZOS)  # Redimensionner l'image à une taille plus petite
            company_logo = ImageTk.PhotoImage(img)
            logo_image = tk.Label(logo_frame, image=company_logo, bg="#34495e")
            logo_image.image = company_logo  # Pour éviter la collecte des ordures
            logo_image.pack(pady=5)
        else:
            image_placeholder = tk.Label(logo_frame, text="[Image de l'Entreprise]", font=("Arial", 14), bg="#34495e", fg="#ecf0f1")
            image_placeholder.pack(pady=5)

# Exemple d'utilisation :
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("600x400")
    app = HomePage(root, None)  # Remplacez None par votre contrôleur réel si nécessaire
    app.pack(fill=tk.BOTH, expand=True)
    root.mainloop()
