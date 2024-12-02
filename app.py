import tkinter as tk
from tkinter import PhotoImage, Label, messagebox
from PIL import Image, ImageTk  # Assurez-vous que Pillow est installé
import os
import sys  # Importer sys pour quitter le programme
# from CaptureEtAffichePhoto import PhotoBoothApp
from recognition_page import FaceRecognition
from home import HomePage
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
        for F in (HomePage, FaceRecognition):
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
