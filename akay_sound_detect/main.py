import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import Qt, QObject, pyqtSignal,QThread
import time, os 
import user_interface
import qdarkstyle
from sound_recognize import sound_recognition
import webbrowser


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


class MainPage (QMainWindow, user_interface.sound_detection_ui):

    def __init__(self, parent=None):
        super(MainPage, self).__init__(parent)
        self.sound_interface()
        self.setAttribute(Qt.WA_DeleteOnClose)


    ##Ses inceleme arayüzü başlatma 
    def sound_interface(self):
        self.setup_sd_ui(self)
        self.show()
        self.setMenuBar(self.ui_menubar)


   #Ses analizi yapan kodlar iişte 
    def sound_recognition_analyze_button(self):        
        if not os.path.isdir(self.output_path_label.text()) or not os.path.isdir(self.input_path_label.text()):
            self.critical_messagebox("Klasör Hatası", "Lütfen girdi ve çıktı klasörlerini seçiniz")
        else:
            try:
                self.info_table_label.setRowCount(0)
                

                #Her işletim sisteminde çalışması için dosya yolları os.path.join fonksiyonu ile tekrar oluşturuluyor...
                output_folder_path = self.output_path_label.text().split("/")[0] + "/"
                for dirs in self.output_path_label.text().split("/"):
                    output_folder_path = os.path.join(output_folder_path , dirs)

                input_folder_path = self.input_path_label.text().split("/")[0] + "/"
                for dirs in self.input_path_label.text().split("/"):
                    input_folder_path = os.path.join(input_folder_path , dirs)
                self.movie_analyze_gif.start() 
                self.movie_process_gif.start() 


                self.timer_thread1 = QThread()
                self.timer1 = Timer()


                self.thread1 = QThread()
                self.timer1.bool_count = True


                # Step 3: Create a worker object
                self.worker1 = sound_recognition()
                # Step 4: Move worker to the thread
                self.worker1.moveToThread(self.thread1)

                self.worker1.sounds_path = input_folder_path
                self.worker1.csv_path = output_folder_path
                self.worker1.lang = self.lang_combobox.currentData()
                self.worker1.stop_bool = False
                self.worker1.search_text = self.search_word_text.text()

                self.timer1.moveToThread(self.timer_thread1)

                self.timer_thread1.started.connect(self.timer1.run)
                self.timer1.finished.connect(self.timer_thread1.quit)
                self.timer1.finished.connect(self.timer1.deleteLater)
                self.timer_thread1.finished.connect(self.timer_thread1.deleteLater)


                self.timer1.timer_count.connect(self.change_digit_timer)
            
                self.thread1.started.connect(self.worker1.run)

                self.worker1.finished.connect(self.thread1.quit)
                self.worker1.finished.connect(self.worker1.deleteLater)
                self.thread1.finished.connect(self.thread1.deleteLater)

                self.worker1.info_text.connect(self.sound_info_writer)

                self.worker1.sound_error.connect(self.error_dialog_sound)

                self.thread1.start()
                self.timer_thread1.start()

                self.stop_process_button.setEnabled(True)
                self.analyze_button.setEnabled(False)
                self.search_word_text.setEnabled(False)
                self.lang_combobox.setEnabled(False)
                self.input_file_tree.setEnabled(False)
                self.output_file_tree.setEnabled(False)
                self.input_path_label.setEnabled(False)
                self.output_path_label.setEnabled(False)
                self.input_folder_bar.setEnabled(False)
                self.output_folder_bar.setEnabled(False) 

                self.thread1.finished.connect(self.thread_finish1)
                self.worker1.finished.connect(self.worker_finish1)
            except:
                pass
        
   #


   #Timerı güncelleyen fonksiyon
    def change_digit_timer(self, time_count):
        try:
            time_str = time.strftime('%H:%M:%S', time.gmtime(time_count))
            self.lcd_process_timer.display(time_str)
        except:
            pass
   #

   #İşlem bittiğinde ya da durdurulduğunda yapılacakları gerçekleyen fonksiyon
    def worker_finish1(self):
        try:
            self.thread1.quit()
        except:
            pass
        try:
            if self.worker1.stop_bool:
                self.sound_waiting_messagebox.done(1)
                self.question_messagebox("İşlem Durduruldu", "Çıktı Klasörünü Görmek İster misiniz?")
            else:
                self.question_messagebox("İşlem Bitti", "Çıktı Klasörünü Görmek İster misiniz?")
        except:
            pass
   #

   
   ##Ses bilgielerini ekrana yazdıran fonksyion 
    def sound_info_writer(self, info_array):
        try:
            self.remaining_process_label.setText(info_array[0])
            self.progress_bar.setValue(int(info_array[0].split("/")[0])/int(info_array[0].split("/")[1])*100)
            if not info_array[1] == "empty" and not info_array[2] == "empty" and not info_array[3] == "empty" and not info_array[4] == "empty":
                rowPosition = self.info_table_label.rowCount()
                
                self.info_table_label.insertRow(rowPosition)
                self.info_table_label.setItem(rowPosition , 0, QtWidgets.QTableWidgetItem(os.path.basename(info_array[2])))
                self.info_table_label.setItem(rowPosition , 1, QtWidgets.QTableWidgetItem(info_array[3]))
                if info_array[4]:
                    self.info_table_label.setItem(rowPosition , 2, QtWidgets.QTableWidgetItem("Bulundu"))
                else:
                    self.info_table_label.setItem(rowPosition , 2, QtWidgets.QTableWidgetItem("Bulunamadı"))


                item = self.info_table_label.item(rowPosition, 0)
                item.setWhatsThis(info_array[1])
                self.info_table_label.scrollToBottom()
        except:
            pass
   # 


   #Ses işi bittiğinde yapılacaklar
    def thread_finish1(self):
        try:
            self.timer1.bool_count = False
            self.analyze_button.setEnabled(True)
            self.search_word_text.setEnabled(True)
            self.lang_combobox.setEnabled(True)
            self.movie_analyze_gif.stop() 
            self.movie_process_gif.stop()
            self.stop_process_button.setEnabled(False)
            self.input_file_tree.setEnabled(True)
            self.output_file_tree.setEnabled(True)
            self.input_path_label.setEnabled(True)
            self.output_path_label.setEnabled(True)
            self.input_folder_bar.setEnabled(True)
            self.output_folder_bar.setEnabled(True) 
            self.timer_thread1.quit()
        except:
            pass
   #

   #Seste hata Kontrolü
    def error_dialog_sound(self, err_strings):
        self.thread1.quit()
        QMessageBox.critical(self, str(err_strings[0]), str(err_strings[1]))
   #


    #Ses durdur butonuna baasılması
    def sound_stop_button_clicked(self):
        
        self.worker1.stop_bool = True
        self.sound_waiting_messagebox = QMessageBox()
        self.sound_waiting_messagebox.setWindowIcon(QtGui.QIcon("icons/icon.png"))
        self.sound_waiting_messagebox.setIcon(QtWidgets.QMessageBox.Information)
        self.sound_waiting_messagebox.setWindowTitle("Durduruluyor")
        self.sound_waiting_messagebox.setText("Geçerli Dosya İşlendiğinde Durdurulacaktır.Lütfen Bekleyin")
        self.sound_waiting_messagebox.setStandardButtons(QMessageBox.NoButton)
        self.sound_waiting_messagebox.exec()
   # 



############# messagebox methodları ######################






    def critical_messagebox(self, title, msg):
        msgbox = QMessageBox()
        msgbox.setIcon(QtWidgets.QMessageBox.Critical)
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
            webbrowser.open('file:///' + self.worker.output_path)
        elif msgbox.clickedButton() == no_button:
            msgbox.close()


##########################################################


    def dark_theme_select(self):
        app.setStyleSheet(qdarkstyle.load_stylesheet())

    
    def light_theme_select(self):

        app.setStyleSheet("")


app = QApplication(sys.argv)
pencere = MainPage()
sys.exit(app.exec_())
