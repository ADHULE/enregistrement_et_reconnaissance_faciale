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
        label_title = tk.Label(self, text="SYSTEME DE RECONNAISSANCE FACIALE", font=("Arial", 24, "bold"), bg="#2c3e50", fg="#ecf0f1")
        label_title.pack(pady=20)

        # Cadre principal pour organiser les éléments au centre
        main_frame = tk.Frame(self, bg="#34495e", bd=10, relief=tk.GROOVE)
        main_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        # Cadre pour les logos
        logos_frame = tk.Frame(main_frame, bg="#34495e", bd=5, relief=tk.RIDGE)
        logos_frame.pack(pady=10, padx=10, side=tk.TOP, fill=tk.X)

        # Configurer les colonnes pour uniformiser la largeur
        for i in range(3):  # 3 colonnes
            logos_frame.grid_columnconfigure(i, weight=1)

        # Ajouter les images de l'entreprise avec leurs titres respectifs
        images_info = [("admin.jpg", "ENREGISTREMENT"), 
                       ("recognition.jpg", "RECONNAISSANCE"), 
                       ("logoMoise.jpg", "")]
        for i, (path, title) in enumerate(images_info):
            self.add_logo(logos_frame, path, i, title)

        # Cadre pour les boutons de navigation
        button_frame = tk.Frame(main_frame, bg="#34495e", bd=5, relief=tk.RIDGE)
        button_frame.pack(pady=20, padx=20, fill=tk.X)

        # Configurer les lignes et les colonnes pour les rendre responsives
        for i in range(3):  # 3 colonnes
            button_frame.grid_columnconfigure(i, weight=1)

        # Style des boutons
        button_style = {"fg": "white", "font": ("Arial", 14), "padx": 20, "pady": 10}

        # Boutons de navigation
        tk.Button(button_frame, text="Capture d'Image", 
                  command=lambda: controller.show_frame("PhotoBoothApp"), 
                  bg="#3498db", **button_style).grid(row=0, column=0, pady=10, padx=10, sticky="nsew")
        
        tk.Button(button_frame, text="Reconnaissance Faciale", 
                  command=lambda: controller.show_frame("FaceRecognition"), 
                  bg="#1abc9c", **button_style).grid(row=0, column=1, pady=10, padx=10, sticky="nsew")
        
        tk.Button(button_frame, text="OFF", 
                  command=sys.exit, 
                  bg="#e74c3c", **button_style).grid(row=0, column=2, pady=10, padx=10, sticky="nsew")

    def add_logo(self, parent, image_path, column, title):
        logo_frame = tk.Frame(parent, bg="#34495e", bd=5, relief=tk.RIDGE)
        logo_frame.grid(row=0, column=column, padx=10, pady=10, sticky="nsew")
        logo_label = tk.Label(logo_frame, text=title, font=("Arial", 18), bg="#34495e", fg="#ecf0f1")
        logo_label.pack(pady=5)

        if os.path.exists(image_path):  # Vérifier si l'image existe
            img = Image.open(image_path)
            img = img.resize((400, 400), Image.LANCZOS)  # Redimensionner l'image à une taille plus petite
            company_logo = ImageTk.PhotoImage(img)
            logo_image = tk.Label(logo_frame, image=company_logo, bg="#34495e")
            logo_image.image = company_logo  # Pour éviter la collecte des ordures
            logo_image.pack(pady=5)
        else:
            image_placeholder = tk.Label(logo_frame, text="[Image de l'Entreprise]", font=("Arial", 14), bg="#34495e", fg="#ecf0f1")
            image_placeholder.pack(pady=5)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Application de Surveillance et Reconnaissance")
        self.geometry("1080x720")
        self.config(bg="#2c3e50")

        # Définir l'icône de l'application
        icon_path = "logoMoise.ico"  # Remplacez par le chemin réel de l'icône
        if os.path.exists(icon_path):  # Vérifier si l'icône existe
            self.iconbitmap(icon_path)
        else:
            print("Icône non trouvée, vérifiez le chemin de l'icône.")

        # Créer un conteneur pour les pages
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (HomePage, PhotoBoothApp, FaceRecognition):
            page_name = F.__name__
            frame = F(container, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

    def show_frame(self, page_name):
        frame = self.frames.get(page_name)
        if frame:
            frame.tkraise()
        else:
            messagebox.showerror("Erreur", f"La page '{page_name}' n'existe pas.")

if __name__ == "__main__":
    app = App()
    app.mainloop()
