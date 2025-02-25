import cv2

file_path = "/home/admins/DjangoProject1/my_app/uploads/yes.mp4"

cap = cv2.VideoCapture(file_path)

if cap.isOpened():
    print(f"✅ OpenCV successfully opened the video: {file_path}")
else:
    print(f"❌ OpenCV cannot open the video file.")

cap.release()
