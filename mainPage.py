import tkinter as tk
from tkinter import PhotoImage, Label, messagebox
from PIL import Image, ImageTk  # Assurez-vous que Pillow est installé
import os
from recognition import FaceRecognitionPage

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

        # Cadre pour le logo
        logo_frame = tk.Frame(main_frame, bg="#34495e", bd=5, relief=tk.RIDGE)
        logo_frame.pack(pady=10, padx=10, side=tk.TOP, fill=tk.X)
        logo_label = tk.Label(logo_frame, text="Logo de l'Entreprise", font=("Arial", 18), bg="#34495e", fg="#ecf0f1")
        logo_label.pack(pady=10)

        # Ajouter l'image de l'entreprise
        image_path = "logoMoise.jpg"  # Remplacez par le chemin réel de l'image
        if os.path.exists(image_path):  # Vérifier si l'image existe
            img = Image.open(image_path)
            img = img.resize((300, 300), Image.LANCZOS)  # Redimensionner l'image à une taille fixe
            company_logo = ImageTk.PhotoImage(img)
            logo_image = tk.Label(logo_frame, image=company_logo, bg="#34495e")
            logo_image.image = company_logo  # Pour éviter la collecte des ordures
            logo_image.pack(pady=5)
        else:
            image_placeholder = tk.Label(logo_frame, text="[Image de l'Entreprise]", font=("Arial", 14), bg="#34495e", fg="#ecf0f1")
            image_placeholder.pack(pady=5)

        # Cadre pour les boutons de navigation
        button_frame = tk.Frame(main_frame, bg="#34495e", bd=5, relief=tk.RIDGE)
        button_frame.pack(pady=20, padx=20, fill=tk.X)

        # Configurer les lignes et les colonnes pour les rendre responsives
        for i in range(2):
            button_frame.grid_columnconfigure(i, weight=1)
        for i in range(2):
            button_frame.grid_rowconfigure(i, weight=1)

        # Style des boutons
        button_style = {"fg": "white", "font": ("Arial", 14), "padx": 20, "pady": 10}

        # Boutons de navigation
        tk.Button(button_frame, text="ON", command=lambda: controller.show_frame("FaceRecognitionPage"), bg="#3498db", **button_style).grid(row=0, column=0, pady=10, padx=10, sticky="nsew")
        tk.Button(button_frame, text="OFF", command=lambda: controller.quit(), bg="#1abc9c", **button_style).grid(row=0, column=1, pady=10, padx=10, sticky="nsew")


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Application de Surveillance et Reconnaissance")
        self.geometry("800x600")
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
        for F in (HomePage, FaceRecognitionPage):
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
