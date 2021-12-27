import  json
from PyQt5 import  QtCore, QtGui, QtWidgets

class ChecklistDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, class_json_file="json_files/coco_classes.json", name="Sınıflar"):
        super(ChecklistDialog, self).__init__(parent)
        self.json_file = class_json_file

        
        with open(self.json_file, encoding="utf-8") as f:
            
            json_content = json.loads(f.read())
        
        self.model = QtGui.QStandardItemModel()
        self.listView = QtWidgets.QListView()


        for json_object in json_content["classes"]:
            item = QtGui.QStandardItem(str(json_object["turkish"]))
            item.setCheckable(True)
            icon = QtGui.QIcon(json_object["icon"])
            item.setIcon(icon)
            check = QtCore.Qt.Checked if json_object["check"] == "True" else QtCore.Qt.Unchecked
            item.setCheckState(check)
            self.model.appendRow(item)

        self.listView.setModel(self.model)
        self.listView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.listView.clicked.connect(self.list_item_click)
        
        
        
        
        self.okButton = QtWidgets.QPushButton("Tamam")
        self.cancelButton = QtWidgets.QPushButton("İptal Et")
        self.unselectButton = QtWidgets.QPushButton("Seçililerin Hepsini Kaldır")

        all_layout = QtWidgets.QGridLayout()
        all_layout.addWidget(self.listView, 0 , 0 , 20, 12)
        all_layout.addWidget(self.okButton,20, 0, 2,  4)
        all_layout.addWidget(self.cancelButton,  20, 4, 2,  4)
        all_layout.addWidget(self.unselectButton,20, 8, 2,  4)


        
        self.setLayout(all_layout)    
        self.setWindowTitle(name)
        #self.setWindowFlags(QtCore.Qt.SubWindow)
        self.setWindowIcon(QtGui.QIcon('icons/icon.png'))

        self.okButton.clicked.connect(self.accept)
        self.cancelButton.clicked.connect(self.reject)
        self.unselectButton.clicked.connect(self.unselect)
        
    def reject(self):
        QtWidgets.QDialog.reject(self)

    def accept(self):
        self.choices = []
        i = 0
        while self.model.item(i):
            if self.model.item(i).checkState():
                self.choices.append(self.model.item(i).text())
            i += 1

        with open(self.json_file, encoding="utf-8") as f:
            json_content = json.loads(f.read())
            for json_object in json_content["classes"]:
                if any(json_object["turkish"] in s for s in self.choices):
                    json_object["check"] = "True"
                else:
                    json_object["check"] = "False"
                        

        json_file = open(self.json_file , "w+")
        json.dump(json_content, json_file) 
        json_file.close()
            
        QtWidgets.QDialog.accept(self)
        

    def unselect(self):
        i = 0
        while self.model.item(i):
            item = self.model.item(i)
            item.setCheckState(False)
            i += 1  

    def list_item_click(self, index):
        item = self.listView.selectedIndexes()[0]
        check = QtCore.Qt.Checked if item.model().itemFromIndex(index).checkState() == QtCore.Qt.Unchecked else QtCore.Qt.Unchecked
        item.model().itemFromIndex(index).setCheckState(check)


    def clean_checked(self):
        
        with open("json_files/coco_classes.json", encoding="utf-8") as f:
            json_content = json.loads(f.read())
            for json_object in json_content["classes"]:
                json_object["check"] = "False"
                    

        json_file = open("json_files/coco_classes.json", "w+")
        json.dump(json_content, json_file) 
        json_file.close()
        self.change_choose_label()

        with open("json_files/custom_classes.json", encoding="utf-8") as f:
            json_content = json.loads(f.read())
            for json_object in json_content["classes"]:
                json_object["check"] = "False"
                    

        json_file = open("json_files/custom_classes.json", "w+")
        json.dump(json_content, json_file) 
        json_file.close()
        self.change_choose_label()