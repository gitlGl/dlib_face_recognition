import cv2, numpy as np
from PyQt5.QtCore import QThread
from src.GlobalVariable import models

class LivenessDetection(QThread):
    def __init__(self):
        super().__init__()
        self.img1 = np.random.randint(255, size=(900, 800, 3), dtype=np.uint8)
        self.img2 = np.random.randint(255, size=(900, 800, 3), dtype=np.uint8)
      
        self.EYE_AR_THRESH = 0.3  #小于0.3时认为是闭眼状态
        self.MAR_THRESH = 0.5  #大于于0.5时认为是张嘴状态

        #68个人脸特征中眼睛的位置

        self.FACIAL_LANDMARKS_IDXS = {
	"mouth": (48, 68),
	"inner_mouth": (60, 68),
	"right_eyebrow": (17, 22),
	"left_eyebrow": (22, 27),
	"right_eye" : (36, 42),
	"left_eye" : (42, 48),
	"nose" : (27, 36),
	"jaw": (0, 17)
}


        self.lStart, self.lEnd = self.FACIAL_LANDMARKS_IDXS["left_eye"]
        self.rStart, self.rEnd = self.FACIAL_LANDMARKS_IDXS["right_eye"]
        #68个人脸特征中嘴巴的位置
        self.mStart, self.mEnd = self.FACIAL_LANDMARKS_IDXS["mouth"]

    def eye_aspect_ratio(self, eye):
        """
        计算眼睛大小
        """
        A = np.linalg.norm(eye[1]- eye[5])
        B = np.linalg.norm(eye[2]-eye[4])
        C = np.linalg.norm(eye[0]- eye[3])

        ear = (A + B) / (2.0 * C)  #眼睛大小值
        return ear

    #计算嘴巴张开大小
    def mouth__aspect_ratio(self, mouth):
        A = np.linalg.norm(mouth[2]-mouth[9])  # 51, 59
        B = np.linalg.norm(mouth[4]-mouth[7])  # 53, 57
        C = np.linalg.norm(mouth[0]-mouth[6])  # 49, 55
        mar = (A + B) / (2.0 * C)  #嘴巴大小值

        return mar

    def compare2faces(self, list_img):  #对比两张人脸照片对比是否发生眨眼。两张照片眼睛距离大于0.1时认为发生眨眼

        rgbImage1 = cv2.cvtColor(list_img[0], cv2.COLOR_BGR2RGB)
        rgbImage2 = cv2.cvtColor(list_img[1], cv2.COLOR_BGR2RGB)
        rect1 = models.detector(rgbImage1, 0)
        rect2 = models.detector(rgbImage2, 0)
        list = []
        if (len(rect1) == 1) and (len(rect2)) == 1:
            list.append(self.comput_eye(rgbImage1, rect1))
            list.append(self.comput_eye(rgbImage2, rect2))
            result = abs(list[0] - list[1])
            if result >= 0.05:

                return True
        return False
    def shape_to_np(self,shape, dtype="int"):
        # initialize the list of (x, y)-coordinates
        coords = np.zeros((shape.num_parts, 2), dtype=dtype)

        # loop over all facial landmarks and convert them
        # to a 2-tuple of (x, y)-coordinates
        for i in range(0, shape.num_parts):
            coords[i] = (shape.part(i).x, shape.part(i).y)

        # return the list of (x, y)-coordinates
        return coords
    #判断是否眨眼
    def comput_eye(self, rgbImage, rect):
        shape = models.predictor(rgbImage, rect[0])
        
        shape = self.shape_to_np(shape)  #68个人脸特征坐标
        leftEye = shape[self.lStart:self.lEnd]
        rightEye = shape[self.rStart:self.rEnd]
        leftEAR = self.eye_aspect_ratio(leftEye)
        rightEAR = self.eye_aspect_ratio(rightEye)
        ear = (leftEAR + rightEAR) / 2.0  # 两个眼睛大小平均值
        return ear

    #判断是否张开嘴巴
    def comput_mouth(self, img):
        rgbImage = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        rect = models.detector(rgbImage, 0)
        if (len(rect) == 1):
            shape = models.predictor(rgbImage, rect[0])
            shape = self.shape_to_np(shape)  #68个人脸特征坐标
            mouth = shape[self.mStart:self.mEnd]
            mouth = self.mouth__aspect_ratio(mouth)
            if mouth > 0.5:
                return True
        return False
