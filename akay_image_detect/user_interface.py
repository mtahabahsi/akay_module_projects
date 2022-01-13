from platform import version
from PyQt5 import QtCore, QtGui, QtWidgets
import sys, os, webbrowser
from PyQt5.QtCore import QModelIndex, Qt




class common_features_ui(object):


    def __init__(self, pencere):
        pencere.empty_label = QtWidgets.QLabel()
        pencere.empty_label.setObjectName("empty_label")
        pencere.setWindowTitle("AKAY - Nesne Tanıma")
        pencere.setWindowIcon(QtGui.QIcon('icons/icon.png'))
        self.model = QtWidgets.QFileSystemModel()

        self.model.setRootPath('')



    def left_field(self, pencere):

        pencere.file_path_completer = QtWidgets.QCompleter(pencere)
        pencere.file_path_completer.setModel(QtWidgets.QDirModel(pencere.file_path_completer))

        pencere.input_file_text = QtWidgets.QLabel("İncelenecek Klasörü Seçiniz")
        pencere.input_file_text.setObjectName("input_file_text")

        pencere.input_file_tree = QtWidgets.QTreeView()
        pencere.input_file_tree.setObjectName("input_file_tree")

        ##Ağaç Ayarlamaları##

        pencere.input_file_tree.setModel(self.model)
        pencere.input_file_tree.hideColumn(1)
        pencere.input_file_tree.hideColumn(2)
        pencere.input_file_tree.hideColumn(3)
        pencere.input_file_tree.setColumnWidth(0, 200)

        ##

        pencere.input_path_label = QtWidgets.QLineEdit("Lütfen Seçin")
        pencere.input_path_label.setObjectName("input_path_label")
        pencere.input_path_label.setCompleter(pencere.file_path_completer)

        pencere.output_file_text = QtWidgets.QLabel("Çıktıların atılacağı klasörü seçiniz")
        pencere.output_file_text.setObjectName("output_file_text")

        pencere.output_file_tree = QtWidgets.QTreeView()
        pencere.output_file_tree.setObjectName("output_file_tree")

        #Çıktı klasör ağacı ayarlanması
        pencere.output_file_tree.setModel(self.model)
        pencere.output_file_tree.hideColumn(1)
        pencere.output_file_tree.hideColumn(2)
        pencere.output_file_tree.hideColumn(3)
        pencere.output_file_tree.setColumnWidth(0, 200)
        pencere.output_file_tree.doubleClicked.connect(pencere.output_tree_clicked)
        #------

        pencere.output_path_label = QtWidgets.QLineEdit("Lütfen Seçin")
        pencere.output_path_label.setObjectName("output_path_label")
        pencere.output_path_label.setCompleter(pencere.file_path_completer)

        pencere.file_choose_vlayout = QtWidgets.QVBoxLayout()


        pencere.file_choose_vlayout.addWidget(pencere.input_file_text)
        pencere.file_choose_vlayout.addWidget(pencere.input_file_tree)
        pencere.file_choose_vlayout.addWidget(pencere.input_path_label)

        pencere.file_choose_vlayout.addWidget(pencere.output_file_text)
        pencere.file_choose_vlayout.addWidget(pencere.output_file_tree)
        pencere.file_choose_vlayout.addWidget(pencere.output_path_label)

    def image_field(self, pencere):
        pencere.process_image = QtWidgets.QLabel()
        pencere.process_image.setObjectName("process_image")
        pencere.process_image.setAlignment(QtCore.Qt.AlignCenter)

        pencere.output_image = QtWidgets.QLabel()
        pencere.output_image.setObjectName("output_image")
        pencere.output_image.setAlignment(QtCore.Qt.AlignCenter)
        
        pencere.progress_gif = QtWidgets.QLabel()
        pencere.progress_gif.setObjectName("progress_gif")
        pencere.progress_gif.setAlignment(QtCore.Qt.AlignCenter)
        
        logo_path = "icons/load.gif"
        pencere.load_gif = QtGui.QMovie(logo_path)

        #pencere.progress_gif.setMovie(pencere.load_gif)
        #pencere.load_gif.start()
        pencere.image_glayout = QtWidgets.QGridLayout()

        pencere.image_glayout.addWidget(pencere.empty_label,0,0 , 1, 2)
        pencere.image_glayout.addWidget(pencere.process_image,0,2, 1, 10)
        pencere.image_glayout.addWidget(pencere.progress_gif,0,12, 1, 2)
        pencere.image_glayout.addWidget(pencere.output_image,0,14, 1, 10)
        pencere.image_glayout.addWidget(pencere.empty_label,0,24, 1, 2)

    def menu_bar(self, pencere):
        
        pencere.ui_menubar = QtWidgets.QMenuBar(pencere.centralwidget)
        pencere.ui_menubar.setAutoFillBackground(False)
        pencere.ui_menubar.setObjectName("ui_menubar")

        ###Qmenüler
        pencere.menu_files = QtWidgets.QMenu(pencere.ui_menubar)
        pencere.menu_files.setObjectName("menu_files")

        pencere.input_folder_bar = QtWidgets.QAction()
        pencere.input_folder_bar.setObjectName("input_folder_bar")

        pencere.output_folder_bar = QtWidgets.QAction()
        pencere.output_folder_bar.setObjectName("output_folder_bar")

        pencere.menu_files.addAction(pencere.input_folder_bar)
        pencere.menu_files.addAction(pencere.output_folder_bar)


        pencere.menu_themes = QtWidgets.QMenu(pencere.ui_menubar)
        pencere.menu_themes.setObjectName("menu_themes")

        pencere.light_theme = QtWidgets.QAction()
        pencere.light_theme.setObjectName("light_theme")

        pencere.dark_theme = QtWidgets.QAction()
        pencere.dark_theme.setObjectName("dark_theme")

        pencere.menu_themes.addAction(pencere.light_theme)
        pencere.menu_themes.addAction(pencere.dark_theme)

        pencere.menu_tools = QtWidgets.QMenu(pencere.ui_menubar)
        pencere.menu_tools.setObjectName("menu_tools")

        pencere.goruntu_inceleme_bar = QtWidgets.QAction()
        pencere.goruntu_inceleme_bar.setObjectName("goruntu_inceleme_bar")
        pencere.menu_tools.addAction(pencere.goruntu_inceleme_bar)

        pencere.video_inceleme_bar = QtWidgets.QAction()
        pencere.video_inceleme_bar.setObjectName("video_inceleme_bar")
        pencere.menu_tools.addAction(pencere.video_inceleme_bar)

        pencere.menu_files.setTitle("Dosya")
        pencere.menu_tools.setTitle("Araçlar")
        pencere.menu_themes.setTitle("Temalar")
        
        pencere.menu_settings = QtWidgets.QMenu(pencere.ui_menubar)
        pencere.menu_settings.setObjectName("menu_settings")
        pencere.menu_settings.setTitle("Ayarlar")
        
        pencere.serial_key_bar = QtWidgets.QAction()
        pencere.serial_key_bar.setObjectName("serial_key_bar")
        pencere.serial_key_bar.setText("Uygulama Seri Numarası")
        
        pencere.menu_settings.addAction(pencere.serial_key_bar)

        pencere.video_inceleme_bar.setText("Video İnceleme Aracı")
        pencere.goruntu_inceleme_bar.setText("Görüntü İnceleme Aracı")
        pencere.light_theme.setText("Light Tema")
        pencere.dark_theme.setText("Dark Tema")
        pencere.input_folder_bar.setText("Girdi Klasörü")
        pencere.output_folder_bar.setText("Çıktı Klasörü")

        
        pencere.output_folder_bar.triggered.connect(pencere.output_folder_bar_click)
        pencere.video_inceleme_bar.triggered.connect(pencere.video_interface)
        pencere.goruntu_inceleme_bar.triggered.connect(pencere.image_interface)
        pencere.serial_key_bar.triggered.connect(pencere.serial_key_bar_click)
        pencere.dark_theme.triggered.connect(pencere.dark_theme_select)
        pencere.light_theme.triggered.connect(pencere.light_theme_select)

        ###Qmenüler
        
        pencere.ui_menubar.addAction(pencere.menu_files.menuAction())
        pencere.ui_menubar.addAction(pencere.menu_tools.menuAction())
        pencere.ui_menubar.addAction(pencere.menu_themes.menuAction())
        if pencere.license != True:
            pencere.ui_menubar.addAction(pencere.menu_settings.menuAction())

    def right_down_field(self, pencere):        
        pencere.info_table_label = QtWidgets.QTableWidget()
        pencere.info_table_label.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        pencere.info_table_label.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        pencere.info_table_label.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        pencere.info_table_label.setObjectName("info_table_label")
        pencere.info_table_label.setColumnCount(3)
        pencere.info_table_label.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        pencere.info_table_label.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        pencere.info_table_label.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        pencere.info_table_label.setHorizontalHeaderItem(2, item)

        #info view labelın ayarlanması 
        pencere.info_table_label.setColumnWidth(0,250)
        pencere.info_table_label.setColumnWidth(1,250)
        pencere.info_table_label.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        pencere.info_table_label.cellDoubleClicked.connect(pencere.open_image)
        #----------------------------

        pencere.remaining_process_label = QtWidgets.QLabel("İşlenen görüntü / Toplam görüntü")
        pencere.remaining_process_label.setAlignment(QtCore.Qt.AlignCenter)
        pencere.remaining_process_label.setObjectName("remaining_process_label")

        pencere.progress_bar = QtWidgets.QProgressBar()
        pencere.progress_bar.setObjectName("progress_bar")

        pencere.lcd_process_timer = QtWidgets.QLCDNumber()
        pencere.lcd_process_timer.setObjectName("lcd_process_timer")
        pencere.lcd_process_timer.setDigitCount(8)  
        
        pencere.version_text = QtWidgets.QLabel("Demo Sürüm")
        pencere.version_text.setObjectName("version_text")
        if pencere.license:
            pencere.version_text.setText(pencere.user)            

        
        
        pencere.timer_table_glayout = QtWidgets.QGridLayout()
        pencere.timer_table_glayout.addWidget(pencere.info_table_label, 0,0,12,24)
        pencere.timer_table_glayout.addWidget(pencere.empty_label, 0, 24, 12, 2)
        pencere.timer_table_glayout.addWidget(pencere.progress_bar, 4,26,1,6)
        pencere.timer_table_glayout.addWidget(pencere.remaining_process_label, 5,26,1,5)
        pencere.timer_table_glayout.addWidget(pencere.lcd_process_timer, 8, 28, 2, 2)
        pencere.timer_table_glayout.addWidget(pencere.empty_label, 0, 32, 11, 2)
        pencere.timer_table_glayout.addWidget(pencere.version_text, 11, 32, 1, 2)




