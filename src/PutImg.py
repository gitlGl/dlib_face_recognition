import copy
from PySide6.QtCore import QTimer
import numpy as np
from PySide6.QtCore import Signal
from . import LivenessDetection
from .Capture import Capture
class PutImg(Capture):
    """
   用于启动普通识别模式
    """

    emit_result = Signal(str)
    emit_text = Signal(str)

    def __init__(self, Q_put, Q_get):
        super().__init__()

        self.list_img = []
        self.timer_collectFrame = QTimer()
        self.timer_collectFrame.timeout.connect(self.collectFrame)
        self.timer_getResult = QTimer()
        self.timer_getResult.timeout.connect(self.getResult)
        self.timer_toPut = QTimer()
        self.timer_toPut.timeout.connect(self.toPut)
        self.Q_put = Q_put
        self.Q_get = Q_get
        self.frame = np.random.randint(255, size=(900, 800, 3),
                                       dtype=np.uint8)  #初始化
        self.flag = False
    #获取判断结果后把帧通过队列发送到子进程进行人脸识别
    def toPut(self):
        self.timer_toPut.stop()
        #控制队列数量为1
        if self.Q_put.empty()  and self.Q_get.empty() :
            self.Q_put.put(self.frame)
        if not self.Q_get.empty():
            self.emit_result.emit(self.Q_get.get())

        self.timer_toPut.start(1000)
    #获取两帧（间隔0.2s）判断是否发生眨眼
    def collectFrame(self):
        self.timer_collectFrame.stop()
        if not self.flag:
            img = copy.deepcopy(self.frame)
            flag = LivenessDetection.computMouth(img)
            if flag:
                self.flag = True
                self.emit_text.emit("提示：请看镜头眨眼睛")
            self.timer_collectFrame.start(200)   
            return
     
        if len(self.list_img) < 2:
            self.list_img.append(self.frame)
        else:
            list_img = copy.deepcopy(self.list_img)
            flag = LivenessDetection.compare2faces(list_img)
            if flag:
                self.flag = False
                self.Q_put.put(self.list_img[0])
                self.timer_getResult.start(1000)
                self.list_img.clear()
                return
            self.list_img.clear()
        self.timer_collectFrame.start(200)
    #获取判断结果
    def getResult(self):
        self.timer_getResult.stop()
        if self.Q_get.qsize() != 0:
            self.emit_result.emit(self.Q_get.get())
            
            #self.emit_text.emit("提示：请张嘴")
            self.timer_collectFrame.start(200)
        else:
            self.timer_getResult.start(1000)
