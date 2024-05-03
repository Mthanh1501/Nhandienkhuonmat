import cv2
# from plugin import FileHandle as f
import numpy as np
import time
import os
from PIL import Image
from PyQt6.QtWidgets import QWidget, QMessageBox
import unicodedata

from GUI import StaffDetailGUI

class FaceRecognitionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.path = 'plugin/Img'
        self.detector = cv2.CascadeClassifier('plugin/haarcascade_frontalface_default.xml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.staffDetailWidget = StaffDetailGUI.StaffDetailGUI()

    def faceDetect(self,id,name):
        cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        w = 640
        cam.set(cv2.CAP_PROP_FRAME_WIDTH, w)
        h = 480
        cam.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
        info = 'plugin/ID.txt'
        count = 0

        print(f'Create new user: {id} - {name}')
        with open(info, 'a', encoding='utf-8') as f:
            f.write(f'{id} - {name}\n')

        # with open(info, 'a') as file:
        #     file.write(f'{id} - {name}\n')
        #     print("oke")

        while True:
            ret, img = cam.read()
            if not ret:
                print("Failed to grab frame")
                break
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.detector.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                count += 1
                normalized_name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('ASCII')
                # normalized_name = name.encode('utf-8')
                # normalized_name = unicodedata.normalize('NFKD', name)
                # utf8_encoded_name = normalized_name.encode('utf-8')
                # utf8_decoded_name = utf8_encoded_name.decode('utf-8')
                face_img_path = os.path.join(self.path, f'{id} {normalized_name} {count}.jpg')
                print("Saving image to:", face_img_path)
                cv2.imwrite(face_img_path, gray[y:y+h, x:x+w])
                cv2.imshow('Images', img)

            time.sleep(0.1)

            pic_limit = 20
            k = cv2.waitKey(1) & 0xff
            if k == 27 or count >= pic_limit:
                print("Exit condition met")
                break
        
        print('Exit')
        cam.release()
        cv2.destroyAllWindows()
        self.trainRecognizer()
        QMessageBox.information(self, "Face Detection", "Chụp hình thành công")

    def trainRecognizer(self):
        print('Training data...')
        faces, ids = self.getImageAndLabel(self.path)
        self.recognizer.train(faces, np.array(ids))
        self.recognizer.write('plugin/Trainer/train.yml')
        print('{0} khuôn mặt được train.'.format(len(np.unique(ids))))
        # QMessageBox.information(self, "Recognizer Training", "Recognizer training completed.")

    def getImageAndLabel(self, path):
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        faceSample = []
        ids = []
        
        for imagePath in imagePaths:
            PIL_Image = Image.open(imagePath).convert('L')
            img_numpy = np.array(PIL_Image, 'uint8')
            
            id = int(os.path.split(imagePath)[-1].split('.')[0].split(' ')[0])
            faces = self.detector.detectMultiScale(img_numpy)
            
            for (x, y, w, h) in faces:
                faceSample.append(img_numpy[y:y+h, x:x+w])
                ids.append(id)
                
        return faceSample, ids
