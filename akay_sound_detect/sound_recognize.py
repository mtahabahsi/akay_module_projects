import speech_recognition as sr
import os
import pandas as pd
from PyQt5.QtCore import QObject, pyqtSignal
import glob
from datetime import datetime



class sound_recognition(QObject):

    finished = pyqtSignal()
    sounds_path = str
    csv_path = str
    search_text = str
    lang = str

    info_text = pyqtSignal(list)

    sound_error = pyqtSignal(list)
    stop_bool = pyqtSignal(bool)

    def run(self):
        start_time = datetime.now()

        sound_formats = ['m4a', 'flac', 'mp3', 'mp4', 'wav', 'wma', 'aac','ogg'] 

        all_files=[]
        ##Girilen klasördeki bütün dosyalar alınıyor
        for sound_file in glob.iglob(os.path.join(self.sounds_path, "**"), recursive=True):
            all_files.append(sound_file)

        ##Bütün dosyalar arasından ses formatına uygun olanlar diziye atılıyor 
        sound_files = [x for x in all_files if x.split('.')[-1].lower() in sound_formats]
        sound_count = 0
        if len(sound_files) == 0:
                self.sound_error.emit(["Ses Dosyası Yok",  "Girdiğiniz klasörde ses dosyası bulunamadı"])
        elif self.search_text == "":
                self.sound_error.emit(["Aranacak metin !",  "Lütfen aramak istediğiniz metni giriniz"])
        else:  
                self.info_text.emit(["0/0", "empty", "empty", "empty", "empty"])
                datas = pd.DataFrame(columns=["Dosya Adı", "Metin", str(self.search_text)])
                r = sr.Recognizer()
                detected_count = 0
                status = ":::Bütün sesler incelendi:::"
                for index, sound in enumerate(sound_files):
                        try:
                                if self.stop_bool:
                                        status = "Durduruldu"
                                        break
                                sound_count = index + 1
                                with sr.AudioFile(sound) as source:

                                        audio = r.record(source)
                                try:
                                        text = r.recognize_google(audio, language=self.lang)
                                        temp_bool = False
                                        if str(self.search_text).lower() in text.lower(): 
                                                detected_count = detected_count + 1
                                                temp_bool = True
                                        datas.loc[index] = [sound, text, temp_bool]
                                        self.info_text.emit([str(index + 1) + "/" + str(len(sound_files)), sound, sound.split('/')[-1], text, temp_bool])
                                except Exception as e :
                                        datas.loc[index] = [sound, "OKUNAMADI!!!", "False"]
                                        self.info_text.emit([str(index + 1) + "/" + str(len(sound_files)), sound, sound.split('/')[-1], "Not Found", False])
                        except:
                                continue
                
                try:
                        datas.to_excel(os.path.join(self.csv_path,r"sonuclar.xlsx"))
                except:
                        pass
                
                
                finish_time = datetime.now()

                try:
                        f = open(os.path.join(self.csv_path, "akad_sonuclar.txt"), "w")
                        f.write(status + "\nBaşlangıç Zamanı==" + start_time.strftime("%d/%m/%Y %H:%M:%S") + "\n" + "Bitiş Zamanı==" + finish_time.strftime("%d/%m/%Y %H:%M:%S") + "\n" + "Geçen Süre=="  + str(finish_time - start_time) + "\n" + 
                        "Kaynak Dosya Yolu==" + self.sounds_path + "\n" + "Hedef Dosya Yolu==" + self.csv_path + "\nAranan Metin==" + str(self.search_text) + "\n" + "Toplam Ses Sayısı==" + str(len(sound_files)) + 
                        "\n" + "İncelenen Ses Sayısı==" + str(sound_count) + "\nİstenenlerin Bulunduğu Ses Sayısı==" + str(detected_count))
                        f.close()
                except:
                        pass
                self.finished.emit()





