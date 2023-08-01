from . import Setting
from PySide6.QtWidgets import QDoubleSpinBox, \
QFormLayout, QGroupBox, QLabel, QMainWindow, \
QPushButton, QSpinBox, QVBoxLayout, QWidget,QMessageBox
from PySide6.QtCore import Qt
import configparser
from PySide6.QtGui import QPalette, QColor

class SettingsWindow(QMainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.resize(240, 300)
        self.setWindowTitle('设置')
        self.setWindowModality(Qt.ApplicationModal)
        # 创建主窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 创建布局
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # 创建表单布局
        form_layout = QFormLayout()
        layout.addLayout(form_layout)


        # 添加每组人数设置项
        self.group_count_label = QLabel('Group Count:')
        self.group_count_spinbox = QSpinBox()
        self.group_count_spinbox.setMinimum(1)
        self.group_count_spinbox.setMaximum(100)
        self.group_count_spinbox.setValue(Setting.group_count)
        form_layout.addRow(self.group_count_label, self.group_count_spinbox)

        # 添加进程数设置项
        self.processes_label = QLabel('Processes:')
        self.processes_spinbox = QSpinBox()
        self.processes_spinbox.setMinimum(1)
        self.processes_spinbox.setMaximum(5)
        self.processes_spinbox.setValue(Setting.processes)
        form_layout.addRow(self.processes_label, self.processes_spinbox)
        

        # 添加是否开启多进程设置项
        self.is_multiprocessing_label = QLabel('Count Max:')
        self.is_multiprocessing_spinbox = QSpinBox()
        self.is_multiprocessing_spinbox.setMinimum(1)
        self.is_multiprocessing_spinbox.setMaximum(100)
        self.is_multiprocessing_spinbox.setValue(Setting.count_max)
        
        form_layout.addRow(self.is_multiprocessing_label, self.is_multiprocessing_spinbox)

        # 每页显示设置项
        self.page_count_label = QLabel('Page Count:')
        self.page_count_spinbox = QSpinBox()
        self.page_count_spinbox.setMinimum(1)
        self.page_count_spinbox.setMaximum(100)
        self.page_count_spinbox.setValue(Setting.page_count)
        
        form_layout.addRow(self.page_count_label, self.page_count_spinbox)
        # 创建人脸识别设置组
        face_recognition_group = QGroupBox('Face Recognition')
        layout.addWidget(face_recognition_group)

        # 创建人脸识别设置布局
        face_recognition_layout = QVBoxLayout()
        face_recognition_group.setLayout(face_recognition_layout)

        # 添加管理员人脸识别阈值设置项
        self.admin_threshold_label = QLabel('Admin Threshold:')
        self.admin_threshold_spinbox = QDoubleSpinBox()
        self.admin_threshold_spinbox.setMinimum(0.3)
        self.admin_threshold_spinbox.setMaximum(0.6)
        self.admin_threshold_spinbox.setSingleStep(0.05)
        self.admin_threshold_spinbox.setValue(Setting.admin_threshold)
        face_recognition_layout.addWidget(self.admin_threshold_label)
        face_recognition_layout.addWidget(self.admin_threshold_spinbox)

        # 添加用户人脸识别阈值设置项
        self.user_threshold_label = QLabel('User Threshold:')
        self.user_threshold_spinbox = QDoubleSpinBox()
        self.user_threshold_spinbox.setMinimum(0.3)
        self.user_threshold_spinbox.setMaximum(0.6)
        self.user_threshold_spinbox.setSingleStep(0.05)
        self.user_threshold_spinbox.setValue(Setting.user_threshold)
        face_recognition_layout.addWidget(self.user_threshold_label)
        face_recognition_layout.addWidget(self.user_threshold_spinbox)

        # 添加眼睛长宽比设置项
        self.eye_ar_thresh_label = QLabel('Eye Aspect Ratio:')
        self.eye_ar_thresh_spinbox = QDoubleSpinBox()
        self.eye_ar_thresh_spinbox.setMinimum(0.01)
        self.eye_ar_thresh_spinbox.setMaximum(0.1)
        self.eye_ar_thresh_spinbox.setSingleStep(0.01)
        self.eye_ar_thresh_spinbox.setValue(Setting.EYE_AR_THRESH)
        face_recognition_layout.addWidget(self.eye_ar_thresh_label)
        face_recognition_layout.addWidget(self.eye_ar_thresh_spinbox)

        # 添加嘴巴长宽比设置项
        self.mar_thresh_label = QLabel('Mouth Aspect Ratio:')
        self.mar_thresh_spinbox = QDoubleSpinBox()
        self.mar_thresh_spinbox.setMinimum(0.4)
        self.mar_thresh_spinbox.setMaximum(0.6)
        self.mar_thresh_spinbox.setSingleStep(0.05)
        self.mar_thresh_spinbox.setValue(Setting.MAR_THRESH)
        face_recognition_layout.addWidget(self.mar_thresh_label)
        face_recognition_layout.addWidget(self.mar_thresh_spinbox)

        
        # 添加保存按钮
        save_button = QPushButton('Save')
        save_button.clicked.connect(self.save_settings)
        layout.addWidget(save_button)

        # 设置样式
        self.setStyleSheet('''
           
            QLabel {
                color: rgb(111, 156, 207);
            }
            QLineEdit, QSpinBox, QDoubleSpinBox {
                background-color: rgb(224, 238, 255);
                color: rgb(111, 156, 207);
                border: 1px solid rgb(111, 156, 207);
                border-radius: 3px;
                padding: 3px;
            }
            
            QPushButton {
                background-color: rgb(111, 156, 207);
                color: white;
                border: none;
                border-radius: 3px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: rgb(90, 130, 175);
            }
            QPushButton:pressed {
                background-color: rgb(120, 130, 175);
            }
            QGroupBox {
                border: 1px solid rgb(111, 156, 207);
                border-radius: 3px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 5px 10px;
                background-color: rgb(232, 241, 252);
                color: rgb(111, 156, 207);
                border: none;
            }
        ''')

        # 设置背景色
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor('#222'))
        self.setPalette(palette)

    def save_settings(self):
        # 保存设置
       
        Setting.group_count = int(self.group_count_spinbox.value())
        Setting.count_max = int(self.is_multiprocessing_spinbox.value())
        Setting.admin_threshold = float(self.admin_threshold_spinbox.value())
        Setting.user_threshold = float(self.user_threshold_spinbox.value())
        Setting.EYE_AR_THRESH = float(self.eye_ar_thresh_spinbox.value())
        Setting.MAR_THRESH = float(self.mar_thresh_spinbox.value())
        Setting.processes = int(self.processes_spinbox.value())
        Setting.page_count = int(self.page_count_spinbox.value())
        # 保存设置到文件
        cfg = configparser.ConfigParser() 
        cfg.read('config.ini')
        cfg.set('setting', 'group_count', str(Setting.group_count))
        cfg.set('setting', 'count_max', str(Setting.count_max))
        cfg.set('setting', 'admin_threshold', str(Setting.admin_threshold))
        cfg.set('setting', 'user_threshold', str(Setting.user_threshold))
        cfg.set('setting', 'EYE_AR_THRESH', str(Setting.EYE_AR_THRESH))
        cfg.set('setting', 'MAR_THRESH', str(Setting.MAR_THRESH))
        cfg.set('setting', 'processes', str(Setting.processes))
        cfg.set('setting', 'page_count', str(Setting.page_count))
        with open('config.ini', 'w') as f:
            cfg.write(f)
        QMessageBox.information(self, '提示', '保存成功！')
        self.close()