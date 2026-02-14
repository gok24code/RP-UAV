import cv2
import numpy as np

def qr_code_camera_scanner():
    cap = cv2.VideoCapture(0)
    
    # Çözünürlüğü drone/kamera standartlarına çekiyoruz
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    if not cap.isOpened():
        print("Hata: Kamera baglantisi saglanamadi.")
        return

    # Daha kararlı bir dedektör nesnesi
    detector = cv2.QRCodeDetector()

    while True:
        ret, frame = cap.read()
        if not ret: break

        h, w = frame.shape[:2]
        
        # --- GÖRSELDEKİ ORANLAR (%25 Yatay, %10 Dikey) ---
        off_x = int(w * 0.25)
        off_y = int(h * 0.10)
        
        x1, y1 = off_x, off_y
        x2, y2 = w - off_x, h - off_y

        # 1. TARAMA ALANI (ROI): Sadece sarı bölgeyi tarıyoruz
        # QR kodun bir kısmı dışarıda olsa bile bu alan içindeki kısmıyla tanınmasını sağlar
        roi = frame[y1:y2, x1:x2]

        # 2. QR ALGILAMA
        try:
            # detectAndDecode bazen kararsızdır, önce konumu netleştiriyoruz
            data, bbox, _ = detector.detectAndDecode(roi)
            
            if bbox is not None and len(bbox) > 0:
                points = bbox[0].astype(int)
                
                # Eğer geçerli bir alan bulunduysa çizim yap (Hata önleyici)
                if cv2.contourArea(points) > 10: 
                    # Kilitlenme Dörtgeni Çizimi (ROI -> Global koordinat dönüşümü)
                    for i in range(len(points)):
                        pt1 = (points[i][0] + x1, points[i][1] + y1)
                        pt2 = (points[(i + 1) % len(points)][0] + x1, points[(i + 1) % len(points)][1] + y1)
                        cv2.line(frame, pt1, pt2, (0, 0, 255), 3) # Kırmızı Kilit

                    # Veri metni ve etiket (Görseldeki gibi)
                    cv2.putText(frame, "Kilitlenme Dortgeni", (points[0][0] + x1, points[0][1] + y1 - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    
                    if data:
                        print(data)
                        cv2.putText(frame, f"DATA: {data}", (x1, y2 + 35), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        except:
            pass # Beklenmedik geometrik hatalarda sistemin çökmesini engeller

        # --- ARAYÜZ TASARIMI (İLK GÖRSEL İLE AYNI) ---
        
        # Mor Dış Çerçeve (Kamera Görüş Alanı)
        cv2.rectangle(frame, (0, 0), (w, h), (255, 0, 127), 3)
        cv2.putText(frame, "Kamera Gorus Alani", (15, h - 20), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

        # Sarı İç Çerçeve (Hedef Vuruş Alanı)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
        cv2.putText(frame, "Hedef Vurus Alani", (x1 + 10, y2 - 15), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

        # Oran Bilgilendirme Okları ve Yazıları (Dekoratif/Bilgilendirme)
        cv2.putText(frame, "%10 Dikey", (w // 2 - 40, y1 - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(frame, "%25 Yatay", (10, h // 2), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.putText(frame, "%100 Yatay", (w // 2 - 50, h - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        cv2.imshow('QR Mission UI', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    qr_code_camera_scanner()