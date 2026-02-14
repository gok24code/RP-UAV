import cv2

# Install necessary libraries if you haven't already:
# pip install opencv-python

def qr_code_camera_scanner():
    cap = cv2.VideoCapture(0)  # 0 for default webcam

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    # Create a QRCodeDetector object
    detector = cv2.QRCodeDetector()

    print("QR Code Camera Scanner Started. Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        # Detect and decode QR codes
        # data: decoded string
        # bbox: bounding box of the detected QR code
        # rectifiedImage: rectified image of the QR code
        data, bbox, rectifiedImage = detector.detectAndDecode(frame)

        if bbox is not None:
            # Display the bounding box
            for i in range(len(bbox[0])):
                # Draw all lines of the bounding box
                pt1 = (int(bbox[0][i][0]), int(bbox[0][i][1]))
                pt2 = (int(bbox[0][(i + 1) % len(bbox[0])][0]), int(bbox[0][(i + 1) % len(bbox[0])][1]))
                cv2.line(frame, pt1, pt2, (0, 255, 0), 3)

            if data:
                print(f"QR Code Detected: {data}")
                # Put the decoded data text near the QR code
                # Get the top-left corner of the bounding box
                x = int(bbox[0][0][0])
                y = int(bbox[0][0][1])
                cv2.putText(frame, data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        cv2.imshow('QR Code Camera Scanner', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    qr_code_camera_scanner()
