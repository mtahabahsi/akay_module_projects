import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QInputDialog
from PyQt5.QtCore import Qt, QObject, pyqtSignal,QThread
from PyQt5.QtGui import QImage, QPixmap
import time, os , json, datetime
import user_interface,re,uuid,pymongo,requests, json
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


    def get_mac(self):
        mac_num = uuid.getnode()
        mac  = str(":".join(re.findall('..', '%012x' % mac_num)))
        return mac
    
    
    def __init__(self, parent=None):
        self.license = False
        self.user = ""
        super(MainPage, self).__init__(parent)
        self.image_interface()
        self.setAttribute(Qt.WA_DeleteOnClose)
        
        
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
                mycollection=mydb["image-detect-serial-keys"]
                if mycollection.count_documents({"key":serial_key,"mac-adress":mac_adress}):
                    self.license = True
                    key_db = mycollection.find_one({"key": serial_key})
                    self.user = key_db["user"]
                    self.version_text.setText(self.user)
                    self.menu_settings.removeAction(self.serial_key_bar)
                else:
                    self.license = False
                    self.version_text.setText("Demo Sürüm")
            except (requests.ConnectionError, requests.Timeout) as exception:
                self.critical_messagebox("Hata", "Tam Sürümü Kullanmak İçin İnternet Bağlantınızı Kontrol Ediniz!", QtWidgets.QMessageBox.Critical)



    ##Ses inceleme arayüzü başlatma 
    def image_interface(self):
        self.setup_id_ui(self)
        self.goruntu_inceleme_bar.setEnabled(False)
        self.show()
        self.setMenuBar(self.ui_menubar)
        if self.license != True:
            self.check_version()
        ChecklistDialog.clean_checked(self)
    

    def video_interface(self):
        self.setup_vfd_ui(self)
        self.video_inceleme_bar.setEnabled(False)
        self.show()
        self.setMenuBar(self.ui_menubar)
        if self.license != True:
            self.check_version()
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
            image_label.setText("Görüntüler Getirilirken Bir Hata Oluştu")
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

            self.form = ChecklistDialog(class_json_file="json_files/coco_classes.json", name="Nesne Listesi")
            if self.form.exec_():

                self.change_choose_label()
        else:            
            self.critical_messagebox("Hata", "Yaygın Suç Nesneleri Seçiliyken Bu Nesneleri Seçemezsiniz.", QtWidgets.QMessageBox.Critical)
            

    def forencrypt_button_clicked(self):
        temp_bool = True
        with open("json_files/coco_classes.json", encoding="utf-8") as f:
            json_content = json.loads(f.read())
            for json_object in json_content["classes"]:
                if json_object["check"] == "True":
                    temp_bool = False  
        if temp_bool:
            self.form = ChecklistDialog(class_json_file="json_files/custom_classes.json", name="Yaygın Suç Nesnleri")
            if self.form.exec_():
                self.change_choose_label()
        else:
            self.critical_messagebox("Hata", "Nesne Listesi Seçiliyken Bu Nesneleri Seçemezsiniz.", QtWidgets.QMessageBox.Critical)
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
            if len(nesneler) > 80:
                self.choose_class_label.setText("Aranacak Nesneler : " + nesneler[:80] + "...")
            else:
                self.choose_class_label.setText("Aranacak Nesneler : " + nesneler)
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
            if not os.path.isfile(self.input_path_label.text()) or not "mp4" in self.input_path_label.text():
                self.critical_messagebox("Video Hatası", "Analiz Edilecek Videoyu Kontrol Ediniz!", QtWidgets.QMessageBox.Critical)
            elif not os.path.isdir(self.output_path_label.text()):
                self.critical_messagebox("Klasör Hatası", "Çıktıların Atılacağı Klasörü Kontrol Ediniz!", QtWidgets.QMessageBox.Critical)
            elif self.choose_class_label.text() == "Aranacak nesneler : ":
               self.critical_messagebox("Hata", "Lütfen Aramak İstediğiniz Nesneleri Seçiniz.", QtWidgets.QMessageBox.Critical)
            else:
                fps = 1.0 / float(self.frame_combobox.currentText())
                
                self.start_image_analyze(fps=fps)
        except:
            pass
   #

   ##resim aracında inceleme butonunun kodları
    def image_detection_analyze_button_clicked(self):
        try:
            if not os.path.isdir(self.input_path_label.text()):
                self.critical_messagebox("Klasör Hatası", "Analiz Edilecek Klasörü Kontrol Ediniz!", QtWidgets.QMessageBox.Critical)
            elif not os.path.isdir(self.output_path_label.text()):
                self.critical_messagebox("Klasör Hatası", "Çıktıların Atılacağı Klasörü Kontrol Ediniz!", QtWidgets.QMessageBox.Critical)
            elif self.choose_class_label.text() == "Aranacak Nesneler : ":
                self.critical_messagebox("Hata", "Lütfen Aramak İstediğiniz Nesneleri Seçiniz.", QtWidgets.QMessageBox.Critical)
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
            
        ##Çıktı klasörü zaman damgası ile oluşturuluyor 
        starting_time = datetime.datetime.now()
        path = os.path.join(output_folder_path, "AKAY-" + str(starting_time).split(".")[0].replace(" ", "-").replace(":","-"))
        os.makedirs(path, exist_ok=True)
        output_folder_path = path

        input_folder_path = self.input_path_label.text().split("/")[0] + "/"
        for dirs in self.input_path_label.text().split("/"):
            input_folder_path = os.path.join(input_folder_path , dirs)
                
        self.progress_gif.setMovie(self.load_gif)
        self.load_gif.start()

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
        self.worker.license = self.license
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

        self.worker.detect_error.connect(self.error_dialog)

        self.thread.start()
        self.timer_thread.start()

        self.stop_process_button.setEnabled(True)
        self.menu_tools.setEnabled(False)
        self.menu_files.setEnabled(False)
        self.menu_settings.setEnabled(False)
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



    def error_dialog(self, err_strings):
        self.thread.quit()
        self.critical_messagebox(str(err_strings[0]), str(err_strings[1]), QtWidgets.QMessageBox.Critical)




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
            self.menu_settings.setEnabled(True)
            self.progress_gif.clear()
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
                self.remaining_process_label.setText("Durduruldu")
                if self.license:
                    self.question_messagebox("İşlem Durduruldu", "<b>Çıktı Klasörüne Gitmek İster Misiniz?</b>")
                else:
                    self.question_messagebox("İşlem Durduruldu", "<b>Çıktı Klasörüne Gitmek İster Misiniz?</b><br>Bu Bir Demo Sürümdür, En Fazla 10 Görüntü ya da 1 Dakika Video İnceleyebilirsiniz.<br><a href='https://www.forencrypt.com/iletisim/'>Tam Sürüm İçin Bize Ulaşın</a>")
            else:
                if self.license:
                    self.question_messagebox("İşlem Bitti", "<b>Çıktı Klasörüne Gitmek İster Misiniz?</b>")
                else:
                    self.question_messagebox("İşlem Bitti", "<b>Çıktı Klasörüne Gitmek İster Misiniz?</b><br>Bu Bir Demo Sürümdür, En Fazla 10 Görüntü ya da 1 Dakika Video İnceleyebilirsiniz.<br><a href='https://www.forencrypt.com/iletisim/'>Tam Sürüm İçin Bize Ulaşın</a>")

        except:
            pass
   #



   #Durdur butonuna basıldığı zaman işlemi sonlandıran fonksiyon
    def stop_button_clicked(self):
        try:
            self.worker.stop_bool = True
            self.remaining_process_label.setText("Durduruluyor")
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
                self.info_table_label.setItem(rowPosition , 2, QtWidgets.QTableWidgetItem(info_array[3]))
                if info_array[3] == "Var":
                        self.info_table_label.item(rowPosition, 2).setBackground(QtGui.QColor(0, 255, 0))
                        self.info_table_label.item(rowPosition, 2).setForeground(QtGui.QColor(0, 0, 0))
                else:
                    self.info_table_label.item(rowPosition, 2).setBackground(QtGui.QColor(255,0,0))
                    self.info_table_label.item(rowPosition, 2).setForeground(QtGui.QColor(0,0,0))
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
            self.process_image.setText("Görüntü Getirelemedi")
            self.output_image.setText("Görüntü Getirelemedi")
   ##



