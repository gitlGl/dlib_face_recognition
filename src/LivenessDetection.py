import cv2, numpy as np
from . import Setting
from .Setting import predictor,detector

#68个人脸特征中眼睛的位置
FACIAL_LANDMARKS_IDXS = {
                "mouth": (48, 68),
                "inner_mouth": (60, 68),
                "right_eyebrow": (17, 22),
                "left_eyebrow": (22, 27),
                "right_eye" : (36, 42),
                "left_eye" : (42, 48),
                "nose" : (27, 36),
                "jaw": (0, 17)

                }
lStart, lEnd = FACIAL_LANDMARKS_IDXS["left_eye"]
rStart, rEnd = FACIAL_LANDMARKS_IDXS["right_eye"]

mStart, mEnd = FACIAL_LANDMARKS_IDXS["mouth"]


def eyeAspectRatio(eye):
    """
    计算眼睛大小
    """
    A = np.linalg.norm(eye[1]- eye[5])
    B = np.linalg.norm(eye[2]-eye[4])
    C = np.linalg.norm(eye[0]- eye[3])

    ear = (A + B) / (2.0 * C)  #眼睛大小值
    return ear


def mouthAspectRatio(mouth):
    A = np.linalg.norm(mouth[2]-mouth[9])  # 51, 59
    B = np.linalg.norm(mouth[4]-mouth[7])  # 53, 57
    C = np.linalg.norm(mouth[0]-mouth[6])  # 49, 55
    mar = (A + B) / (2.0 * C)  #嘴巴大小值

    return mar

def compare2faces(list_img):  #对比两张人脸照片对比是否发生眨眼。两张照片眼睛距离大于0.05时认为发生眨眼

    rgbImage1 = cv2.cvtColor(list_img[0], cv2.COLOR_BGR2RGB)
    rgbImage2 = cv2.cvtColor(list_img[1], cv2.COLOR_BGR2RGB)
    rect1 = detector(rgbImage1, 0)
    rect2 = detector(rgbImage2, 0)
    list = []
    if (len(rect1) == 1) and (len(rect2)) == 1:
        list.append(computEye(rgbImage1, rect1))
        list.append(computEye(rgbImage2, rect2))
        result = abs(list[0] - list[1])
        if result >= Setting.EYE_AR_THRESH:
            return True
    return False


def shape2np(shape, dtype="int"):
    # initialize the list of (x, y)-coordinates
    coords = np.zeros((shape.num_parts, 2), dtype=dtype)

    # loop over all facial landmarks and convert them
    # to a 2-tuple of (x, y)-coordinates
    for i in range(0, shape.num_parts):
        coords[i] = (shape.part(i).x, shape.part(i).y)

    # return the list of (x, y)-coordinates
    return coords
#判断是否眨眼
def computEye(rgbImage, rect):
    shape = predictor(rgbImage, rect[0])
    shape = shape2np(shape)  #68个人脸特征坐标
    leftEye = shape[lStart:lEnd]
    rightEye = shape[rStart:rEnd]
    leftEAR = eyeAspectRatio(leftEye)
    rightEAR = eyeAspectRatio(rightEye)
    ear = (leftEAR + rightEAR) / 2.0  # 两个眼睛大小平均值
    return ear

#判断是否张开嘴巴
def computMouth(img):
    rgbImage = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    rect = detector(rgbImage, 0)
    if (len(rect) == 1):
        shape = predictor(rgbImage, rect[0])
        shape = shape2np(shape)  #68个人脸特征坐标
        mouth = shape[mStart:mEnd]
        mouth = mouthAspectRatio(mouth)
        if mouth >  Setting.MAR_THRESH:
            return True
    return False
