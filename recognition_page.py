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
        self.label_title = tk.Label(self, text="RECONNAISSANCE", font=("Arial", 30, "bold"), bg="#3e4149", fg="#ffcc00")
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
        # Dossier contenant les images des visages connus
        known_faces_folder = "data"
        valid_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]

        if not os.path.exists(known_faces_folder):
            messagebox.showerror("Erreur", f"Le dossier '{known_faces_folder}' n'existe pas.")
            return
        
        # Liste des chemins d'images valides dans le dossier
        known_image_paths = [os.path.join(known_faces_folder, img) for img in os.listdir(known_faces_folder) if any(img.lower().endswith(ext) for ext in valid_extensions)]

        if not known_image_paths:
            messagebox.showwarning("Avertissement", "Aucune image trouvée dans le dossier 'data'.")
            return

        for image_path in known_image_paths:
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)

            if encodings:
                encoding = encodings[0]
                name = os.path.splitext(os.path.basename(image_path))[0]

                # Exemple d'informations supplémentaires
                info = {
                    "prenom": "Prénom_" + name,
                    "numero_detenu": "Numéro_" + name,
                    "nom": name.capitalize()
                }
                self.face_info[name] = info  # Stocker les informations dans le dictionnaire

                self.known_face_encodings.append(encoding)
                self.known_face_names.append(name)
            else:
                messagebox.showwarning("Avertissement", f"Aucun visage détecté dans l'image '{image_path}'.")

    def update_frame(self):
        if not self.is_running:
            return

        ret, frame = self.cap.read()
        
        if not ret:
            messagebox.showerror("Erreur", "Impossible de lire le flux vidéo.")
            return

        # Redimensionner le cadre pour accélérer le traitement
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        
        # Convertir l'image de BGR à RGB
        rgb_small_frame = small_frame[:, :, ::-1]

        if self.process_this_frame:
            # Trouver toutes les positions de visages et les encodages dans le cadre actuel
            self.face_locations = face_recognition.face_locations(rgb_small_frame, model="cnn")  # Utiliser un modèle CNN
            self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

            # Réinitialiser les noms des visages pour ce cadre
            self.face_names = []

            for face_encoding in self.face_encodings:
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = "Inconnu"

                # Utiliser le visage connu avec la plus petite distance par rapport au nouveau visage
                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index] and face_distances[best_match_index] < 0.5:  # Utiliser un seuil de confiance plus strict
                    name = self.known_face_names[best_match_index]

                self.face_names.append(name)

            # Mettre à jour l'affichage du visage reconnu et les informations
            recognized_name = None
            for name in self.face_names:
                if name != "Inconnu":
                    recognized_name = name
                    break
            
            if recognized_name:
                # Vérifiez chaque extension pour les images reconnues
                image_path = None
                for ext in [".jpg", ".jpeg", ".png", ".bmp", ".tiff"]:
                    candidate_path = os.path.join("data", recognized_name + ext)
                    if os.path.exists(candidate_path):
                        image_path = candidate_path
                        break

                if image_path:
                    img = Image.open(image_path)
                    img.thumbnail((400, 400))  # Redimensionner l'image pour l'affichage
                    img_tk = ImageTk.PhotoImage(img)
                    self.recognized_face_label.config(image=img_tk)
                    self.recognized_face_label.image = img_tk  # Garder une référence à l'image

                    # Afficher les informations sous la photo reconnue
                    info = self.face_info.get(recognized_name, {})
                    display_info = f"Nom: {info.get('nom', 'Inconnu')}\nPrénom: {info.get('prenom', 'Inconnu')}\nNuméro de détenu: {info.get('numero_detenu', 'Inconnu')}"
                    self.recognized_face_info_label.config(text=display_info)

                    # Jouer un son d'alarme si le nom est "JOSUE"
                    if recognized_name.upper() == "JOSUE":
                        playsound(os.path.abspath('audios/zombi.mp3'))
                        
                else:
                    self.recognized_face_label.config(image='')
                    self.recognized_face_label.image = None
                    self.recognized_face_info_label.config(text="")

          
             # Si aucune personne reconnue, effacer l'image affichée et afficher "Inconnu"
            else:
                self.recognized_face_label.config(image='')
                self.recognized_face_label.image = None
                self.recognized_face_info_label.config(text="Inconnu")

            # Dessiner des rectangles autour des visages reconnus avec des couleurs différentes
            for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
                color = (0, 255, 0) if name != "Inconnu" else (255, 0, 0)  # Vert pour reconnu, rouge pour inconnu
                cv2.rectangle(frame, (left * 4, top * 4), (right * 4, bottom * 4), color, 2)
                cv2.putText(frame, name, (left * 4 + 6, top * 4 - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)

        # Afficher l'image résultante dans le canvas
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.canvas_camera.create_image(0, 0, anchor=tk.NW, image=imgtk)
        self.canvas_camera.imgtk = imgtk

        # Traiter le prochain cadre
        self.process_this_frame = not self.process_this_frame
        self.after(10, self.update_frame)

    def on_closing(self):
        self.is_running = False
        self.cap.release()
        self.controller.destroy()

# Exemple d'utilisation
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    app = FaceRecognition(root, root)  # Remplacez root par votre contrôleur réel si nécessaire
    app.pack(fill=tk.BOTH, expand=True)
    root.mainloop()