##############################################################################################################################################################################################################################






############# messagebox methodları ######################






    def critical_messagebox(self, title, msg, type = QtWidgets.QMessageBox.Critical):
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
            webbrowser.open('file:///' + self.worker.output_path)
        elif msgbox.clickedButton() == no_button:
            msgbox.close()




##########################################################
        
    def serial_key_bar_click(self):
        dialog = QInputDialog(self)
        dialog.setWindowTitle("Ürün Anahtarı")
        dialog.setLabelText("Ürün Anahtarını Giriniz.")    
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
                mycollection=mydb["image-detect-serial-keys"]
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
                        self.critical_messagebox("Harika!", "Uygulamanız Tam Sürüm Olmuştur", QtWidgets.QMessageBox.Information)
                        self.user = key_db["user"]
                        self.version_text.setText(self.user)
                        self.license = True
                        self.menu_settings.removeAction(self.serial_key_bar)
                    else: 
                        if key_db["mac-adress"] != self.get_mac(): 
                            self.critical_messagebox("Hata", "Girdiğiniz Ürün Anahtarı Başkası Tarafından Kullanılıyor!", QtWidgets.QMessageBox.Critical)
                        else: 
                            self.critical_messagebox("Bilgi", "Ürün Etkinleştirildi!", QtWidgets.QMessageBox.Information)
                            self.user = key_db["user"]
                            self.version_text.setText(self.user)    
                            json_file = open("serial_key.json", "w+")
                            json.dump({ "serial_key": text }, json_file) 
                            json_file.close()
                            self.license = True
                            self.menu_settings.removeAction(self.serial_key_bar)
                else:
                    self.critical_messagebox("Hata", "Girdiğiniz anahtar doğru değil!", QtWidgets.QMessageBox.Critical)
            except (requests.ConnectionError, requests.Timeout) as exception:
                self.critical_messagebox("Hata", "Tam Sürümü Kullanmak İçin İnternet Bağlantınızı Kontrol Ediniz!", QtWidgets.QMessageBox.Critical)
        else:
            print("canceled")
    
    
    def usage_doc_click(self):
        print("tıkla baba")
        webbrowser.open('file:///' + os.path.join(os.getenv('APPDATA'), "Akay Nesne Tanıma", "Kullanım Kılavuzu.pdf"))




    def dark_theme_select(self):
        #buraya css eklenebilir
        app.setStyleSheet(qdarkstyle.load_stylesheet())

    
    def light_theme_select(self):

        app.setStyleSheet("")

app = QApplication(sys.argv)
pencere = MainPage()
sys.exit(app.exec_())