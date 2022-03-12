# gitlGl-dlib_face_recognition
基于dib人脸识别应用
1.人脸识别，活体识别（张嘴，眨眼）
2.人脸识别登录，注册
3.批量用户导入数据库（将人脸向量特征转为二进制存入sqlite3，由于人脸向量特征是浮点数，转换成二进制会丢失精度），numpy==1.15.4。否则报错。
4.
dlib                    19.8.1
face-recognition        1.3.0
face-recognition-models 0.3.0
importlib-metadata      4.8.3
imutils                 0.5.4
numpy                   1.15.4
opencv-python           4.5.5.62
psutil                  5.9.0
PyQt5                   5.15.6             
scipy                   1.5.4
xlrd                    1.2.0
