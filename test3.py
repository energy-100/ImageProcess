from PyQt5.QtWidgets import QWidget, QApplication, QLabel
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QGuiApplication
import cv2
import sys
class MyLabel(QLabel):
    sx = 0
    sy = 0
    ex = 0
    ey = 0
    count=0
    flag = False
    #鼠标点击事件
    def mousePressEvent(self,event):
        self.sx = event.x
        self.sy = event.y
        self.ex = -1
        self.ey = -1
        self.flag = True

    #鼠标释放事件
    def mouseReleaseEvent(self,event):
        self.ex = event.x
        self.ey = event.y
        self.flag = False


    #鼠标移动事件
    def mouseMoveEvent(self,event):
        if self.flag:
            self.ex = event.x()
            self.ey = event.y()
            self.update()
    #绘制事件
    def paintEvent(self, event):
        super().paintEvent(event)
        rect =QRect(self.sx, self.sy, abs(self.ex-self.sx), abs(self.ey-self.sy))
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red,2,Qt.SolidLine))
        painter.drawLine(self.sx,self.sy,self.ex,self.ey)
class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.resize(675, 300)
        self.setWindowTitle('在label中绘制矩形')
        self.lb = MyLabel(self)  #重定义的label
        self.lb.setGeometry(QRect(30, 30, 511, 541))
        img = cv2.imread('C:/Users/ENERGY/Desktop/aaaa.png')
        height, width, bytesPerComponent = img.shape
        bytesPerLine = 3 * width
        cv2.cvtColor(img, cv2.COLOR_BGR2RGB, img)
        QImg = QImage(img.data, width, height, bytesPerLine,QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(QImg)
        self.lb.setPixmap(pixmap)
        self.lb.setCursor(Qt.CrossCursor)
        self.show()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    x = Example()
    sys.exit(app.exec_())
