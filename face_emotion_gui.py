import cv2
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont
import threading
import os
import numpy as np
from deepface import DeepFace

# Yüz, göz ve gülümseme için Haar Cascade dosyalarını yüklüyoruz
yuz_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
go_z_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
gulumseme_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')

# Duygu etiketlerini Türkçeye çeviren eşleştirme sözlüğü
emotion_map = {
    "happy": "Mutlu 😊",
    "sad": "Üzgün 😢",
    "angry": "Kızgın 😠",
    "fear": "Korkmuş 😨",
    "surprise": "Şaşkın 😲",
    "disgust": "İğrenmiş 😒",
    "neutral": "Nötr 😐"
}

# Tkinter penceresini oluşturuyoruz
root = tk.Tk()
root.title("Yüz, Göz, Gülümseme ve Duygu Analizi")

# Ekranda gösterilecek etiketler (analiz sonucu ve görsel)
result_label = tk.Label(root, text="Durum: -", font=("Segoe UI", 14))
result_label.pack(pady=10)

img_label = tk.Label(root)
img_label.pack()

# Analiz fonksiyonu
def analyze_frame(image):
    try:
        result = DeepFace.analyze(image, actions=['emotion'], enforce_detection=False)
        emotion = result[0]['dominant_emotion']
        turkce = emotion_map.get(emotion, "Bilinmeyen 😐")
        durum = f"Duygu: {turkce}"

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = yuz_cascade.detectMultiScale(gray, 1.1, 4)

        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = image[y:y + h, x:x + w]

            eyes = go_z_cascade.detectMultiScale(roi_gray, 1.1, 10)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

            smiles = gulumseme_cascade.detectMultiScale(roi_gray, 1.7, 22)
            for (sx, sy, sw, sh) in smiles:
                cv2.rectangle(roi_color, (sx, sy), (sx + sw, sy + sh), (0, 0, 255), 2)

        # Türkçe karakter destekli yazı
        image_pil = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(image_pil)
        try:
            font = ImageFont.truetype("arial.ttf", 32)
        except:
            font = ImageFont.load_default()

        draw.text((20, 20), durum, font=font, fill=(255, 255, 0))
        image = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)

        return image, durum
    except Exception:
        return image, "Duygu algılanamadı"

# Kamera başlatma fonksiyonu
def start_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        result_label.config(text="⚠️ Kamera açılamadı!")
        return

    def run_camera():
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame, durum = analyze_frame(frame)
            cv2.imshow("Kamera - Yüz, Göz, Gülümseme ve Duygu Tespiti", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    threading.Thread(target=run_camera).start()

# Resim yükleyip analiz eden fonksiyon
def upload_image():
    file_path = filedialog.askopenfilename(filetypes=[("Görsel dosyaları", "*.jpg *.jpeg *.png")])
    if not file_path:
        return

    safe_path = os.path.normpath(file_path)
    image = cv2.imread(safe_path)
    if image is None:
        result_label.config(text="⚠️ Resim okunamadı!")
        return

    image, durum = analyze_frame(image)
    result_label.config(text=durum)

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(image_rgb)
    img_tk = ImageTk.PhotoImage(img_pil)
    img_label.config(image=img_tk)
    img_label.image = img_tk

# Arayüz butonları
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

cam_btn = tk.Button(btn_frame, text="Kamera ile Tara", command=start_camera, font=("Arial", 12), width=20)
cam_btn.pack(side=tk.LEFT, padx=10)

img_btn = tk.Button(btn_frame, text="Resim Yükle ve Tara", command=upload_image, font=("Arial", 12), width=20)
img_btn.pack(side=tk.LEFT, padx=10)

root.mainloop()
