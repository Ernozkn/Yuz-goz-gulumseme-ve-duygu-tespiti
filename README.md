# 🧠 Yüz, Göz, Gülümseme ve Duygu Tespiti Sistemi

Bu proje, OpenCV’nin Haar Cascade sınıflandırıcılarını ve DeepFace kütüphanesini kullanarak bir kişinin **yüzünü, gözlerini, gülümsemesini** ve **duygusal durumunu** (mutlu, üzgün, kızgın vb.) gerçek zamanlı olarak analiz eden bir yapay zekâ uygulamasıdır.

---

## 🎯 Projenin Amacı

Bu projenin amacı, kameradan alınan görüntülerde insan yüzünü, gözünü, gülümsemeyi ve duygu durumunu doğru ve etkili şekilde tespit eden bir sistem geliştirmektir. Sistem, sosyal robotlar, eğlence uygulamaları, güvenlik sistemleri ve insan-bilgisayar etkileşimi gibi alanlarda kullanılabilir.

---

## 👥 Hedef Kullanıcı Kitlesi

- Yapay zekâ ve bilgisayarla görü konularına ilgi duyan öğrenciler  
- İnsan davranış analizi geliştiren yazılım geliştiriciler  
- Görüntü işleme üzerine çalışan akademisyenler  

---

## 🧰 Kullanılan Teknolojiler

- Python 3.10  
- OpenCV 4.x  
- Haar Cascade XML sınıflandırıcıları  
- DeepFace (Keras/Tensorflow tabanlı duygu analizi)  
- NumPy  
- Tkinter (GUI arayüzü)  
- PIL (Pillow - Görsel işlemler için)

---

## ⚙️ Kurulum Adımları

```bash
# Gerekli kütüphaneleri yükleyin
pip install opencv-python numpy deepface pillow tk

🚀 Kullanım
bash
Kopyala
Düzenle
python face_emotion_gui.py
Uygulama açıldığında ekranda bir arayüz görünür.

"Kamera ile Tara" butonuyla canlı tespit yapılabilir.

"Resim Yükle ve Tara" butonuyla yüklü görselde analiz yapılabilir.

