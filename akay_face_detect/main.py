#! /usr/bin/env python
# -*- coding: UTF-8 -*-
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox,QLineEdit, QInputDialog
from PyQt5.QtCore import Qt, QObject, pyqtSignal,QThread
from PyQt5.QtGui import QPixmap
import sys, qdarkstyle, time, os, webbrowser,re,uuid,pymongo,requests, json
import user_interface 
from face_detect import face_recognition
from PyQt5 import QtWidgets,QtGui

####Ekranda digit olarak zamanı gösteren timer Sınıfı
###----------*************---------------- 
class Timer(QObject):
    timer_count = pyqtSignal(int)
    bool_count = pyqtSignal(bool)
    finished = pyqtSignal()


    def run(self):
        temp = 0
        while self.bool_count:
            self.timer_count.emit(temp)
            time.sleep(1)
            temp = temp + 1
        self.finished.emit()
###----------*************----------------


class MainPage (QMainWindow, user_interface.face_detection_ui):
    
    
    
    def get_mac(self):
        mac_num = uuid.getnode()
        mac  = str(":".join(re.findall('..', '%012x' % mac_num)))
        return mac

    def __init__(self, parent=None):
        self.license = False
        super(MainPage, self).__init__(parent)
        self.face_interface()
        self.setAttribute(Qt.WA_DeleteOnClose)

    ##Yüz inceleme arayüzü başlatma 
    def face_interface(self):
        self.setup_fd_ui(self)
        self.show()
        self.setMenuBar(self.ui_menubar)
        self.check_version()

            
    def check_version(self):
        mac_adress = self.get_mac()
        serial_key = ""
        with open("serial_key.json", encoding="utf-8") as f:
            json_object = json.loads(f.read())
            serial_key = str(json_object["serial_key"])
            f.close()
            
        if serial_key != "":
            url = "http://www.google.com"
            timeout = 1
            try:
                request = requests.get(url, timeout=timeout)
                myclients=pymongo.MongoClient("mongodb+srv://forencrypt:Pt-for-cry47@akay.ktm1k.mongodb.net/Akay?retryWrites=true&w=majority", tls=True,tlsAllowInvalidCertificates=True)
                mydb=myclients["license"]
                mycollection=mydb["serial-keys"]
                if mycollection.count_documents({"key":serial_key,"mac-adress":mac_adress}):
                    self.license = True
                    key_db = mycollection.find_one({"key": serial_key})
                    self.version_text.setText(key_db["user"])
                    self.ui_menubar.removeAction(self.menu_settings.menuAction())
                else:
                    self.license = False
                    self.version_text.setText("Demo Sürüm")
            except (requests.ConnectionError, requests.Timeout) as exception:
                self.critical_messagebox("Hata", "Tam sürümü kullanmak için internet bağlantınızı kontrol ediniz!", QtWidgets.QMessageBox.Critical)




   ##facedetect analiz kodları 
    def face_detect_button_clicked(self):
        print(str(self.detect_face_image_select_button.whatsThis()))
        detect_image_path = str(self.detect_face_image_select_button.whatsThis())
        if not os.path.isdir(self.output_path_label.text()) or not os.path.isdir(self.input_path_label.text()) or not os.path.isfile(detect_image_path):
            self.critical_messagebox("Klasör Hatası", "Lütfen girdi ve çıktıyı doğru seçiniz", QtWidgets.QMessageBox.Critical)
        else:
            self.progress_gif.setMovie(self.load_gif)
            self.load_gif.start()
            self.info_table_label.setRowCount(0)
                    #Her işletim sisteminde çalışması için dosya yolları os.path.join fonksiyonu ile tekrar oluşturuluyor...
            output_folder_path = self.output_path_label.text().split("/")[0] + "/"
            for dirs in self.output_path_label.text().split("/"):
                output_folder_path = os.path.join(output_folder_path , dirs)

            input_folder_path = self.input_path_label.text().split("/")[0] + "/"
            for dirs in self.input_path_label.text().split("/"):
                input_folder_path = os.path.join(input_folder_path , dirs)
            
            self.timer_thread_fd = QThread()
            self.thread_fd = QThread()

            self.worker_fd = face_recognition()

            self.timer_fd = Timer()

            self.worker_fd.moveToThread(self.thread_fd)
            self.timer_fd.moveToThread(self.timer_thread_fd)

            self.worker_fd.input_path = input_folder_path
            self.worker_fd.output_path = output_folder_path
            self.worker_fd.detect_face_image = detect_image_path
            
            self.worker_fd.license = self.license

            self.worker_fd.stop_bool = False
            self.timer_fd.bool_count = True

            self.thread_fd.started.connect(self.worker_fd.run)
            self.worker_fd.finished.connect(self.thread_fd.quit)
            self.worker_fd.finished.connect(self.worker_fd.deleteLater)
            self.thread_fd.finished.connect(self.thread_fd.deleteLater)

            self.timer_thread_fd.started.connect(self.timer_fd.run)
            self.timer_fd.finished.connect(self.timer_thread_fd.quit)
            self.timer_fd.finished.connect(self.timer_fd.deleteLater)
            self.timer_thread_fd.finished.connect(self.timer_thread_fd.deleteLater)


            self.timer_fd.timer_count.connect(self.change_digit_timer)

            self.worker_fd.info_text.connect(self.image_info_writer)

            self.worker_fd.change_image.connect(self.set_label_image_fd)

            self.worker_fd.detect_error.connect(self.error_dialog_fd)

            self.thread_fd.start()
            self.timer_thread_fd.start()

            self.stop_process_button.setEnabled(True)
            self.menu_files.setEnabled(False)
            self.menu_settings.setEnabled(False)
            self.analyze_button.setEnabled(False)
            self.input_file_tree.setEnabled(False)
            self.output_file_tree.setEnabled(False)
            self.input_path_label.setEnabled(False)
            self.output_path_label.setEnabled(False)
            self.detect_face_image_select_button.setEnabled(False)

            self.thread_fd.finished.connect(self.thread_fd_finish)
            self.worker_fd.finished.connect(self.worker_fd_finish)
 


   ## 


   ##facea detect işlemi bitişi 
    def thread_fd_finish(self):
        try:
            self.timer_fd.bool_count = False
            self.stop_process_button.setEnabled(False)
            self.menu_files.setEnabled(True)
            self.analyze_button.setEnabled(True)
            self.input_file_tree.setEnabled(True)
            self.output_file_tree.setEnabled(True)
            self.input_path_label.setEnabled(True)
            self.output_path_label.setEnabled(True)
            self.detect_face_image_select_button.setEnabled(True)
            self.menu_settings.setEnabled(True)
            self.load_gif.stop()
            self.progress_gif.clear()
            self.timer_thread_fd.quit()
        except:
            pass
   #


    def error_dialog_fd(self, err_strings):
        self.thread_fd.quit()
        self.critical_messagebox(str(err_strings[0]), str(err_strings[1]), QtWidgets.QMessageBox.Critical)

   #facedetect işlemi bitişi
    def worker_fd_finish(self):
        try:
            self.timer_thread_fd.quit()
        except:
            pass
        try:
            if self.worker_fd.stop_bool:
                self.remaining_process_label.setText("Durduruldu")
                if self.license:
                    self.question_messagebox("İşlem Durduruldu", "<b>Çıktı Klasörüne Gitmek İster Misiniz?</b>")
                else:
                    self.question_messagebox("İşlem Durduruldu", "<b>Çıktı Klasörüne Gitmek İster Misiniz?</b><br>Bu bir demo sürümdür, en fazla 10 görüntü inceleyebilirsiniz.<br><a href='https://www.forencrypt.com/iletisim/'>Tam sürüm için bize ulaşın</a>")
            else:
                if self.license:
                    self.question_messagebox("İşlem Bitti", "<b>Çıktı Klasörüne Gitmek İster Misiniz?</b>")
                else:
                    self.question_messagebox("İşlem Bitti", "<b>Çıktı Klasörüne Gitmek İster Misiniz?</b><br>Bu bir demo sürümdür, en fazla 10 görüntü inceleyebilirsiniz.<br><a href='https://www.forencrypt.com/iletisim/'>Tam sürüm için bize ulaşın</a>")

        except:
            pass
   ##

   ##facedetect stop kodları
    def face_detect_stop_button_clicked(self):
        try:
            self.worker_fd.stop_bool = True
            self.remaining_process_label.setText("Durduruluyor")
        except:
            pass
   ##

   ##Resimleri alıp labela yerleşmesi için ayarlayan fonks
    def set_label_image_fd(self, image_path):
        try:
            label = self.output_image

            self.add_image(image_path, label)
        except:
            self.output_image.setText("Resim Getirelemedi")
   ##


   #Timerı güncelleyen fonksiyon
    def change_digit_timer(self, time_count):
        try:
            time_str = time.strftime('%H:%M:%S', time.gmtime(time_count))
            self.lcd_process_timer.display(time_str)
        except:
            pass
   #





   ##İşlem devam ettikçe bilgilerin yazdırıldığı  tablonun ve progresin güncellenmesi
    def image_info_writer(self, info_array):
        try:
            self.remaining_process_label.setText(info_array[0])
            self.progress_bar.setValue(int(info_array[0].split("/")[0])/int(info_array[0].split("/")[1])*100)
            if not info_array[1] == "empty" and not info_array[2] == "empty":
                rowPosition = self.info_table_label.rowCount()
                
                self.info_table_label.insertRow(rowPosition)
                self.info_table_label.setItem(rowPosition , 0, QtWidgets.QTableWidgetItem(os.path.basename(info_array[1])))

                self.info_table_label.setItem(rowPosition , 1, QtWidgets.QTableWidgetItem(info_array[2]))
                if info_array[2] == "Var":
                    self.info_table_label.item(rowPosition, 1).setBackground(QtGui.QColor(0,255,0))
                else:
                    self.info_table_label.item(rowPosition, 1).setBackground(QtGui.QColor(255,0,0))
                    
                item = self.info_table_label.item(rowPosition, 0)
                item.setWhatsThis(info_array[1])
                #self.process_text.append(info_array[1])
                self.info_table_label.scrollToBottom()
        except:
            pass
   #         

   ###Parametre olarak alınan resmi , parametre olarak alınan label'a uygun boyutlarda yerleştiren fonksiyon
    def add_image(self, image_path, image_label):
        try:
            pixmap = QPixmap(image_path)
            
           
            image_label_height = int(self.screen_height * 0.34)

            pixmap = pixmap.scaled(image_label_height ,image_label_height)
            image_label.setAlignment(Qt.AlignCenter)
            image_label.setPixmap(QPixmap(pixmap))
        except ZeroDivisionError:
            image_label.setText("Resim getirilirken bir hata oluştu")
   ###-------------


