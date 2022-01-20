
from PyQt5 import QtCore, QtGui, QtWidgets
import sys, os, webbrowser



class face_detection_ui(object):
    app = QtWidgets.QApplication(sys.argv)
    screen = app.primaryScreen()
    size = screen.size()
    
    screen_width = size.width()*0.7
    screen_height = size.height()*0.7
    def setup_fd_ui(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(self.screen_width, self.screen_height)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath('')

        self.empty_label = QtWidgets.QLabel()
        self.empty_label.setObjectName("empty_label")
        self.setWindowTitle("AKAY - Yüz Tanıma")
        self.setWindowIcon(QtGui.QIcon('icons/icon.png'))



        ##Ortak öğeleri tek yerde toplayan sınıf 

        ##Arayüzün ilk ayarları
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(self.screen_width, self.screen_height)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        cssFile ="main.css"
        with open(cssFile,"r") as fh:
                MainWindow.setStyleSheet(fh.read())

        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        ###############################

 
        self.file_path_completer = QtWidgets.QCompleter(self)
        self.file_path_completer.setModel(QtWidgets.QDirModel(self.file_path_completer))

        self.input_file_text = QtWidgets.QLabel("İncelenecek Klasörü Seçiniz")
        self.input_file_text.setObjectName("input_file_text")

        self.input_file_tree = QtWidgets.QTreeView()
        self.input_file_tree.setObjectName("input_file_tree")

        ##Ağaç Ayarlamaları##

        self.input_file_tree.setModel(self.model)
        self.input_file_tree.hideColumn(1)
        self.input_file_tree.hideColumn(2)
        self.input_file_tree.hideColumn(3)
        self.input_file_tree.setColumnWidth(0, 200)
        self.input_file_tree.doubleClicked.connect(self.input_tree_clicked)

        ##

        self.input_path_label = QtWidgets.QLineEdit("Lütfen Seçin")
        self.input_path_label.setObjectName("input_path_label")
        self.input_path_label.setCompleter(self.file_path_completer)

        self.detect_face_image_select_button = QtWidgets.QPushButton("İncelenecek Yüz")
        self.detect_face_image_select_button.setObjectName("detect_face_image_select_button")       



        self.output_file_text = QtWidgets.QLabel("Çıktıların Atılacağı Klasörü Seçiniz")
        self.output_file_text.setObjectName("output_file_text")

        self.output_file_tree = QtWidgets.QTreeView()
        self.output_file_tree.setObjectName("output_file_tree")

        #Çıktı klasör ağacı ayarlanması
        self.output_file_tree.setModel(self.model)
        self.output_file_tree.hideColumn(1)
        self.output_file_tree.hideColumn(2)
        self.output_file_tree.hideColumn(3)
        self.output_file_tree.setColumnWidth(0, 200)
        self.output_file_tree.doubleClicked.connect(self.output_tree_clicked)
        #------

        self.output_path_label = QtWidgets.QLineEdit("Lütfen Seçin")
        self.output_path_label.setObjectName("output_path_label")
        self.output_path_label.setCompleter(self.file_path_completer)

        self.file_choose_vlayout = QtWidgets.QVBoxLayout()


        self.file_choose_vlayout.addWidget(self.detect_face_image_select_button)

        self.file_choose_vlayout.addWidget(self.input_file_text)
        self.file_choose_vlayout.addWidget(self.input_file_tree)
        self.file_choose_vlayout.addWidget(self.input_path_label)

        self.file_choose_vlayout.addWidget(self.output_file_text)
        self.file_choose_vlayout.addWidget(self.output_file_tree)
        self.file_choose_vlayout.addWidget(self.output_path_label)
        ##########################

        self.process_image = QtWidgets.QLabel()
        self.process_image.setObjectName("process_image")
        self.process_image.setAlignment(QtCore.Qt.AlignCenter)

        self.output_image = QtWidgets.QLabel()
        self.output_image.setObjectName("output_image")
        self.output_image.setAlignment(QtCore.Qt.AlignCenter)
        
        self.progress_gif = QtWidgets.QLabel()
        self.progress_gif.setObjectName("progress_gif")
        self.progress_gif.setAlignment(QtCore.Qt.AlignCenter)
        
        logo_path = "icons/load.gif"
        self.load_gif = QtGui.QMovie(logo_path)
        
        #self.progress_gif.setMovie(self.load_gif)
        #self.load_gif.start()

        self.image_glayout = QtWidgets.QGridLayout()

        self.image_glayout.addWidget(self.empty_label,0,0 , 1, 2)
        self.image_glayout.addWidget(self.process_image,0,2, 1, 10)
        self.image_glayout.addWidget(self.progress_gif,0,12, 1, 2)
        self.image_glayout.addWidget(self.output_image,0,14, 1, 10)
        self.image_glayout.addWidget(self.empty_label,0,24, 1, 2)


        ##########################


        self.analyze_button = QtWidgets.QPushButton("Analiz Et")
        self.analyze_button.setObjectName("analyze_button")
        self.analyze_button.setMinimumWidth(50)
        self.analyze_button.setMinimumHeight(40)

        self.stop_process_button = QtWidgets.QPushButton("Durdur")
        self.stop_process_button.setObjectName("stop_process_button")
        self.stop_process_button.setMinimumWidth(50)
        self.stop_process_button.setMinimumHeight(40)
        
    
    
        buttons_classes_glayout = QtWidgets.QGridLayout()
        buttons_classes_glayout.addWidget(self.empty_label, 0 , 0 , 3, 10)
        buttons_classes_glayout.addWidget(self.empty_label, 3, 0 , 2, 8)
        buttons_classes_glayout.addWidget(self.empty_label, 2, 8 , 4, 2)
        buttons_classes_glayout.addWidget(self.empty_label, 0, 10, 6, 2)
        buttons_classes_glayout.addWidget(self.analyze_button, 2, 12, 4, 3)
        buttons_classes_glayout.addWidget(self.stop_process_button, 2, 15, 4, 3)
        buttons_classes_glayout.addWidget(self.empty_label, 0, 18, 6, 2)

        
        ##################################
            
        self.info_table_label = QtWidgets.QTableWidget()
        self.info_table_label.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.info_table_label.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.info_table_label.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.info_table_label.setObjectName("info_table_label")
        self.info_table_label.setColumnCount(2)
        self.info_table_label.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.info_table_label.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.info_table_label.setHorizontalHeaderItem(1, item)


        #info view labelın ayarlanması 
        self.info_table_label.setColumnWidth(0,350)
        self.info_table_label.setColumnWidth(1,80)
        self.info_table_label.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.info_table_label.cellDoubleClicked.connect(self.open_image)
        #----------------------------

        self.remaining_process_label = QtWidgets.QLabel("İşlenen Resim / Toplam Resim")
        self.remaining_process_label.setAlignment(QtCore.Qt.AlignCenter)
        self.remaining_process_label.setObjectName("remaining_process_label")

        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setObjectName("progress_bar")

        self.lcd_process_timer = QtWidgets.QLCDNumber()
        self.lcd_process_timer.setObjectName("lcd_process_timer")
        self.lcd_process_timer.setDigitCount(8)  
        
        self.version_text = QtWidgets.QLabel("Demo Sürüm")
        self.version_text.setObjectName("version_text")

        self.timer_table_glayout = QtWidgets.QGridLayout()
        self.timer_table_glayout.addWidget(self.info_table_label, 0,0,12,24)
        self.timer_table_glayout.addWidget(self.empty_label, 0, 24, 12, 2)
        self.timer_table_glayout.addWidget(self.progress_bar, 4,26,1,6)
        self.timer_table_glayout.addWidget(self.remaining_process_label, 5,26,1,5)
        self.timer_table_glayout.addWidget(self.lcd_process_timer, 8, 28, 2, 2)
        self.timer_table_glayout.addWidget(self.empty_label, 0, 32, 11, 2)
        self.timer_table_glayout.addWidget(self.version_text, 11, 32, 1, 2)



        ###################################
        all_screen_glayout = QtWidgets.QGridLayout()
        all_screen_glayout.setSpacing(5)
        all_screen_glayout.setColumnStretch(0, 1)
        all_screen_glayout.setColumnStretch(1, 6)

        all_screen_glayout.addLayout(self.file_choose_vlayout, 0, 0, 7, 1)
        all_screen_glayout.addLayout(self.image_glayout, 0, 1, 3, 2)
        all_screen_glayout.addLayout(buttons_classes_glayout, 3, 1, 1, 2)
        all_screen_glayout.addLayout(self.timer_table_glayout, 4, 1 ,3 ,1)

        
        ##Bütün ekran ayarlanıyor
        self.centralwidget.setLayout(all_screen_glayout)
        MainWindow.setCentralWidget(self.centralwidget)
        ########


        self.ui_menubar = QtWidgets.QMenuBar(self.centralwidget)
        self.ui_menubar.setAutoFillBackground(False)
        self.ui_menubar.setObjectName("ui_menubar")

        ###Qmenüler
        self.menu_files = QtWidgets.QMenu(self.ui_menubar)
        self.menu_files.setObjectName("menu_files")
        self.menu_files.setTitle("Dosya")

        self.input_folder_bar = QtWidgets.QAction()
        self.input_folder_bar.setObjectName("input_folder_bar")
        self.input_folder_bar.setText("Girdi Klasörü")
        self.input_folder_bar.triggered.connect(self.input_folder_bar_click)

        self.output_folder_bar = QtWidgets.QAction()
        self.output_folder_bar.setObjectName("output_folder_bar")
        self.output_folder_bar.setText("Çıktı Klasörü")
        self.output_folder_bar.triggered.connect(self.output_folder_bar_click)
        
        
        self.detect_face_select_bar = QtWidgets.QAction()
        self.detect_face_select_bar.setObjectName("detect_face_select_bar")
        self.detect_face_select_bar.setText("İncelenecek Yüz")
        self.detect_face_select_bar.triggered.connect(self.select_detect_face_image)

        self.menu_files.addAction(self.input_folder_bar)
        self.menu_files.addAction(self.output_folder_bar)
        self.menu_files.addAction(self.detect_face_select_bar)

        #######
        self.menu_themes = QtWidgets.QMenu(self.ui_menubar)
        self.menu_themes.setObjectName("menu_themes")
        self.menu_themes.setTitle("Temalar")

        self.light_theme = QtWidgets.QAction()
        self.light_theme.setObjectName("light_theme")
        self.light_theme.setText("Light Tema")
        self.light_theme.triggered.connect(self.light_theme_select)

        self.dark_theme = QtWidgets.QAction()
        self.dark_theme.setObjectName("dark_theme")
        self.dark_theme.setText("Dark Tema")
        self.dark_theme.triggered.connect(self.dark_theme_select)

        self.menu_themes.addAction(self.light_theme)
        self.menu_themes.addAction(self.dark_theme)
        ########

        self.menu_settings = QtWidgets.QMenu(self.ui_menubar)
        self.menu_settings.setObjectName("menu_settings")
        self.menu_settings.setTitle("Ayarlar")
        
        self.serial_key_bar = QtWidgets.QAction()
        self.serial_key_bar.setObjectName("serial_key_bar")
        self.serial_key_bar.setText("Uygulama Seri Numarası")
        self.serial_key_bar.triggered.connect(self.serial_key_bar_click)
        
        self.menu_settings.addAction(self.serial_key_bar)
        ###




        self.ui_menubar.addAction(self.menu_files.menuAction())
        self.ui_menubar.addAction(self.menu_themes.menuAction())
        self.ui_menubar.addAction(self.menu_settings.menuAction())







        self.retranslate_fd_ui()
        ##QtCore.QMetaObject.connectSlotsByName(MainWindow)####BU SATIR NE İŞE YARIYOR !!!!

    def retranslate_fd_ui(self):

        item = self.info_table_label.horizontalHeaderItem(0)
        item.setText("Resmin Yolu")
        item = self.info_table_label.horizontalHeaderItem(1)
        item.setText("Sonuç")

        #iconlar ve resimler tanıtıldı
        logo_path = "icons/face-detection1.png"
        image = self.process_image
        self.add_image(image_path=logo_path, image_label=image)

        logo_path = "icons/face-detection.png"
        image = self.output_image
        self.add_image(image_path=logo_path, image_label=image)
        #------
        

        
        #Analiz butonunun fonksyiona bağlanması 
        self.analyze_button.clicked.connect(self.face_detect_button_clicked)
        #------------

        self.detect_face_image_select_button.clicked.connect(self.select_detect_face_image)

        #Durdur butonu başta tıklanabilir olmayacak
        self.stop_process_button.clicked.connect(self.face_detect_stop_button_clicked)
        self.stop_process_button.setEnabled(False)
        #-----



        
    def input_folder_bar_click(self):
        response = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            caption='Girdi Klasörünü Seçiniz'
        )

        if str(response)  != "":
            self.input_path_label.setText(str(response))
        else:
            self.input_path_label.setText("Lütfen Klasör Seçiniz")


    def output_folder_bar_click(self):
        response = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            caption='Çıktı Klasörünü Seçiniz'
        )

        if str(response)  != "":
            self.output_path_label.setText(str(response))
        else:
            self.output_path_label.setText("Lütfen Klasör Seçiniz")

    def select_detect_face_image(self):
        file_filter = 'Resim (*.jpg *.png)'
        response = QtWidgets.QFileDialog.getOpenFileName(
            parent=self,
            caption='İncelenecek Yüzü Seçin',
            directory=os.getcwd(),
            filter=file_filter,
            initialFilter='Resim (*.jpg *.png)'
        )
        if str(response[0])  != "":
            i_image = self.process_image
            self.detect_face_image_select_button.setWhatsThis(str(response[0]))
            self.add_image(str(response[0]), i_image)


    ##Girdi klaösrünün seçildiği fonksyion
    def input_tree_clicked(self, index):
        #print("acaba")
        try:
            if os.path.isdir(self.model.filePath(index)):
                self.input_path_label.setText(self.model.filePath(index))
            else: 
                self.input_path_label.setText("Lütfen Klasör Seçiniz")
        except:
            pass
   ##---------



   ##Çıktı bilgilerinin tutulduğu tabloda çift tıklayınca girdi resminin açılması
    def open_image(self, row, column):
        try:
            if column == 0:
                item = self.info_table_label.item(row, column)
                webbrowser.open('file:///' + item.whatsThis())
        except:
            pass
   #


   ##çıktı Klasörünün seçildiği fonksiyon
    def output_tree_clicked(self, index):
        try:
            if os.path.isdir(self.model.filePath(index)):
                self.output_path_label.setText(self.model.filePath(index))
            else: 
                self.output_path_label.setText(1, "Lütfen Klasör Seçiniz")
        except:
            pass
   ##----------
