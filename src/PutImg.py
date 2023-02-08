import copy
from PyQt5.QtCore import QTimer
import numpy as np
from PyQt5.QtCore import pyqtSignal
from .LivenessDetection import LivenessDetection
from .GlobalVariable import GlobalFlag
from .Capture import Capture
class PutImg(Capture):
    """
   用于启动普通识别模式
    """

    emit_result = pyqtSignal(str)
    emit_text = pyqtSignal(str)

    def __init__(self, Q1, Q2):
        super().__init__()

        self.list_img = []
        self.livecheck  = LivenessDetection()
        self.timer1 = QTimer()
        self.timer1.timeout.connect(self.collectFrame)
        self.timer2 = QTimer()
        self.timer2.timeout.connect(self.getFesult)
        self.timer3 = QTimer()
        self.timer3.timeout.connect(self.toPut)
        self.Q1 = Q1
        self.Q2 = Q2
        self.frame = np.random.randint(255, size=(900, 800, 3),
                                       dtype=np.uint8)  #初始化
    #获取判断结果后把帧通过队列发送到子进程进行人脸识别
    def toPut(self):
        self.timer3.stop()
        #控制队列数量为1
        if self.Q1.empty()  and self.Q2.empty() :
            self.Q1.put(self.frame)
        if not self.Q2.empty():
            self.emit_result.emit(self.Q2.get())

        self.timer3.start(1000)
    #获取两帧（间隔0.2s）判断是否发生眨眼
    def collectFrame(self):
        self.timer1.stop()
        if not GlobalFlag.gflag2:
            img = copy.deepcopy(self.frame)
            flag = self.livecheck.computMouth(img)
            if flag:
                GlobalFlag.gflag2 = True
                self.emit_text.emit("提示：请看镜头眨眼睛")
            self.timer1.start(200)   
            return
     
        if len(self.list_img) <= 1:
            self.list_img.append(self.frame)
        elif len(self.list_img) == 2:
            list_img = copy.deepcopy(self.list_img)
            flag = self.livecheck.compare2faces(list_img)
            if flag:
                GlobalFlag.gflag2 = False
                self.Q1.put(self.list_img[0])
                self.timer2.start(1000)
                self.list_img.clear()
                return
            self.list_img.clear()
        self.timer1.start(200)
    #获取判断结果
    def getFesult(self):
        self.timer2.stop()
        if self.Q2.qsize() != 0:
            self.emit_result.emit(self.Q2.get())
            
            #self.emit_text.emit("提示：请张嘴")
            self.timer1.start(200)
        else:
            self.timer2.start(1000)
