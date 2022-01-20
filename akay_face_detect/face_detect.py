import os
import glob
from PyQt5.QtCore import QObject, pyqtSignal
from datetime import datetime 
import pandas as pd
import matplotlib.pyplot as plt 
import cv2
import numpy as np
from keras_vggface.vggface import VGGFace
from tensorflow.keras.preprocessing import image
from keras_vggface import utils
from sklearn.metrics import pairwise
import shutil


class face_recognition(QObject):

    prototxt="weight_files\\deploy.prototxt.txt"
    model="weight_files\\res10_300x300_ssd_iter_140000.caffemodel"

    net = cv2.dnn.readNetFromCaffe(prototxt,model)

    finished = pyqtSignal()

    change_image = pyqtSignal(str)
    info_text = pyqtSignal(list)

    stop_bool = pyqtSignal(bool)

    input_path = str
    output_path = str
    detect_face_image = str

    detect_error = pyqtSignal(list)
    license = bool


    def get_image_files(self):
        #DeepFace sınıfı sadece jpg ve png resimleri inceleyebiliyor 
        img_formats = ['jpg','png'] 
        files = []
        self.info_text.emit(["Resimler Toplanıyor...", "empty","empty"])
        for image_file in glob.iglob(os.path.join(self.input_path, "**"), recursive=True):
            if self.stop_bool:
                files = []
                break
            files.append(image_file)
        return [x for x in files if x.split('.')[-1].lower() in img_formats]

    def get_images_distance(self, source_img, target_img):

        resnet_model = VGGFace(model='resnet50', input_shape=(200,200,3) ,include_top=False,pooling="avg")

        img = image.load_img(source_img, target_size=(200, 200,3))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = utils.preprocess_input(x, version=2) # or version=2
        preds = resnet_model.predict(x)


        img1 = image.load_img(target_img, target_size=(200, 200,3))
        x1 = image.img_to_array(img1)
        x1 = np.expand_dims(x1, axis=0)
        x1 = utils.preprocess_input(x1, version=2) # or version=2
        preds1 = resnet_model.predict(x1)



        result = pairwise.cosine_distances(preds, preds1)

        result = result[0][0]
        print(result)
        return result


    def run(self):
        start_time = datetime.now()

        path = os.path.join(self.output_path, "bulunanlar")
        os.makedirs(path, exist_ok=True)

        self.datas = pd.DataFrame(columns=["Aranan Yüz", "Arandığı Resim", "Sonuç"])


        all_images = self.get_image_files()

        self.info_text.emit(["0/" + str(len(all_images)), "empty","empty"])

        ##Girdi resminden yüzün çıkartılması 
        #image = cv2.imread(self.detect_face_image)
        try:
            image = cv2.imdecode(np.fromfile(self.detect_face_image, dtype=np.uint8),
                    cv2.IMREAD_UNCHANGED)

            (h, w) = image.shape[:2]
            blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

            self.net.setInput(blob)
            detections = self.net.forward()
            count = 0
            for i in range(0, detections.shape[2]):

                confidence = detections[0, 0, i, 2]
                
                if confidence > 0.5:
                    count += 1

                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")

                    ss = image[startY:endY, startX:endX]
                    

                    im_save_path = os.path.join(self.output_path, "aranan_yuz.jpg")
                    is_success, im_buf_arr = cv2.imencode(".jpg", ss)
                    im_buf_arr.tofile(im_save_path)
                            
            if len(all_images) == 0:
                self.detect_error.emit(["Görüntü Dosyası Yok",  "İncelenecek klasörde görüntü dosyası bulunamadı!"])
            elif count == 0:
                self.detect_error.emit(["Girilen Görüntüde Yüz Yok",  "İncelenecek yüzün seçildiği görüntüde yüz bulunamadı!"])
            elif count > 1:
                self.detect_error.emit(["Girilen Görüntüde Birden Fazla Yüz Var",  "İncelenecek yüzün seçildiği görüntüde birden fazla yüz var!<br>Lütfen tek bir kişiyi içeren görüntü seçiniz!"])
            else:
                count = 0
                for file in all_images:
                    if self.stop_bool:
                        break


                    self.change_image.emit(file)

                    try:
                        found = False
                        #image = cv2.imread(file)

                        image = cv2.imdecode(np.fromfile(file, dtype=np.uint8),
                                cv2.IMREAD_UNCHANGED)

                        (h, w) = image.shape[:2]
                        blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))

                        self.net.setInput(blob)
                        detections = self.net.forward()
                        for i in range(0, detections.shape[2]):
                            if self.stop_bool:
                                break
                            
                            
                            try:

                                confidence = detections[0, 0, i, 2]
                                
                                if confidence > 0.5:


                                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                                    (startX, startY, endX, endY) = box.astype("int")

                                    ss = image[startY:endY, startX:endX]
                                    
                                    im_save_path = os.path.join(self.output_path, "temp.jpg")
                                    # encode the im_resize into the im_buf_arr, which is a one-dimensional ndarray
                                    is_success, im_buf_arr = cv2.imencode(".jpg", ss)
                                    im_buf_arr.tofile(im_save_path)

                                    distance = self.get_images_distance(os.path.join(self.output_path, "aranan_yuz.jpg"), os.path.join(self.output_path, "temp.jpg"))

                                    if distance < 0.4: 
                                        print("Bulundu")
                                        found = True

                                    os.remove(os.path.join(self.output_path, "temp.jpg"))


                            except:
                                pass

                        excel_array = [self.detect_face_image, file, "Var" if found else "Yok"]
                        self.datas.loc[count] = excel_array
                        self.info_text.emit([str(count + 1) +  "/" + str(len(all_images)) , str(file), "Var" if found else "Yok"])
                        if found:
                            shutil.copy2(file, os.path.join(self.output_path, "bulunanlar"))


                    except:
                        self.info_text.emit([str(count + 1) +  "/" + str(len(all_images)) , str(file), "Yok"])
                        self.datas.loc[count] = [self.detect_face_image, file, "Yok"]
                        pass
                    
                    count += 1

                    #Demo sürüm özelliği
                    if count >= 10 and self.license == False:
                        break




                finish_time = datetime.now()

                try:
                    if self.stop_bool:
                        status = "Durduruldu"
                    else:
                        status = ":::İnceleme Tamamlandı:::"
                        #self.info_text.emit([str(len(all_images))  + "/" + str(len(all_images)) , "empty","empty"])
                except:
                    pass

                try:
                    f = open(os.path.join(self.output_path, "akay_sonuclar.txt"), "w")
                    f.write(status + "\nBaşlangıç Zamanı==" + start_time.strftime("%d/%m/%Y %H:%M:%S") + "\n" + "Bitiş Zamanı==" + finish_time.strftime("%d/%m/%Y %H:%M:%S") + "\n" + "Geçen Süre=="  + str(finish_time - start_time) + "\n" + 
                        "Kaynak Dosya Yolu==" + self.input_path + "\n" + "Hedef Dosya Yolu==" + self.output_path + "\nAranan Yüz==" + str(self.detect_face_image) + "\n" + "Toplam Resim Sayısı==" + str(len(all_images)) + 
                        "\n" + "İncelenen Resim Sayısı==" + str(count))
                    f.close()
                except:
                    pass
                
                try:
                    self.datas.to_excel(os.path.join(self.output_path, "sonuclar.xlsx"))
                except:
                    pass

                self.finished.emit()
        except:
            self.detect_error.emit(["Görüntü Okuma Hatası",  "Seçtiğiniz görüntü dosyası bozuk.Lütfen farklı bir görüntü deneyin."])