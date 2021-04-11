#создай тут фоторедактор Easy Editor!
from PyQt5 import*
from PyQt5.QtWidgets import*
import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import Image,ImageFilter
app = QApplication([])
main_win = QWidget()
main_win.setWindowTitle('Умные заметки')
main_win.resize(700,400)

lw_list = QListWidget()
btn_dir = QPushButton('Папка')
btn_left = QPushButton('Влево')
btn_right = QPushButton('Вправо')
btn_mirror = QPushButton('Зеркало')
btn_sharp = QPushButton('Резкость')
btn_bw = QPushButton('Ч/Б')
lb_image = QLabel('Картинка')

row = QHBoxLayout()
layout_main = QHBoxLayout()
row_tools = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()

col1.addWidget(btn_dir)
col1.addWidget(lw_list)

row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_mirror)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_bw)

col2.addWidget(lb_image)
col2.addLayout(row_tools)
row.addLayout(col1)
row.addLayout(col2)

workdir = ''
def chosendir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filenameslist():
    chosendir()
    exceptions = ['.jpg','.jpeg','.png','.bmp']
    filenames = os.listdir(workdir)
    images = filter(exceptions,filenames)
    lw_list.clear()
    lw_list.addItems(images)

def filter(exceptions,filenames):
    img = []
    for file in filenames:
        for exs in exceptions:
            if file.endswith(exs):
                img.append(file)
    return img

class ImageProcess():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "Modified/"
    
    def load_image(self,dir,filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir,filename)
        self.image = Image.open(image_path)

    def showImage(self,path):
        lb_image.hide()
        pixmapimage = QPixmap(path)
        w, h = lb_image.width(), lb_image.height()
        pixmapimage = pixmapimage.scaled(w,h,Qt.KeepAspectRatio)
        lb_image.setPixmap(pixmapimage)
        lb_image.show()

    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(workdir,self.save_dir,self.filename)
        self.showImage(image_path)

    def saveImage(self):
        path = os.path.join(workdir,self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path,self.filename)
        self.image.save(image_path)
    
    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir,self.save_dir,self.filename)
        self.showImage(image_path)
    
    def do_sharp(self):
        self.image = self.image.filter(ImageFilter.SHARPEN)
        self.saveImage()
        image_path = os.path.join(workdir,self.save_dir,self.filename)
        self.showImage(image_path)

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir,self.save_dir,self.filename)
        self.showImage(image_path)

    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir,self.save_dir,self.filename)
        self.showImage(image_path)


workimage = ImageProcess()

def showChosenImage():
    if lw_list.currentRow() >= 0:
        filename = lw_list.currentItem().text()
        workimage.load_image(workdir,filename)
        image_path = os.path.join(workdir,workimage.filename)
        workimage.showImage(image_path)

btn_dir.clicked.connect(filenameslist)
lw_list.currentRowChanged.connect(showChosenImage)
btn_bw.clicked.connect(workimage.do_bw)
btn_mirror.clicked.connect(workimage.do_flip)
btn_left.clicked.connect(workimage.do_left)
btn_right.clicked.connect(workimage.do_right)
btn_sharp.clicked.connect(workimage.do_sharp)

main_win.setLayout(row)
main_win.show()
app.exec()