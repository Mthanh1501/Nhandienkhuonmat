import cv2
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtCore import pyqtSignal


class FaceRecognitionThread(QThread):
    face_detected = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.cam = cv2.VideoCapture(0)  # Mở camera
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read('plugin/Trainer/train.yml')
        self.faceCascade = cv2.CascadeClassifier(
            'plugin/haarcascade_frontalface_default.xml')

        # Đọc danh sách tên từ tệp ID.txt
        self.ids = []
        self.names = []
        with open('plugin/ID.txt', 'r', encoding='utf-8') as file:
            for line in file:
                self.ids.append(line.split(' - ')[0].strip())
                self.names.append(line.split(' - ')[1].strip())

    def run(self):
        minW = 0.1 * self.cam.get(3)
        minH = 0.1 * self.cam.get(4)
        while True:
            ret, img = self.cam.read()
            if ret:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                # Phát hiện khuôn mặt
                faces = self.faceCascade.detectMultiScale(
                    gray,
                    scaleFactor=1.2,
                    minNeighbors=5,
                    minSize=(int(minW), int(minH))
                )

                for (x, y, w, h) in faces:
                    # Nhận dạng khuôn mặt

                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

                    id, confidence = self.recognizer.predict(gray[y:y + h, x:x + w])
                    print("-------------------------")
                    index = 0
                    print(id)
                    print(self.ids)
                    for i in self.ids:
                        if id == int(i):
                            break
                        index += 1

                    if 40 < confidence < 100:
                        name = self.names[index]
                        id = self.ids[index]
                        print("-------------------------")
                        confidence_str = f"{100 - confidence:.0f}%"
                    else:
                        name = "Unknown"
                        id = "Unknown"
                        confidence_str = f"{confidence:.0f}%"
                    # # Gửi tín hiệu đến GUI
                    cv2.putText(img, str(id), (x+5, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 1, cv2.LINE_AA)

                    
                    print(confidence_str + "  +  " + name + " + " + str(id))
                    self.face_detected.emit(name, str(id))

    def stop(self):
        self.cam.release()
