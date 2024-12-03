import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import cv2
from PIL import Image, ImageTk
import os
import time

class PhotoBoothApp(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="#2c3e50")
        self.controller = controller
        self.parent = parent

        # Titre de l'application
        self.label_title = tk.Label(self, text="ENREGISTREMENT", font=("Arial", 24, "bold"), bg="#2c3e50", fg="#ecf0f1")
        self.label_title.pack(pady=20)

        # Cadre principal pour organiser les éléments
        self.main_frame = tk.Frame(self, bg="#2c3e50")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Configuration de la grille pour rendre les widgets responsive
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(2, weight=1)

        # Canvas pour afficher la caméra
        self.canvas = tk.Canvas(self.main_frame, bg="black")
        self.canvas.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Canvas pour afficher les images capturées
        self.canvas_images = tk.Canvas(self.main_frame, bg="black")
        self.canvas_images.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Cadre pour les boutons et la liste des images
        self.side_frame = tk.Frame(self.main_frame, bg="#34495e")
        self.side_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        # Bouton pour capturer une photo
        self.button_capture = tk.Button(self.side_frame, text="Prendre une Photo", font=("Arial", 14), command=self.capture_photo, bg="#3498db", fg="white")
        self.button_capture.pack(pady=15, fill=tk.X)

        # Bouton pour afficher la dernière photo prise
        self.button_show_last_photo = tk.Button(self.side_frame, text="Afficher la Dernière Photo", font=("Arial", 14), command=self.show_last_photo, bg="#1abc9c", fg="white")
        self.button_show_last_photo.pack(pady=15, fill=tk.X)

        # Bouton retour à la page principale
        self.button_back = tk.Button(self.side_frame, text="Retour", command=lambda: controller.show_frame("HomePage"), bg="#dc3545", fg="white", font=("Arial", 14), padx=20, pady=10)
        self.button_back.pack(pady=15, fill=tk.X)

        # Listbox pour afficher la liste des images
        self.listbox_images = tk.Listbox(self.side_frame, font=("Arial", 12), width=40, height=15, bg="#ecf0f1", fg="#2c3e50")
        self.listbox_images.pack(pady=10, fill=tk.BOTH, expand=True)
        self.listbox_images.bind('<<ListboxSelect>>', self.on_select_image)

        # Boutons pour supprimer et renommer une photo
        self.button_delete = tk.Button(self.side_frame, text="Supprimer la Photo", font=("Arial", 14), command=self.delete_photo, bg="#e74c3c", fg="white", state=tk.DISABLED)
        self.button_delete.pack(pady=5, fill=tk.X)

        self.button_rename = tk.Button(self.side_frame, text="Renommer la Photo", font=("Arial", 14), command=self.rename_photo, bg="#f39c12", fg="white", state=tk.DISABLED)
        self.button_rename.pack(pady=5, fill=tk.X)

        self.update_image_list()

        # Initialiser la caméra
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            messagebox.showerror("Erreur", "La caméra n'est pas accessible.")
            self.controller.destroy()
            return

        # Variable pour stocker le nom de la dernière photo prise
        self.last_photo = None

        # Démarrer la mise à jour de l'image de la caméra
        self.is_running = True
        self.update_frame()  # Utiliser after() pour planifier les mises à jour

        # Libérer la ressource de la caméra si la fenêtre est fermée
        self.controller.protocol("WM_DELETE_WINDOW", self.on_closing)

    def update_frame(self):
        # Mettre à jour l'image de la caméra
        if self.is_running:
            ret, frame = self.cap.read()
            if ret:
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
                self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
                self.canvas.config(width=self.canvas.winfo_width(), height=self.canvas.winfo_height())
            self.controller.after(10, self.update_frame)  # Planifier la prochaine mise à jour

    def capture_photo(self):
        # Capturer et enregistrer la photo
        ret, frame = self.cap.read()
        if ret:
            filename = f"data/photo_{int(time.time())}.jpg"
            cv2.imwrite(filename, frame)
            self.last_photo = filename  # Stocker le nom de la dernière photo prise
            messagebox.showinfo("Photo capturée", f"La photo a été capturée et enregistrée sous '{filename}'")
            self.update_image_list()  # Mettre à jour la liste des images

    def show_last_photo(self):
        # Afficher la dernière photo prise
        if self.last_photo:
            img = Image.open(self.last_photo)
            img = img.resize((self.canvas_images.winfo_width(), self.canvas_images.winfo_height()), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            self.canvas_images.create_image(0, 0, anchor=tk.NW, image=img_tk)
            self.canvas_images.image = img_tk  # Empêcher la collecte des ordures
        else:
            messagebox.showinfo("Aucune Photo", "Aucune photo n'a été prise encore.")

    def on_select_image(self, event):
        # Afficher l'image sélectionnée dans le cadre et activer les boutons
        selected_index = self.listbox_images.curselection()
        if selected_index:
            selected_image = self.listbox_images.get(selected_index)
            filepath = os.path.join("data", selected_image)
            img = Image.open(filepath)
            img = img.resize((self.canvas_images.winfo_width(), self.canvas_images.winfo_height()), Image.Resampling.LANCZOS)
            img_tk = ImageTk.PhotoImage(img)
            self.canvas_images.create_image(0, 0, anchor=tk.NW, image=img_tk)
            self.canvas_images.image = img_tk  # Empêcher la collecte des ordures

            # Activer les boutons de suppression et de renommage
            self.button_delete.config(state=tk.NORMAL)
            self.button_rename.config(state=tk.NORMAL)

    def delete_photo(self):
        # Supprimer la photo sélectionnée
        selected_index = self.listbox_images.curselection()
        if selected_index:
            selected_image = self.listbox_images.get(selected_index)
            filepath = os.path.join("data", selected_image)
            os.remove(filepath)
            messagebox.showinfo("Photo supprimée", f"La photo '{selected_image}' a été supprimée.")
            self.update_image_list()  # Mettre à jour la liste des images

    def rename_photo(self):
        # Renommer la photo sélectionnée
        selected_index = self.listbox_images.curselection()
        if selected_index:
            selected_photo = self.listbox_images.get(selected_index)
            new_name = simpledialog.askstring("Renommer la Photo", "Entrez le nouveau nom (sans extension) :")
            if new_name:
                new_name_with_extension = f"data/{new_name}.png"
                old_path = os.path.join("data", selected_photo)
                new_path = new_name_with_extension
                os.rename(old_path, new_path)  # Renommer le fichier
                messagebox.showinfo("Succès", f"Photo renommée en : {new_name_with_extension}")
                self.update_image_list()  # Mettre à jour la liste des images

    def update_image_list(self):
        # Mettre à jour la liste des images
        self.listbox_images.delete(0, tk.END)  # Effacer la liste existante
        images = [f for f in os.listdir("data") if os.path.isfile(os.path.join("data", f))]
        for img_file in images:
            self.listbox_images.insert(tk.END, img_file)

        # Désactiver les boutons de suppression et de renommage s'il n'y a pas d'image sélectionnée
        self.button_delete.config(state=tk.DISABLED)
        self.button_rename.config(state=tk.DISABLED)

    def on_closing(self):
        # Libérer les ressources de la caméra et fermer l'application
        self.is_running = False
        if self.cap.isOpened():
            self.cap.release()
        self.controller.destroy()

# if __name__ == "__main__":

#     def on_closing(self):
#         # Libérer les ressources de la caméra et fermer l'application
#         self.is_running = False
#         if self.cap.isOpened():
#             self.cap.release()
#         self.controller.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoBoothApp(root, root)
    app.pack(fill=tk.BOTH, expand=True)
    root.mainloop()
