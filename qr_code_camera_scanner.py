import cv2
import numpy as np

def qr_code_camera_scanner():
    cap = cv2.VideoCapture(0)
    
    # Görüntü kalitesi için çözünürlük ayarı
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    if not cap.isOpened():
        print("Hata: Kamera açılamadı.")
        return

    detector = cv2.QRCodeDetector()

    while True:
        ret, frame = cap.read()
        if not ret: break

        h, w = frame.shape[:2]
        
        # --- İDEAL DİKDÖRTGEN ORANLARI ---
        # %25 çok dardı, %15 çok genişti. %20 tam orta nokta.
        off_x = int(w * 0.20)  # Yatay boşluk
        off_y = int(h * 0.12)  # Dikey boşluk
        
        x1, y1 = off_x, off_y
        x2, y2 = w - off_x, h - off_y

        # 1. ROI (Yalnızca sarı bölge taranır)
        roi = frame[y1:y2, x1:x2]

        # 2. QR TARAMA VE KİLİTLENME
        try:
            # ROI içinde tarama yap
            data, bbox, _ = detector.detectAndDecode(roi)
            
            if bbox is not None and len(bbox) > 0:
                points = bbox[0].astype(int)
                
                # Alan kontrolü (Hatalı algılamayı önler)
                if cv2.contourArea(points) > 10:
                    # Kilitlenme Dörtgeni (Kırmızı)
                    for i in range(len(points)):
                        pt1 = (points[i][0] + x1, points[i][1] + y1)
                        pt2 = (points[(i + 1) % len(points)][0] + x1, points[(i + 1) % len(points)][1] + y1)
                        cv2.line(frame, pt1, pt2, (0, 0, 255), 3)

                    # Kilitlenme Yazısı
                    cv2.putText(frame, "Kilitlenme Dortgeni", (points[0][0] + x1, points[0][1] + y1 - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    
                    if data:
                        print("Veri okundu: " + data)
                        # Okunan datayı sarı kutunun altına yazdır
                        cv2.putText(frame, f"DATA: {data}", (x1, y2 + 35), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        except:
            pass

        # --- ARAYÜZ TASARIMI ---
        
        # Mor Dış Çerçeve (Kamera Görüş Alanı)
        cv2.rectangle(frame, (0, 0), (w, h), (255, 0, 127), 4)
        cv2.putText(frame, "Kamera Gorus Alani", (20, h - 20), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # Sarı Hedef Vuruş Alanı (Yeni Ölçülü Dikdörtgen)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
        cv2.putText(frame, "Hedef Vurus Alani", (x1 + 10, y2 - 15), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)


        cv2.imshow('QR Mission UI - Final Form', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    qr_code_camera_scanner()