############# messagebox methodları ######################

    def critical_messagebox(self, title, msg, type):
        msgbox = QMessageBox()
        msgbox.setIcon(type)
        msgbox.setWindowIcon(QtGui.QIcon("icons/icon.png"))
        msgbox.setWindowTitle(title)
        msgbox.setText(msg)
        ok_button = msgbox.addButton('Tamam', QMessageBox.AcceptRole)

        msgbox.exec_()

        if msgbox.clickedButton() == ok_button:
            msgbox.close()

    def question_messagebox(self, title, msg):
        msgbox = QMessageBox()
        msgbox.setIcon(QtWidgets.QMessageBox.Question)
        msgbox.setWindowIcon(QtGui.QIcon("icons/icon.png"))
        msgbox.setWindowTitle(title)
        msgbox.setText(msg)
        yes_button = msgbox.addButton('Evet', QMessageBox.YesRole)
        no_button = msgbox.addButton('Hayır', QMessageBox.NoRole)

        msgbox.exec_()

        if msgbox.clickedButton() == yes_button:
            webbrowser.open('file:///' + self.worker_fd.output_path)
        elif msgbox.clickedButton() == no_button:
            msgbox.close()
            
            
            
            
        
    def serial_key_bar_click(self):
        dialog = QInputDialog(self)
        dialog.setWindowTitle("Seri Numarası")
        dialog.setLabelText("Seri Numarasını Giriniz")    
        with open("serial_key.json", encoding="utf-8") as f:
            json_object = json.loads(f.read())
            dialog.setTextValue(str(json_object["serial_key"]))
            f.close()
        dialog.setOkButtonText("Tamam")
        dialog.setCancelButtonText("Vazgeç")
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            text = dialog.textValue()
            url = "http://www.google.com"
            timeout = 1
            try:
                request = requests.get(url, timeout=timeout)
                myclients=pymongo.MongoClient("mongodb+srv://forencrypt:Pt-for-cry47@akay.ktm1k.mongodb.net/Akay?retryWrites=true&w=majority", tls=True,tlsAllowInvalidCertificates=True)
                mydb=myclients["license"]
                mycollection=mydb["serial-keys"]
                key_db = mycollection.find_one({"key": text})
                if key_db != None:
                    if key_db["mac-adress"] == "":
                        self.license = True
                        mycollection.update_one(
                            {"key":text},
                            {"$set":{
                                "key":text,
                                "mac-adress":self.get_mac()
                            }}
                        )
                        json_file = open("serial_key.json", "w+")
                        json.dump({ "serial_key": text }, json_file) 
                        json_file.close()
                        self.critical_messagebox("Harika!", "Uygulamanız tam sürüm olmuştur", QtWidgets.QMessageBox.Information)
                        self.version_text.setText(key_db["user"])
                        self.license = True
                        self.ui_menubar.removeAction(self.menu_settings.menuAction())
                    else: 
                        if key_db["mac-adress"] != self.get_mac(): 
                            self.critical_messagebox("Hata", "Girdiğiniz anahtar başkası tarafından kullanılıyor!", QtWidgets.QMessageBox.Critical)
                        else: 
                            self.critical_messagebox("Bilgi", "Uygulamanız tam sürüm olmuştur!", QtWidgets.QMessageBox.Information)
                            self.version_text.setText(key_db["user"])    
                            json_file = open("serial_key.json", "w+")
                            json.dump({ "serial_key": text }, json_file) 
                            json_file.close()
                            self.license = True
                            self.ui_menubar.removeAction(self.menu_settings.menuAction())
                else:
                    self.critical_messagebox("Hata", "Girdiğiniz anahtar doğru değil!", QtWidgets.QMessageBox.Critical)
            except (requests.ConnectionError, requests.Timeout) as exception:
                self.critical_messagebox("Hata", "Tam sürümü kullanmak için internet bağlantınızı kontrol ediniz!", QtWidgets.QMessageBox.Critical)
        else:
            print("canceled")

##########################################################

    def dark_theme_select(self):
        app.setStyleSheet(qdarkstyle.load_stylesheet())

    
    def light_theme_select(self):

        app.setStyleSheet("")
        
        



app = QApplication(sys.argv)
pencere = MainPage()
sys.exit(app.exec_())