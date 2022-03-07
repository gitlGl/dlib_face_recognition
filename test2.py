import xlrd
from PyQt5.QtWidgets import QFileDialog
from src import CreatUser
from PyQt5.QtWidgets import QApplication
import sys


class ReadStudentInformation():
    def __init__(self) -> None:

        pass
    def read_path(self):
        path ,_= QFileDialog.getOpenFileName(
                None, "选择文件", "c:\\", "files(*.xlsx )")
           
        book = xlrd.open_workbook(path)
        sheets = book.sheets()
        for sheet in sheets:
            rows = sheet.nrows
            for i in range(1,rows):
                list1 =  sheet.row_values(rowx=i)
                list1[0] = int(list1[0])#转为正确格式
                list1[1] = str(list1[1])
                list1[2] = str(list1[2])
                list1[3] = str(list1[3])
       
                list2 = ["id_number","user_name","password","img_path" ]
                dic = dict(zip(list2,list1))
                CreatUser(dic)
                print(dic)
         
if __name__ == '__main__':

    app = QApplication(sys.argv)
    test = ReadStudentInformation()
    test.read_path()   
    app.exec_()


                 
