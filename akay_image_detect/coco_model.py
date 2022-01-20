import torch, os, glob, json
from datetime import datetime 
from PyQt5.QtCore import QObject, pyqtSignal
import cv2
import pandas as pd
import datetime as dt
import shutil


class CocoModel(QObject):


    finished = pyqtSignal()

    change_image = pyqtSignal(list)
    info_text = pyqtSignal(list)

    stop_bool = pyqtSignal(bool)

    input_path = str
    output_path = str
    model_file = bool

    fps = float
    license = bool

    def get_classes_turkish(self,detect_classes):
        if self.model_file:
            path = "json_files/coco_classes.json"
        else:
            path = "json_files/custom_classes.json"

        with open(path, encoding="utf-8") as f:
            json_content = json.loads(f.read())
            #print(detect_classes)
            if detect_classes.strip():
                result = ""
                arr = []
                if "," in detect_classes:
                    arr = detect_classes.split(",")
                else:
                    arr = [detect_classes]

                for el in arr:
                    #print(el.split(" ")[1])
                    json_id = json_id =  ''.join([i for i in el if not i.isdigit()])
                    json_id = json_id.strip()

                    if int(el.split(" ")[1]) > 1 :
                        json_id = json_id[:-1] #eğer birden fazla nesne varsa sondaki "s" takısını atmak için 
                        #print(json_id)

                    for json_object in json_content["classes"]:
                        if json_object["id"] == json_id:
                            result += el.split(" ")[1] + " " + json_object["turkish"] + ","
                            break # objenin türkçesi bulunduysa döngüden çık
                
                
                result = result[:-1] #en sondaki virgülü kaldırmak için
                result = result.replace("(CDS)","")
                return result
            else:
                return "Nesne Bulunamadı"


    
    

    def get_image_files(self, path):
        img_formats = ['bmp', 'jpg', 'jpeg', 'png', 'tif', 'tiff', 'dng', 'webp', 'mpo'] 
        files = []
        self.info_text.emit(["Görüntüler Toplanıyor...", "empty","empty"])
        for image_file in glob.iglob(os.path.join(path, "**"), recursive=True):
            if self.stop_bool:
                files = []
                break
            files.append(image_file)
        return [x for x in files if x.split('.')[-1].lower() in img_formats]




    def image_detect(self, img):

        try:
            results = self.model(img) 

            cikti_text = results.print()
            results.save(os.path.join(self.output_path, "temp"))

            im0 = results.get_image()

            found_bool = False
            for (x, y) in  zip(self.searched_objects, self.objects_turkish):
                if x in cikti_text:
                    found_bool = True
                    results.save(os.path.join(self.output_path, y))
            
            self.change_image.emit([str(img), im0])
            try:
                detect_class = ' '.join(cikti_text.split(" ")[3:])
            except:
                detect_class = "Bulunamadı"
            detect_class = " " + detect_class
            print(cikti_text)
            


            count_searched_object = []
            for x in self.searched_objects:
                if x in detect_class:
                    count_searched_object.append(detect_class.split(x)[0].split(" ")[-2].rstrip())
                else:
                    count_searched_object.append("0")

            detect_class = self.get_classes_turkish(detect_class)           
            excel_array = [img] + [detect_class] + count_searched_object 

            self.datas.loc[self.count] = excel_array
                    
            self.count = self.count + 1

            self.info_text.emit([str(self.count) +  "/" + str(self.total_picture) , img, detect_class, "Var" if found_bool else "Yok"])

            os.remove(os.path.join(self.output_path, "temp\\" + img.split("\\")[-1]))            
            if os.path.isfile(self.input_path):
                os.remove(os.path.join(img))


        except:
            print("Resim detect edilemedi")
            pass

    def get_searched_objects(self):
        self.searched_objects = []
        self.objects_turkish = []
        ##Yolo modeli ise
        if self.model_file:
            self.model = torch.hub.load("weight_files", "yolov5x", source="local")
            with open("json_files/coco_classes.json", encoding="utf-8") as f:
                json_content = json.loads(f.read())
                for json_object in json_content["classes"]:
                    if json_object["check"] == "True":
                        self.searched_objects.append(json_object["id"])
                        self.objects_turkish.append(json_object["turkish"])
        ##Custom Model ise
        else:
            self.model = torch.hub.load("weight_files", "custom", source="local")
            
            with open("json_files/custom_classes.json", encoding="utf-8") as f:
                json_content = json.loads(f.read())
                for json_object in json_content["classes"]:
                    if json_object["check"] == "True":
                        self.searched_objects.append(json_object["id"])
                        self.objects_turkish.append(json_object["turkish"])


        ##Aranan nesneler belirlendikten sonra çıktı yoluna klasörleri oluşturuluyor
        for i in self.objects_turkish:
            path = os.path.join(self.output_path, i)
            os.makedirs(path, exist_ok=True)

        ###cikti resimlerinin atılacağı klasör 
            path = os.path.join(self.output_path, "temp")
            os.makedirs(path, exist_ok=True)
    

    def run(self):
        
        start_time = datetime.now()

        self.get_searched_objects()


        self.total_picture = 0

        if not self.stop_bool:
            ##### bi başlangıç ayarlamaları arayüz ve xlsx dosyası
            self.datas = pd.DataFrame(columns=["Dosya Adı", "İçerdiği Nesneler"] + self.objects_turkish)
            self.count = 0
            ###########################
        

            if os.path.isdir(self.input_path):
                images_array = self.get_image_files(self.input_path)
                self.total_picture = len(images_array)
                for img in images_array:        
                    if self.stop_bool:
                        break
                    if self.count >= 10 and self.license == False:
                        break
                    self.image_detect(img)
                shutil.rmtree(os.path.join(self.output_path, "temp"))



            elif os.path.isfile(self.input_path): 
                path = os.path.join(self.output_path, "frames")
                os.makedirs(path, exist_ok=True)
                vidcap = cv2.VideoCapture(self.input_path)
                saniye = float(vidcap.get(cv2.CAP_PROP_FRAME_COUNT)) / float(vidcap.get(cv2.CAP_PROP_FPS))
                our_frame = int(saniye / self.fps)
                self.total_picture = our_frame

                def getFrame(sec):
                    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
                    hasFrames,image = vidcap.read()
                    if hasFrames:
                        a = str(dt.timedelta(seconds=sec))
                        if "." not in a: 
                            a = a + ".000000"
                        
                        a = a[:-4]
                        a = a.replace(".",",")
                        a = a.split(":")
                        b = ""
                        b = (b + str(a[0]) + "saat") if int(a[0]) != 0 else b
                        b = (b + str(a[1]) + "dk") if int(a[1]) != 0 else b 
                        b = (b + str(a[2]) + "sn") 
                        #cv2.imwrite(os.path.join(self.output_path, "frames\\" + str(b) +".jpg"), image) # save frame as JPG file
                        
                        im_save_path = os.path.join(self.output_path, "frames\\" + str(b) +".jpg")
                        is_success, im_buf_arr = cv2.imencode(".jpg", image)
                        im_buf_arr.tofile(im_save_path)
                        
                        
                        self.image_detect(os.path.join(self.output_path, "frames\\" + str(b) + ".jpg"))
                    return hasFrames
                sec = 0
                frameRate = self.fps #//it will capture image in each 0.5 second
                count=1
                success = getFrame(sec)
                while success:
                    if self.stop_bool:
                        break
                    #Sadece bir dakika inceleyebilsin
                    if sec >= 60 and self.license == False:
                        break
                    count = count + 1
                    sec = sec + frameRate
                    sec = round(sec, 2)
                    success = getFrame(sec)
                shutil.rmtree(os.path.join(self.output_path, "temp"))
                shutil.rmtree(os.path.join(self.output_path, "frames"))
                

                    
        finish_time = datetime.now()

        try:
            if self.stop_bool:
                status = "Durduruldu"
            else:
                status = ":::Hepsi incelendi:::"
                #self.info_text.emit([str(self.total_picture)  + "/" + str(self.total_picture) , "empty","empty"])
        except:
            pass

        try:
            f = open(os.path.join(self.output_path, "akay_sonuclar.txt"), "w")
            f.write(status + "\nBaşlangıç Zamanı==" + start_time.strftime("%d/%m/%Y %H:%M:%S") + "\n" + "Bitiş Zamanı==" + finish_time.strftime("%d/%m/%Y %H:%M:%S") + "\n" + "Geçen Süre=="  + str(finish_time - start_time) + "\n" + 
                "Kaynak Dosya Yolu==" + self.input_path + "\n" + "Hedef Dosya Yolu==" + self.output_path + "\nAranan Nesneler==" + str(self.objects_turkish) + "\n" + "Toplam Görüntü Sayısı==" + str(self.total_picture) + 
                "\n" + "İncelenen Görüntü Sayısı==" + str(self.count))
            f.close()
        except:
            pass
        


        try:
            self.datas.to_excel(os.path.join(self.output_path, "sonuclar.xlsx"))
        except:
            pass

        self.finished.emit()




