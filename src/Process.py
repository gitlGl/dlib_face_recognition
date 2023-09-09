import cv2,dlib
from .Setting import predictor,detector
from .Face import StudentRgFace
import time

#此用于面部特征计算进程
def processStudentRg(Q1, Q2, share):
    face_rg = StudentRgFace()
    while share.value < 10:#作为进程退出的标志
        while not Q1.empty():
            rgbImage = Q1.get()
            img = rgbImage
            rgbImage = cv2.cvtColor(rgbImage, cv2.COLOR_BGR2RGB)
            location_faces = detector(rgbImage)
            if len(location_faces) == 1:
                raw_face = predictor(rgbImage, location_faces[0])
                #rgbImage = dlib.get_face_chip(rgbImage, face)
            
                result = face_rg.rg(img, rgbImage, raw_face, share)
                Q2.put(result)

        time.sleep(1)


