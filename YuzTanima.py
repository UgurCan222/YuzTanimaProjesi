import os
import cv2
import face_recognition

# Yüzlerin bulunduğu klasörü belirleyelim
yuz_klasoru = "C:/Users/ugurc/Desktop/Yuzler"

# Yüzlerin isimlerini ve özelliklerini depolayacak sözlük
yuz_veritabani = {}

# Klasördeki tüm resimleri tarayalım
for dosya_adi in os.listdir(yuz_klasoru):
    # Dosya ismini ve uzantısını ayıralım
    ad, uzanti = os.path.splitext(dosya_adi)
    # Sadece JPEG/JPG/PNG formatındaki dosyaları işleyelim
    if uzanti in [".jpg", ".jpeg", ".png"]:
        # Resmi yükle ve yüzlerin koordinatlarını bul
        resim = face_recognition.load_image_file(os.path.join(yuz_klasoru, dosya_adi))
        yuz_konumlari = face_recognition.face_locations(resim)
        # Eğer resimde yüz yoksa, devam edelim
        if not yuz_konumlari:
            print(f"{dosya_adi} dosyasında yüz bulunamadı.")
            continue
        # Yüzün özelliklerini bul (burada yüzün sadece bir tanesi var)
        yuz_ozellikleri = face_recognition.face_encodings(resim, known_face_locations=yuz_konumlari)
        # Yüzün özelliklerini kaydet
        yuz_veritabani[ad] = yuz_ozellikleri[0]

# Video kaynağını aç
video_kaynagi = cv2.VideoCapture(0)

while True:
    # Kameradan bir kare oku
    ret, kare = video_kaynagi.read()

    # Kareyi BGR'den RGB'ye dönüştür
    rgb_kare = kare[:, :, ::-1]

    # Tüm yüzleri bul
    yuz_konumlari = face_recognition.face_locations(rgb_kare)
    # Yüzlerin özelliklerini bul
    yuz_ozellikleri = face_recognition.face_encodings(rgb_kare, known_face_locations=yuz_konumlari)

    # Her bir yüz için, en yakın yüz özelliklerini bul ve eşleşen ismi yazdır
    for yuz_ozelligi in yuz_ozellikleri:
        # Eşleşen yüzü bul
        eslesmeler = face_recognition.compare_faces(list(yuz_veritabani.values()), yuz_ozelligi)
        # Eşleşen yüz yoksa, isim olarak "Bilinmiyor" yazdır
        isim = "Bilinmiyor"
        if any(eslesmeler):
            # Yüz özelliklerine en yakın yüze karşılık gelen ismi bul
            eslesme_indexi = eslesmeler.index(True)
            isim = list(yuz_veritabani.keys())[eslesme_indexi]

        # Yüzün etrafına dikdörtgen çiz ve ismi yazdır
        for (top, right, bottom, left) in yuz_konumlari:
    # Dikdörtgeni çiz
            cv2.rectangle(kare, (left, top), (right, bottom), (0, 255, 0), 2)

    # İsmi yazdır
    cv2.rectangle(kare, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
    cv2.putText(kare, isim, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

# Kamerayı aç
    cv2.imshow('Video', kare)

# 'q' tuşuna basarak programı sonlandır
    if cv2.waitKey(1) & 0xFF == ord('q'):
                break

#Her şey bittiğinde, video kaynağını serbest bırak ve tüm pencereleri kapat
video_kaynagi.release()
cv2.destroyAllWindows()