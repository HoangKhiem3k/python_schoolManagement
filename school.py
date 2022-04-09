from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from PyQt5.uic import loadUiType
import mysql.connector as con

ui, _ = loadUiType('school.ui')

class MainApp(QMainWindow, ui): 
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)  
 
        self.tabWidget.setCurrentIndex(0) #Open o page Login
        self.tabWidget.tabBar().setVisible(False) # An tabbar truoc khi login
        self.menubar.setVisible(False) # An menubar khi login
        self.b01.clicked.connect(self.login)

        self.menu11.triggered.connect(self.show_add_new_student_tab) # Phat signal
        self.menu12.triggered.connect(self.show_edit_or_delete_student_tab)
        self.b12.clicked.connect(self.save_student_details)
        self.cb21.currentIndexChanged.connect(self.fill_details_when_combobox_selected)
        self.b21.clicked.connect(self.edit_student)
        self.b22.clicked.connect(self.delete_student)
        
        self.menu21.triggered.connect(self.show_mark_tab)
        self.b31.clicked.connect(self.save_mark_details)
        self.cb32.currentIndexChanged.connect(self.fill_exam_name_in_combobox_for_registration_number_selected)
        self.b32.clicked.connect(self.fill_exam_details_in_textbox_for_examname_selected)
        self.b33.clicked.connect(self.update_mark_details)
        self.b34.clicked.connect(self.delete_mark_details)


        self.menu31_2.triggered.connect(self.show_report) # Phat signal
        self.menu32.triggered.connect(self.show_report)
        self.menu41_2.triggered.connect(self.logout)

    ##### LOGIN #####
    def login(self):
        un = self.tb01.text()
        pw = self.tb02.text()
        if(un == "admin" and pw == "123"):
            self.menubar.setVisible(True)
            self.tabWidget.setCurrentIndex(1) # dang nhap thanh cong vo page Home
        else:
            QMessageBox.information(self,"Đăng nhập","Nhập sai, Nhập lại!")
            self.l01.setText("Thử lại!")

    ##### Add New Student ######
    def show_add_new_student_tab(self):
        self.tabWidget.setCurrentIndex(2)
        self.fill_next_registration_number()

    def fill_next_registration_number(self):
        try:
            rn = 0 
            mydb = con.connect(host="localhost", user="root", password="",db="school")
            cursor = mydb.cursor()
            cursor.execute("select * from student") #con tro
            result = cursor.fetchall()  # truy vấn và trả về một danh sách các  giá trị
            if result:
                for stud in result:
                    rn += 1
            self.tb11.setText(str(rn+1))
        except con.Error as e:
            print("Lỗi "+ e)

    def save_student_details(self):
        try:
            mydb = con.connect(host="localhost", user="root", password="",db="school")
            cursor = mydb.cursor()
            registration_number = self.tb11.text()
            full_name = self.tb12.text()
            gender = self.cb11.currentText()
            date_of_birth = self.tb13.text()
            class_ = self.tb14.text()
            address = self.mtb11.toPlainText()
            phone = self.tb15.text()
            email = self.tb16.text()
            school_year = self.cb12.currentText()

            qry = "insert into student (registration_number,full_name,gender,date_of_birth,class_,address,phone,email,school_year) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)" 
            value = (registration_number,full_name,gender,date_of_birth,class_,address,phone,email,school_year)
            cursor.execute(qry,value)   
            mydb.commit()

            self.l11.setText("Lưu thành công")
            QMessageBox.information(self,"School Management System","Thêm thành công!")
            self.tb11.setText("")

            self.tb12.setText("")

            self.tb13.setText("")

            self.tb14.setText("")

            self.tb15.setText("")

            self.tb16.setText("")

            self.mtb11.setText("")

            self.tabWidget.setCurrentIndex(1)
        except con.Error as e:
            self.l11.setText("Lỗi: "+e)

    #########  Edit/ Delete Student ########
    def show_edit_or_delete_student_tab(self):
        self.tabWidget.setCurrentIndex(3)
        self.fill_registration_number_in_combobox()

    def fill_registration_number_in_combobox(self):
        try:
            self.cb21.clear()
            mydb = con.connect(host="localhost", user="root", password="",db="school")
            cursor = mydb.cursor()
            cursor.execute("select * from student")
            result = cursor.fetchall()
            if result:
                for stud in result:
                    self.cb21.addItem(str(stud[1]))
            
        except con.Error as e:
            print("Lỗi "+ e)

    def fill_details_when_combobox_selected(self):
        try:
            
            mydb = con.connect(host="localhost", user="root", password="",db="school")
            cursor = mydb.cursor()
            cursor.execute("select * from student where registration_number = '"+ self.cb21.currentText() +"' ")
            result = cursor.fetchall()
            if result:
                for stud in result:
                    self.tb21.setText(str(stud[2]))
                    self.tb22.setText(str(stud[3]))
                    self.tb23.setText(str(stud[4]))
                    self.tb24.setText(str(stud[5]))
                    self.mtb21.setText(str(stud[6]))
                    self.tb25.setText(str(stud[7]))
                    self.tb26.setText(str(stud[8]))
                    self.tb27.setText(str(stud[9]))
        except con.Error as e:
            print("Lỗi "+ e)

    def edit_student(self):
        try:
            mydb = con.connect(host="localhost", user="root", password="",db="school")
            cursor = mydb.cursor()
            registration_number = self.cb21.currentText()
            full_name = self.tb21.text()
            gender = self.tb22.text()
            date_of_birth = self.tb23.text()
            class_ = self.tb24.text()
            address = self.mtb21.toPlainText()
            phone = self.tb25.text()
            email = self.tb26.text()
            school_year = self.tb27.text()

            qry = "update student set full_name = '"+ full_name +"',gender = '"+ gender +"',date_of_birth = '"+ date_of_birth +"',class_ = '"+ class_ +"',address = '"+ address +"',phone = '"+ phone +"',email = '"+ email +"',school_year = '"+ school_year +"' where registration_number = '"+ registration_number +"'" 
            
            cursor.execute(qry)
            mydb.commit()

            self.l21.setText("Thành công")
            QMessageBox.information(self,"School Management System","Cập nhật thành công!")
            self.tb21.setText("")

            self.tb22.setText("")

            self.tb23.setText("")

            self.tb24.setText("")

            self.tb25.setText("")

            self.tb26.setText("")

            self.tb27.setText("")

            self.mtb21.setText("")

            self.tabWidget.setCurrentIndex(1)
        except con.Error as e:
            self.l21.setText("Lỗi "+e)

    def delete_student(self):
        m = QMessageBox.question(self,"Xóa","Xóa học sinh này? ?",QMessageBox.Yes|QMessageBox.No)
        if m == QMessageBox.Yes:
            try:
                mydb = con.connect(host="localhost", user="root", password="",db="school")
                cursor = mydb.cursor()
                registration_number = self.cb21.currentText()
                

                qry = "delete from student where registration_number = '"+ registration_number +"' " 
            
                cursor.execute(qry)
                mydb.commit()

                self.l21.setText("Thành công")
                QMessageBox.information(self,"School Management System","Xóa thành công!")
                self.tabWidget.setCurrentIndex(1)
            except con.Error as e:
                self.l21.setText("Lỗi "+e)

    ######### MARK #########
    def show_mark_tab(self):
        self.tabWidget.setCurrentIndex(4)
        self.fill_registration_number_in_combobox_for_mark_tab()

    def fill_registration_number_in_combobox_for_mark_tab(self):
        try:
            self.cb31.clear()
            self.cb32.clear()
            mydb = con.connect(host="localhost", user="root", password="",db="school")
            cursor = mydb.cursor()
            cursor.execute("select * from student")
            result = cursor.fetchall()
            if result:
                for stud in result:
                    self.cb31.addItem(str(stud[1]))
                    self.cb32.addItem(str(stud[1]))
        except con.Error as e:
            print("Lỗi "+ e)

    def save_mark_details(self):
        try:
            mydb = con.connect(host="localhost", user="root", password="",db="school")
            cursor = mydb.cursor()
            registration_number = self.cb31.currentText()
            exam_name = self.tb31.text()
            literature = self.tb32.text()
            english = self.tb33.text()
            math = self.tb34.text()
            physics = self.tb35.text()
            chemistry = self.tb36.text()
        
            qry = "insert into mark (registration_number,exam_name, literature,english,math,physics,chemistry) values(%s,%s,%s,%s,%s,%s,%s)" 
            value = (registration_number,exam_name, literature,english,math,physics,chemistry)
            cursor.execute(qry,value)
            mydb.commit()

            self.l31.setText("Lưu thành công")
            QMessageBox.information(self,"School Management System","Thêm thành công!")
            self.tb31.setText("")

            self.tb32.setText("")

            self.tb33.setText("")

            self.tb34.setText("")

            self.tb35.setText("")

            self.tb36.setText("")

            self.tabWidget.setCurrentIndex(1)
        except con.Error as e:
            self.l11.setText("Lỗi "+e)

    def fill_exam_name_in_combobox_for_registration_number_selected(self):
        try:
            self.cb33.clear()
            registration_number = self.cb32.currentText()
            mydb = con.connect(host="localhost", user="root", password="",db="school")
            cursor = mydb.cursor()
            cursor.execute("select * from mark where registration_number = '"+ registration_number +"'  ")
            result = cursor.fetchall()
            if result:
                for stud in result: 
                    self.cb33.addItem(str(stud[2]))
        except con.Error as e:
            print("Lỗi "+ e)

    def fill_exam_details_in_textbox_for_examname_selected(self):
        try:
            registration_number = self.cb32.currentText()
            exam_name = self.cb33.currentText()
            mydb = con.connect(host="localhost", user="root", password="",db="school")
            cursor = mydb.cursor()
            cursor.execute("select * from mark where registration_number ='"+registration_number+"'and exam_name ='"+exam_name+"'")
            result = cursor.fetchall()
            if result:
                for stud in result: 
                    self.tb37.setText(str(stud[3]))
                    self.tb38.setText(str(stud[4]))
                    self.tb39.setText(str(stud[5]))
                    self.tb310.setText(str(stud[6]))
                    self.tb311.setText(str(stud[7]))
        except con.Error as e:
            print("Lỗi "+ e)

    def update_mark_details(self):
        try:
            mydb = con.connect(host="localhost",user="root",password="",db="school")
            cursor = mydb.cursor()
            registration_number = self.cb32.currentText()
            exam_name = self.cb33.currentText()
            literature = self.tb37.text()
            english = self.tb38.text()
            math = self.tb39.text()
            physics = self.tb310.text()
            chemistry = self.tb311.text()
            qry = "update mark set  literature = '"+   literature +"',english = '"+ english +"',math = '"+ math +"',physics = '"+ physics +"', chemistry = '"+ chemistry +"'  where registration_number = '"+ registration_number +"' and exam_name = '"+ exam_name +"'"
            
            cursor.execute(qry)
            mydb.commit()

            self.l32.setText("Thành công")
            QMessageBox.information(self, "School management system","Sửa thành công!")
            self.tb37.setText("")
            self.tb38.setText("")

            self.tb39.setText("")

            self.tb310.setText("")

            self.tb311.setText("")

            self.tabWidget.setCurrentIndex(1)
        except con.Error as e:
            self.l32.setText("Lỗi " + e)


    def delete_mark_details(self):

        m = QMessageBox.question(self,"Xóa","Bạn muốn xóa ?", QMessageBox.Yes|QMessageBox.No)

        if m == QMessageBox.Yes:

            try:

                mydb = con.connect(host="localhost",user="root",password="",db="school")

                cursor = mydb.cursor()

                registration_number = self.cb32.currentText()

                exam_name = self.cb33.currentText()

                qry = "delete from mark where registration_number = '"+ registration_number +"' and exam_name = '"+ exam_name +"'"

                cursor.execute(qry)

                mydb.commit()

                self.l32.setText("Thành công")

                QMessageBox.information(self, "School management system","Đã xóa thành công!")

                self.tb37.setText("")

                self.tb38.setText("")

                self.tb39.setText("")

                self.tb310.setText("")

                self.tb311.setText("")

                self.tabWidget.setCurrentIndex(1)

            except con.Error as e:

                self.l32.setText("Lỗi " + e)

    ########### report ###########

    def show_report(self):

        table_name = self.sender()

        self.l61.setText(table_name.text())

        self.tabWidget.setCurrentIndex(5)

        try:

            self.tableReport.setRowCount(0)

            print(table_name.text())

            if(table_name.text()=="Học sinh"):

                mydb = con.connect(host="localhost",user="root",password="",db="school")

                cursor = mydb.cursor()

                qry = "select registration_number,full_name,gender,date_of_birth,class_,address,phone,email,school_year from student"

                cursor.execute(qry)

                result = cursor.fetchall() # tra ve danh sach

                r = 0

                c = 0

                for row_number, row_data in enumerate(result): #them bo dem vao doi tuong

                    r += 1

                    c = 0

                    for row_number, data in enumerate(row_data):

                        c += 1

                self.tableReport.clear()

                self.tableReport.setColumnCount(c)

                for row_number, row_data in enumerate(result):

                    self.tableReport.insertRow(row_number)

                    for column_number, data in enumerate(row_data):

                        self.tableReport.setItem(row_number, column_number,QTableWidgetItem(str(data)))

                        self.tableReport.setHorizontalHeaderLabels(['No.','Họ và tên','Giới tính','Ngày sinh','Lớp','Địa chỉ','Điện thoại','Email','Niên khóa'])
            

            if(table_name.text()=="Điểm"):

                mydb = con.connect(host="localhost",user="root",password="",db="school")

                cursor = mydb.cursor()

                qry = "select registration_number,exam_name,literature,english,math,physics,chemistry from mark"

                cursor.execute(qry)

                result = cursor.fetchall()

                r = 0
                c = 0

                for row_number, row_data in enumerate(result):

                    r += 1
                    c = 0

                    for row_number, data in enumerate(row_data):
                        c += 1

                self.tableReport.clear()

                self.tableReport.setColumnCount(c)

                for row_number, row_data in enumerate(result):
                    self.tableReport.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.tableReport.setItem(row_number, column_number,QTableWidgetItem(str(data)))
                        self.tableReport.setHorizontalHeaderLabels(['Học sinh','Tên kỳ thi','Ngữ Văn','Tiếng Anh','Toán','Vật lý','Hóa học'])
        except con.Error as e:
            print(e)



   
    ########## log out ###########
    def logout(self):
        self.menubar.setVisible(False)
        self.tb01.setText("")
        self.tb02.setText("")
        self.tabWidget.setCurrentIndex(0)
        QMessageBox.information(self, "Đăng xuất!","Bạn muốn đăng xuất ?")

def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
