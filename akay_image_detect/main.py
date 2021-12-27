import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import Qt, QObject, pyqtSignal,QThread
from PyQt5.QtGui import QImage, QPixmap
import time, os , json
import user_interface
import qdarkstyle
import webbrowser
from coco_dataset_dialog import ChecklistDialog
from coco_model import CocoModel
from PIL.ImageQt import ImageQt



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


class MainPage (QMainWindow, user_interface.image_detection_ui):

    def __init__(self, parent=None):
        super(MainPage, self).__init__(parent)
        self.image_interface()
        self.setAttribute(Qt.WA_DeleteOnClose)


    ##Ses inceleme arayüzü başlatma 
    def image_interface(self):
        self.setup_id_ui(self)
        self.goruntu_inceleme_bar.setEnabled(False)
        self.show()
        self.setMenuBar(self.ui_menubar)
        ChecklistDialog.clean_checked(self)


    def video_interface(self):
        self.setup_vfd_ui(self)
        self.video_inceleme_bar.setEnabled(False)
        self.show()
        self.setMenuBar(self.ui_menubar)
        ChecklistDialog.clean_checked(self)


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

   #Sınıf seçme butonlar
    def coco_button_clicked(self):

        temp_bool = True
        with open("json_files/custom_classes.json", encoding="utf-8") as f:
            json_content = json.loads(f.read())
            for json_object in json_content["classes"]:
                if json_object["check"] == "True":
                    temp_bool = False  
        if temp_bool:

            self.form = ChecklistDialog(class_json_file="json_files/coco_classes.json", name="Coco Dataset Sınıfları")
            if self.form.exec_():

                self.change_choose_label()
        else:            
            self.critical_messagebox("Hata", "Forencrypt modelleri seçiliyken bu nesneleri seçemezsiniz")
            

    def forencrypt_button_clicked(self):
        temp_bool = True
        with open("json_files/coco_classes.json", encoding="utf-8") as f:
            json_content = json.loads(f.read())
            for json_object in json_content["classes"]:
                if json_object["check"] == "True":
                    temp_bool = False  
        if temp_bool:
            self.form = ChecklistDialog(class_json_file="json_files/custom_classes.json", name="Forencrypt Sınıfları")
            if self.form.exec_():
                self.change_choose_label()
        else:
            self.critical_messagebox("Hata", "Coco modelleri seçiliyken bu nesneleri seçemezsiniz")
  #
 

 
   ##Seçim comboboxu değiştiğinde seçilenlerin gösterildiği text labelın ayarlanması 
    def change_choose_label(self):

            #Seçilen nesneleri getirme
        try:
            nesneler = ""
            with open("json_files/custom_classes.json", encoding="utf-8") as f:
                json_content = json.loads(f.read())
                for json_object in json_content["classes"]:
                    if json_object["check"] == "True":
                        nesneler += json_object["turkish"] + ", "
            with open("json_files/coco_classes.json", encoding="utf-8") as f:
                json_content = json.loads(f.read())
                for json_object in json_content["classes"]:
                    if json_object["check"] == "True":
                        nesneler += json_object["turkish"] + ", "

            #En sondaki virgülü kaldırmak için
            nesneler = nesneler[:-2]
            self.choose_class_label.setText("Aranacak nesneler : " + nesneler)

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








