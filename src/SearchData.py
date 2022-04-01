from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt,QSize
from  PyQt5.QtWidgets import QWidget,QTableWidget,QTableWidgetItem,QVBoxLayout,QMenu,QHeaderView,QMessageBox, QDialog,QHBoxLayout
from src.UpdateData import UpdateData
from PyQt5 import QtWidgets
from PyQt5.QtCore import QPoint,pyqtSlot,Qt
from PyQt5.QtCore import QPointF, Qt, QRectF, QSizeF
from PyQt5.QtGui import QPainter, QColor, QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsPixmapItem, QGraphicsScene
import os
class SearchData(QWidget):
    def __init__(self ):
        super().__init__()
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)#允许右键显示上菜单
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)#禁止用户编辑单元格
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)#表示均匀拉直表头
        # self.qlineedit = QLineEdit()
        # self.qlineedit.setPlaceholderText('Please enter your usernumber')
        # self
        self.tableWidget.customContextMenuRequested[QPoint].connect(self.context_menu)#菜单右键槽函数
        self.tableWidget.cellDoubleClicked.connect(self.on_tableWidget_cellDoubleClicked)
        self.VBoxLayout = QVBoxLayout()
        self.VBoxLayout.addWidget(self.tableWidget)
        self.setLayout(self.VBoxLayout)
        self.tableWidget.setColumnCount(4)
       
        
        self.tableWidget.setHorizontalHeaderLabels([ '学号', '姓名', '性别',"图片" ])
    def set_information(self,information):
        self.information = information#信息来源
        row = 0
        self.tableWidget.setRowCount(0)
        print(len(self.information))
        for i in self.information:
            self.tableWidget.insertRow(row)
            sid_item = QTableWidgetItem(str(i["id_number"]))
            name_item = QTableWidgetItem(i["user_name"])
            if  i["gender"] == 0:
                i["gender"] = "女"
            else:
                i["gender"] = "男"
            sex_item = QTableWidgetItem(i["gender"])
            img_item =  QTableWidgetItem()
            self.tableWidget.setIconSize(QSize(60, 100))
            imag_path = "img_information/student/{0}/{1}.jpg".format(i["id_number"],i["id_number"])
            img_item.setIcon(QIcon(imag_path))
            sid_item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
            name_item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
            sex_item.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
            
            self.tableWidget.setItem(row, 0, sid_item)
            self.tableWidget.setItem(row, 1, name_item)
            self.tableWidget.setItem(row, 2, sex_item)
            self.tableWidget.setItem(row, 3,img_item)
            row = row + 1
            self.tableWidget.setRowCount(row)
      
           
    def on_tableWidget_cellDoubleClicked(self, row, column):#双击槽函数 self.tableWidget.cellDoubleClicked.connect()
        update_data = UpdateData(self.information[row])
        ok = update_data.exec_()
        print("是否",ok)
        if not ok:
            return
        user_name = update_data.user_name_line.text()
        id_number = update_data.id_number_line.text()
        gender = update_data.gender_line.text()
        #变更信息后修改信息
        self.information[row]["id_number"] = int(id_number)
        self.information[row]["user_name"] = user_name
        self.information[row]["gender"] = gender

        self.tableWidget.item(row, 0).setText(id_number)
        self.tableWidget.item(row, 1).setText(user_name)
        self.tableWidget.item(row, 2).setText(gender)
    @pyqtSlot(QPoint)
    def context_menu(self,pos):
        print("测试",pos)
        pop_menu = QMenu()
        #菜单事件信号
        change_new_event = pop_menu.addAction("修改")
        delete_event = pop_menu.addAction("删除")
        imageView_event = pop_menu.addAction("查看图片")
        item = self.tableWidget.itemAt(pos)
        if item != None:
            row = item.row()
            update_data = UpdateData(self.information[row])
            action = pop_menu.exec_(self.tableWidget.mapToGlobal(pos))#显示菜单列表，pos为菜单栏坐标位置
            if action == change_new_event:
                user_name = update_data.user_name_line.text()
                id_number = update_data.id_number_line.text()
                gender = update_data.gender_line.text()
                ok = update_data.exec_()
                if not ok:
                    return
                user_name = update_data.user_name_line.text()
                id_number = update_data.id_number_line.text()
                gender = update_data.gender_line.text()
            #变更信息后修改信息
                self.information[row]["id_number"] = int(id_number)
                self.information[row]["user_name"] = user_name
                self.information[row]["gender"] = gender
            #变更表格信息
                self.tableWidget.item(item.row(), 0).setText(id_number)
                self.tableWidget.item(item.row(), 1).setText(user_name)
                self.tableWidget.item(item.row(), 2).setText(gender)
            elif action == delete_event:
                r = QMessageBox.warning(self, "注意", "删除可不能恢复了哦！", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if r == QMessageBox.No:
                   return
                update_data.delete(int(self.information["id_number"]))
                self.tableWidget.clear()    
            elif action == imageView_event:
                imag_path = "img_information/student/{0}/{1}.jpg".format(str(self.information[row]["id_number"]),str(self.information[row]["id_number"]))
                show_imag = ShowImage(imag_path,Qt.WhiteSpaceMode)
                show_imag.exec_()


class ImageView(QGraphicsView):
    """图片查看控件"""

    def __init__(self, imag,  background):
        
        super(ImageView, self).__init__()
        self.setWindowModality(Qt.ApplicationModal)
        image = imag
        background =background
        self.setCursor(Qt.OpenHandCursor)
        self.setBackground(background)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing |
                            QPainter.SmoothPixmapTransform)
        self.setCacheMode(self.CacheBackground)
        self.setViewportUpdateMode(self.SmartViewportUpdate)
        self._item = QGraphicsPixmapItem()  # 放置图像
        self._item.setFlags(QGraphicsPixmapItem.ItemIsFocusable |
                            QGraphicsPixmapItem.ItemIsMovable)
        self._scene = QGraphicsScene(self)  # 场景
        self.setScene(self._scene)
        self._scene.addItem(self._item)
        rect = QApplication.instance().desktop().availableGeometry(self)
        self.resize(int(rect.width() * 2 / 3), int(rect.height() * 2 / 3))

        self.pixmap = None
        self._delta = 0.1  # 缩放
        self.setPixmap(image)

    def setBackground(self, color):
        """设置背景颜色
        :param color: 背景颜色
        :type color: QColor or str or GlobalColor
        """
        if isinstance(color, QColor):
            self.setBackgroundBrush(color)
        elif isinstance(color, (str, Qt.GlobalColor)):
            color = QColor(color)
            if color.isValid():
                self.setBackgroundBrush(color)

    def setPixmap(self, pixmap, fitIn=True):
        """加载图片
        :param pixmap: 图片或者图片路径
        :param fitIn: 是否适应
        :type pixmap: QPixmap or QImage or str
        :type fitIn: bool
        """
        if isinstance(pixmap, QPixmap):
            self.pixmap = pixmap
        elif isinstance(pixmap, QImage):
            self.pixmap = QPixmap.fromImage(pixmap)
        elif isinstance(pixmap, str) and os.path.isfile(pixmap):
            self.pixmap = QPixmap(pixmap)
        else:
            return
        self._item.setPixmap(self.pixmap)
        self._item.update()
        self.setSceneDims()
        if fitIn:
            self.fitInView(QRectF(self._item.pos(), QSizeF(
                self.pixmap.size())), Qt.KeepAspectRatio)
        self.update()

    def setSceneDims(self):
        if not self.pixmap:
            return
        self.setSceneRect(QRectF(QPointF(0, 0), QPointF(self.pixmap.width(), self.pixmap.height())))

    def fitInView(self, rect, flags=Qt.IgnoreAspectRatio):
        """剧中适应
        :param rect: 矩形范围
        :param flags:
        :return:
        """
        if not self.scene() or rect.isNull():
            return
        unity = self.transform().mapRect(QRectF(0, 0, 1, 1))
        self.scale(1 / unity.width(), 1 / unity.height())
        viewRect = self.viewport().rect()
        sceneRect = self.transform().mapRect(rect)
        x_ratio = viewRect.width() / sceneRect.width()
        y_ratio = viewRect.height() / sceneRect.height()
        if flags == Qt.KeepAspectRatio:
            x_ratio = y_ratio = min(x_ratio, y_ratio)
        elif flags == Qt.KeepAspectRatioByExpanding:
            x_ratio = y_ratio = max(x_ratio, y_ratio)
        self.scale(x_ratio, y_ratio)
        self.centerOn(rect.center())

    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            self.zoomIn()
        else:
            self.zoomOut()

    def zoomIn(self):
        """放大"""
        self.zoom(1 + self._delta)

    def zoomOut(self):
        """缩小"""
        self.zoom(1 - self._delta)

    def zoom(self, factor):
        """缩放
        :param factor: 缩放的比例因子
        """
        _factor = self.transform().scale(
            factor, factor).mapRect(QRectF(0, 0, 1, 1)).width()
        if _factor < 0.07 or _factor > 100:
            # 防止过大过小
            return
        self.scale(factor, factor)

class ShowImage(QDialog):
    def __init__(self,image ,background) :
        super().__init__()
        self.view = ImageView(image,background)
        self.Hlayout = QHBoxLayout()
        self.Hlayout.addWidget(self.view)
        self.setLayout(self.Hlayout)