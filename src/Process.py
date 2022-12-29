import cv2,dlib
from src.GlobalVariable import models
from src.Face import StudentRgFace
import time

#此用于面部特征计算进程
def process_student_rg(Q1, Q2, share):
    face_rg = StudentRgFace()
    while True:
        while not Q1.empty():
            rgbImage = Q1.get()
            location_faces = models.detector(rgbImage)
            if len(location_faces) == 1:
                img = rgbImage
                faces = models.detector(rgbImage)
                dets = models.detector(rgbImage, 0)
                faces = dlib.full_object_detections()
                for detection in dets:
                    faces.append(models.predictor(rgbImage, detection))
                rgbImage = dlib.get_face_chip(rgbImage, faces[0])
                rgbImage = cv2.cvtColor(rgbImage, cv2.COLOR_BGR2RGB)
                gray = cv2.cvtColor(rgbImage, cv2.COLOR_RGB2GRAY)
                location_faces = models.detector(rgbImage)
                if len(location_faces) == 1:
                    raw_face = models.predictor(gray, location_faces[0])
                    result = face_rg.rg(img, rgbImage, raw_face, share)
                    Q2.put(result)

        time.sleep(0.5)


# def process_admin_rg(Q1, share):
#     face_rg = AdminRgFace()
#     while True:
#         while not Q1.empty():
#             img = Q1.get()
#             rgbImage = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#             gray = cv2.cvtColor(rgbImage, cv2.COLOR_RGB2GRAY)
#             location_faces = models.detector(gray)
#             if len(location_faces) == 1:
#                 raw_face = models.predictor(gray, location_faces[0])
#                 result = face_rg.rg_face(img, rgbImage, raw_face,share)