#########################################################################################################################################################################################################################










   ##Video aracından inceleme butonuna basıldığında  
    def video_frame_analyze_button_clicked(self):
        try:
            if not os.path.isdir(self.output_path_label.text()) or not os.path.isfile(self.input_path_label.text()) or not "mp4" in self.input_path_label.text():
                self.critical_messagebox("Klasör Hatası", "Lütfen girdi ve çıktıyı doğru seçiniz")
            elif self.choose_class_label.text() == "Aranacak nesneler : ":
               self.critical_messagebox("Hata", "Lütfen Aranacak Nesneleri Seçiniz")
            else:
                fps = 1.0 / float(self.frame_combobox.currentText())
                
                self.start_image_analyze(fps=fps)
        except:
            pass
   #

   ##resim aracında inceleme butonunun kodları
    def image_detection_analyze_button_clicked(self):
        try:
            if not os.path.isdir(self.output_path_label.text()) or not os.path.isdir(self.input_path_label.text()):
                self.critical_messagebox("Klasör Hatası", "Lütfen girdi ve çıktıyı doğru seçiniz")
            elif self.choose_class_label.text() == "Aranacak nesneler : ":
                self.critical_messagebox("Hata", "Lütfen Aranacak Nesneleri Seçiniz")
            else:
                self.start_image_analyze()
        except:
            pass
   #



   #resim ve ya video inceleme işlemini başlatan kodlar
    def start_image_analyze(self, fps = 1):
        self.info_table_label.setRowCount(0)
                #Her işletim sisteminde çalışması için dosya yolları os.path.join fonksiyonu ile tekrar oluşturuluyor...
        output_folder_path = self.output_path_label.text().split("/")[0] + "/"
        for dirs in self.output_path_label.text().split("/"):
            output_folder_path = os.path.join(output_folder_path , dirs)

        input_folder_path = self.input_path_label.text().split("/")[0] + "/"
        for dirs in self.input_path_label.text().split("/"):
            input_folder_path = os.path.join(input_folder_path , dirs)
                


        self.timer_thread = QThread()
        self.thread = QThread()
        # Step 3: Create a worker object

        self.worker = CocoModel()



        self.timer = Timer()
        # Step 4: Move worker to the thread
        self.worker.moveToThread(self.thread)
        self.timer.moveToThread(self.timer_thread)

        self.worker.input_path = input_folder_path
        self.worker.output_path = output_folder_path
        self.worker.stop_bool = False
        self.timer.bool_count = True
        if "CDS" in self.choose_class_label.text():
            self.worker.model_file = True
        else:
            self.worker.model_file = False
        self.worker.fps = fps
                

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.timer_thread.started.connect(self.timer.run)
        self.timer.finished.connect(self.timer_thread.quit)
        self.timer.finished.connect(self.timer.deleteLater)
        self.timer_thread.finished.connect(self.timer_thread.deleteLater)


        self.timer.timer_count.connect(self.change_digit_timer)

        self.worker.info_text.connect(self.image_info_writer)

        self.worker.change_image.connect(self.set_label_image)

        self.thread.start()
        self.timer_thread.start()

        self.stop_process_button.setEnabled(True)
        self.menu_tools.setEnabled(False)
        self.menu_files.setEnabled(False)
        self.analyze_button.setEnabled(False)
        self.input_file_tree.setEnabled(False)
        self.output_file_tree.setEnabled(False)
        self.input_path_label.setEnabled(False)
        self.output_path_label.setEnabled(False)
        self.cocodataset_button.setEnabled(False)
        self.forencrypt_model_button.setEnabled(False)
        try:
            self.frame_combobox.setEnabled(False)
        except:
            pass
        try:
            self.image_file_select.setEnabled(False)
            self.extract_folder_select.setEnabled(False)
            self.mount_button.setEnabled(False) 

        except:
            pass

        self.thread.finished.connect(self.thread_finish)
        self.worker.finished.connect(self.worker_finish)
   #----------------








   #İşlem bittiğinde timerı durduran fonksyion 
    def thread_finish(self):
        try:
            self.timer.bool_count = False
            self.analyze_button.setEnabled(True)
            self.stop_process_button.setEnabled(False)
            self.input_file_tree.setEnabled(True)
            self.output_file_tree.setEnabled(True)
            self.input_path_label.setEnabled(True)
            self.output_path_label.setEnabled(True)
            self.cocodataset_button.setEnabled(True)
            self.forencrypt_model_button.setEnabled(True)
            self.menu_files.setEnabled(True)
            self.menu_tools.setEnabled(True)
            self.timer_thread.quit()
            try:
                self.frame_combobox.setEnabled(True)
            except:
                pass
        except:
            pass
   # 

   
   #İşlem bittiğinde ya da durdurulduğunda yapılacakları gerçekleyen fonksiyon
    def worker_finish(self):
        try:
            self.timer_thread.quit()
        except:
            pass
        try:
            if self.worker.stop_bool:
                self.question_messagebox("İşlem durduruldu", "Çıktı Klasörüne Gitmek İster Misiniz?")
            else:
                self.question_messagebox("İşlem bitti", "Çıktı Klasörüne Gitmek İster Misiniz?")
        except:
            pass
   #



   #Durdur butonuna basıldığı zaman işlemi sonlandıran fonksiyon
    def stop_button_clicked(self):
        try:
            self.worker.stop_bool = True
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
                if info_array[2] == "":
                    self.info_table_label.setItem(rowPosition , 1, QtWidgets.QTableWidgetItem("Bulunamadı"))
                else:
                    self.info_table_label.setItem(rowPosition , 1, QtWidgets.QTableWidgetItem(info_array[2]))
                self.info_table_label.setItem(rowPosition , 2, QtWidgets.QTableWidgetItem(info_array[3]))
                item = self.info_table_label.item(rowPosition, 0)
                item.setWhatsThis(info_array[1])
                #self.process_text.append(info_array[1])
                self.info_table_label.scrollToBottom()
        except:
            pass
   #         


   ##Resimleri alıp labela yerleşmesi için ayarlayan fonks
    def set_label_image(self, image_paths):
        try:
            i_image = self.process_image
            imageq = ImageQt(image_paths[1])
            im = QImage(imageq)

            o_image = self.output_image
            self.add_image(image_paths[0], i_image)
            self.add_image(im, o_image)
        except:
            self.process_image.setText("Resim Getirelemedi")
            self.output_image.setText("Resim Getirelemedi")
   ##



##############################################################################################################################################################################################################################






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