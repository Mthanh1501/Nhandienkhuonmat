import cv2, os
import numpy as np
from PIL import Image

path = 'plugin/Img'
reconizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier('plugin/haarcascade_frontalface_default.xml')

def getImageAndLabel(path):
    # imagePaths = []
    # for f in os.listdir(path):
    #     i = os.path.join(path, f)
    #     imagePaths.append(i)
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faceSample = []
    ids = []
    
    for imagePath in imagePaths:
        PIL_Image = Image.open(imagePath).convert('L')
        img_numpy = np.array(PIL_Image, 'uint8')
        
        id = int(os.path.split(imagePath)[-1].split('.')[0].split(' ')[0])
        # print(id)
        faces = detector.detectMultiScale(img_numpy)
        
        for (x, y, w, h) in faces:
            faceSample.append(img_numpy[y:y+h, x:x+w])
            ids.append(id)
            
    return faceSample, ids

print('Training data...')
faces, ids = getImageAndLabel(path)

# print(faces, ids)

reconizer.train(faces, np.array(ids))
reconizer.write('plugin/Trainer/train.yml')

print('{0} khuon mat duoc train.'.format(len(np.unique(ids))))