class image_detection_ui(object):
    app = QtWidgets.QApplication(sys.argv)
    screen = app.primaryScreen()
    size = screen.size()
    
    screen_width = size.width()*0.7
    screen_height = size.height()*0.7
    def setup_id_ui(self, MainWindow, image_mount_bool = False):

        ##Ortak öğeleri tek yerde toplayan sınıf 
        self.common = common_features_ui(self)

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

        self.common.left_field(self)
        self.input_file_text.setText("Lütfen Klasör Seçiniz")
        ##########################

        self.common.image_field(self)

        ##########################

        self.choose_class_label = QtWidgets.QLabel()
        self.choose_class_label.setWordWrap(True)
        self.choose_class_label.setAlignment(QtCore.Qt.AlignLeft)
        self.choose_class_label.setObjectName("choose_class_label")


        self.forencrypt_model_button = QtWidgets.QPushButton("Yaygın Suç Nesneleri")
        self.forencrypt_model_button.setObjectName("forencrypt_model_button")
        button_icon = QtGui.QPixmap("icons/for-logo.png");
        self.forencrypt_model_button.setIcon(QtGui.QIcon(button_icon))

        self.cocodataset_button = QtWidgets.QPushButton("Nesne Listesi")
        self.cocodataset_button.setObjectName("cocodataset_button")
        button_icon = QtGui.QPixmap("icons/coco-logo.png");
        self.cocodataset_button.setIcon(QtGui.QIcon(button_icon))

        self.analyze_button = QtWidgets.QPushButton("Analiz Et")
        self.analyze_button.setObjectName("analyze_button")
        self.analyze_button.setMinimumWidth(50)
        self.analyze_button.setMinimumHeight(40)

        self.stop_process_button = QtWidgets.QPushButton("Durdur")
        self.stop_process_button.setObjectName("stop_process_button")
        self.stop_process_button.setMinimumWidth(50)
        self.stop_process_button.setMinimumHeight(40)


        buttons_classes_glayout = QtWidgets.QGridLayout()
        buttons_classes_glayout.addWidget(self.choose_class_label, 0 , 0 , 3, 10)
        buttons_classes_glayout.addWidget(self.forencrypt_model_button, 3, 0 , 2, 8)
        buttons_classes_glayout.addWidget(self.cocodataset_button, 3, 8 , 2, 2)
        buttons_classes_glayout.addWidget(self.empty_label, 0, 10, 6, 2)
        buttons_classes_glayout.addWidget(self.analyze_button, 2, 12, 4, 3)
        buttons_classes_glayout.addWidget(self.stop_process_button, 2, 15, 4, 3)
        buttons_classes_glayout.addWidget(self.empty_label, 0, 18, 6, 2)

        
        ##################################

        self.common.right_down_field(self)

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

        self.common.menu_bar(self)


        self.retranslate_id_ui()
        ##QtCore.QMetaObject.connectSlotsByName(MainWindow)####BU SATIR NE İŞE YARIYOR !!!!

    def retranslate_id_ui(self):

        item = self.info_table_label.horizontalHeaderItem(0)
        item.setText("Resmin Yolu")
        item = self.info_table_label.horizontalHeaderItem(1)
        item.setText("Sınıflar")
        item = self.info_table_label.horizontalHeaderItem(2)
        item.setText("Sonuç")

        #iconlar ve resimler tanıtıldı
        logo_path = "icons/forencrypt.jpg"
        image = self.process_image
        self.add_image(image_path=logo_path, image_label=image)

        logo_path = "icons/forencrypt-out.jpg"
        image = self.output_image
        self.add_image(image_path=logo_path, image_label=image)
        #------
        
        self.cocodataset_button.clicked.connect(self.coco_button_clicked)
        self.forencrypt_model_button.clicked.connect(self.forencrypt_button_clicked)

        self.input_file_tree.doubleClicked.connect(self.input_tree_clicked)

        self.input_folder_bar.triggered.connect(self.input_folder_bar_click)
        
       #Analiz butonunun fonksyiona bağlanması 
        self.analyze_button.clicked.connect(self.image_detection_analyze_button_clicked)
       #------------

       #Durdur butonu başta tıklanabilir olmayacak
        self.stop_process_button.clicked.connect(self.stop_button_clicked)
        self.stop_process_button.setEnabled(False)
       #-----
        

  
    def setup_vfd_ui(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(self.screen_width, self.screen_height)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        cssFile ="main.css"
        with open(cssFile,"r") as fh:
                MainWindow.setStyleSheet(fh.read())

        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        #########################

        self.common = common_features_ui(self)

        ##########################

        self.common.left_field(self)
        self.input_file_text.setText("Lütfen Video Seçiniz")
        ##########################

        self.common.image_field(self)
        
        ##################################

        self.common.right_down_field(self)

        self.remaining_process_label.setText("İşlenen frame / Toplam frame")

        ##########################

        self.choose_class_label = QtWidgets.QLabel()
        self.choose_class_label.setWordWrap(True)
        self.choose_class_label.setAlignment(QtCore.Qt.AlignLeft)
        self.choose_class_label.setObjectName("choose_class_label")


        self.forencrypt_model_button = QtWidgets.QPushButton("Yaygın Suç Nesneleri")
        self.forencrypt_model_button.setObjectName("forencrypt_model_button")
        button_icon = QtGui.QPixmap("icons/for-logo.png");
        self.forencrypt_model_button.setIcon(QtGui.QIcon(button_icon))

        self.cocodataset_button = QtWidgets.QPushButton("Nesne Listesi")
        self.cocodataset_button.setObjectName("cocodataset_button")
        button_icon = QtGui.QPixmap("icons/coco-logo.png");
        self.cocodataset_button.setIcon(QtGui.QIcon(button_icon))
        
        
        self.analyze_button = QtWidgets.QPushButton("Analiz Et")
        self.analyze_button.setObjectName("analyze_button")
        self.analyze_button.setMinimumWidth(50)
        self.analyze_button.setMinimumHeight(40)

        self.stop_process_button = QtWidgets.QPushButton("Durdur")
        self.stop_process_button.setObjectName("stop_process_button")
        self.stop_process_button.setMinimumWidth(50)
        self.stop_process_button.setMinimumHeight(40)

        self.fps_label = QtWidgets.QLabel("FPS:")
        self.fps_label.setObjectName("fps_label")
        self.fps_label.setAlignment(QtCore.Qt.AlignRight)

        self.frame_combobox = QtWidgets.QComboBox(self)
        self.frame_combobox.addItem("1")
        self.frame_combobox.addItem("2")
        self.frame_combobox.addItem("4")
        self.frame_combobox.addItem("5")
        self.frame_combobox.addItem("10")
        self.frame_combobox.setObjectName("frame_combobox")

        buttons_classes_glayout = QtWidgets.QGridLayout()
        buttons_classes_glayout.addWidget(self.choose_class_label, 0 , 0 , 3, 10)
        buttons_classes_glayout.addWidget(self.forencrypt_model_button, 3, 0 , 2, 5)
        buttons_classes_glayout.addWidget(self.cocodataset_button, 3, 5 , 2, 2)
        buttons_classes_glayout.addWidget(self.fps_label, 3, 7 , 2, 1)
        buttons_classes_glayout.addWidget(self.frame_combobox, 3, 8 , 2, 2)
        buttons_classes_glayout.addWidget(self.empty_label, 0, 10, 6, 2)
        buttons_classes_glayout.addWidget(self.analyze_button, 2, 12, 4, 3)
        buttons_classes_glayout.addWidget(self.stop_process_button, 2, 15, 4, 3)
        buttons_classes_glayout.addWidget(self.empty_label, 0, 18, 6, 2)

        ##################################
        
        all_screen_glayout = QtWidgets.QGridLayout()
        all_screen_glayout.setSpacing(5)
        all_screen_glayout.setColumnStretch(0, 1)
        all_screen_glayout.setColumnStretch(1, 6)

        all_screen_glayout.addLayout(self.file_choose_vlayout, 0, 0, 7, 1)
        all_screen_glayout.addLayout(self.image_glayout, 0, 1, 3, 2)
        all_screen_glayout.addLayout(buttons_classes_glayout, 3, 1, 1, 2)
        all_screen_glayout.addLayout(self.timer_table_glayout, 4, 1 ,3 ,1)

        self.centralwidget.setLayout(all_screen_glayout)


        MainWindow.setCentralWidget(self.centralwidget)

        #################

        self.common.menu_bar(self)

        self.input_folder_bar.setText("Girdi Videosu")

        ##################


        self.retranslate_vfd_ui()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslate_vfd_ui(self):
        item = self.info_table_label.horizontalHeaderItem(0)
        item.setText("Resmin Yolu")
        item = self.info_table_label.horizontalHeaderItem(1)
        item.setText("Sınıflar")
        item = self.info_table_label.horizontalHeaderItem(2)
        item.setText("Sonuç")

        #iconlar ve resimler tanıtıldı
        logo_path = "icons/forencrypt.jpg"
        image = self.process_image
        self.add_image(image_path=logo_path, image_label=image)

        logo_path = "icons/forencrypt-out.jpg"
        image = self.output_image
        self.add_image(image_path=logo_path, image_label=image)
        #------

        self.cocodataset_button.clicked.connect(self.coco_button_clicked)
        self.forencrypt_model_button.clicked.connect(self.forencrypt_button_clicked)


       #Analiz butonunun fonksyiona bağlanması 
        self.analyze_button.clicked.connect(self.video_frame_analyze_button_clicked)
       #------------
       
        self.input_file_tree.doubleClicked.connect(self.input_tree_clicked_video)


        self.input_folder_bar.triggered.connect(self.input_video_bar_click)

       #Durdur butonu başta tıklanabilir olmayacak
        self.stop_process_button.clicked.connect(self.stop_button_clicked)
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


    ##Girdi klaösrünün seçildiği fonksyion
    def input_tree_clicked(self, index):
        try:
            if os.path.isdir(self.common.model.filePath(index)):
                self.input_path_label.setText(self.common.model.filePath(index))
            else: 
                self.input_path_label.setText("Lütfen Klasör Seçiniz")
        except:
            pass
   ##---------


   ##Girdi videosunun seçildiği fonksyion
    def input_tree_clicked_video(self, index):
        try:
            if os.path.isfile(self.common.model.filePath(index)):
                self.input_path_label.setText(self.common.model.filePath(index))
            else: 
                self.input_path_label.setText("Lütfen Video Seçiniz")
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
            if os.path.isdir(self.common.model.filePath(index)):
                self.output_path_label.setText(self.common.model.filePath(index))
            else: 
                self.output_path_label.setText(1, "Lütfen Klasör Seçiniz")
        except:
            pass
   ##----------


    def input_video_bar_click(self):
        file_filter = 'Video Dosyası (*.mp4)'
        response = QtWidgets.QFileDialog.getOpenFileName(
            parent=self,
            caption='Video Dosyası Seçiniz',
            directory=os.getcwd(),
            filter=file_filter,
            initialFilter='Video Dosyası (*.mp4)'
        )
        if str(response)  != "":
            self.input_path_label.setText(str(response[0]))
        else:
            self.input_path_label.setText("Lütfen Video Seçiniz")

