from PyQt5.QtWidgets import QWidget, QApplication, QLabel
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QGuiApplication
from PyQt5 import QtCore
import os
from PyQt5 import QtGui, QtWidgets
import cv2



class MyLabel(QLabel):

    sx = 0
    sy = 0
    ex = 0
    ey = 0
    Vx1=0
    Vx2=0
    Vy1=0
    Vy2=0
    count = 0
    # linewide=5
    # linelen=50
    linewide=0
    linelen=0
    mode=1
    flag = False
    PressedSignal = QtCore.pyqtSignal(int,int)
    ReleasedSignal = QtCore.pyqtSignal(int,int,int,int,object)
    MoveedSignal = QtCore.pyqtSignal(int,int,int,int)
    MessageSignal = QtCore.pyqtSignal(str)
    FilepathSignal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(MyLabel, self).__init__(parent)

    # 鼠标点击事件
    def mousePressEvent(self, event):
        self.sx = event.x()
        self.sy = event.y()
        print(self.sx)
        print(self.sy)
        self.ex = -1
        self.ey = -1
        self.flag = True
        self.PressedSignal.emit(event.x(),event.y())

    # 鼠标释放事件
    def mouseReleaseEvent(self, event):
        self.ex = event.x()
        self.ey = event.y()

        if(self.ex != self.sx or self.ey != self.sy):
            self.ReleasedSignal.emit(self.sx,self.sy,event.x(),event.y(),self.pixmap().copy())
            # self.ReleasedSignal.emit(self.sx,self.sy,event.x(),event.y(),self.pixmap().toImage())
        self.flag = False
    # 鼠标移动事件
    def mouseMoveEvent(self, event):
        if self.flag:
            self.ex = event.x()
            self.ey = event.y()
            self.update()
        if(self.mode==1):
            self.MoveedSignal.emit(self.sx,self.sy,self.ex,self.ey)
        elif(self.mode==2):
            self.MoveedSignal.emit(self.Vx1,self.Vy1,self.Vx2,self.Vy2)
    # 绘制事件
    def paintEvent(self, event):
        super().paintEvent(event)
        if (self.ex != self.sx or self.ey != self.sy):
            # rect = QRect(self.sx, self.sy, abs(self.ex - self.sx), abs(self.ey - self.sy))

            painter = QPainter(self)
            if(self.mode==1):
                painter.setPen(QPen(Qt.red, self.linewide*2+1, Qt.DotLine))
                painter.setFont(QtGui.QFont("Roman times", 15))
                painter.drawLine(self.sx, self.sy, self.ex, self.ey)
                painter.drawText(self.sx, self.sy, "[" + str(self.sx) + "," + str(self.sy) + "]")
                painter.drawText(self.ex, self.ey, "[" + str(self.ex) + "," + str(self.ey) + "]")
            elif(self.mode==2):
                painter.setPen(QPen(Qt.red, 3, Qt.DotLine))
                painter.setFont(QtGui.QFont("Roman times",15))
                painter.drawLine(self.sx, self.sy, self.ex, self.ey)
                # painter.drawText(self.sx, self.sy, "["+str(self.sx)+","+str(self.sy)+"]")
                # painter.drawText(self.ex, self.ey, "["+str(self.ex)+","+str(self.ey)+"]")
                painter.setPen(QPen(Qt.blue, self.linewide*2+1, Qt.DotLine))
                Vx1=round(self.sx+(self.ey-self.sy)*self.linelen/((self.ey-self.sy)**2+(self.sx-self.ex)**2)**0.5)
                Vy1=round(self.sy-(self.ex-self.sx)*self.linelen/((self.ey-self.sy)**2+(self.sx-self.ex)**2)**0.5)
                Vx2 = round(self.sx - (self.ey - self.sy) * self.linelen / ((self.ey - self.sy) ** 2 + (self.sx - self.ex) ** 2) ** 0.5)
                Vy2 = round(self.sy + (self.ex - self.sx) * self.linelen / ((self.ey - self.sy) ** 2 + (self.sx - self.ex) ** 2) ** 0.5)

                painter.drawLine(self.sx, self.sy, Vx1,Vy1)
                painter.drawLine(self.sx, self.sy, Vx2,Vy2)
                painter.drawText(Vx1, Vy1, "[" + str(Vx1) + "," + str(Vy1) + "]")
                painter.drawText(Vx2, Vy2, "[" + str(Vx2) + "," + str(Vy2) + "]")
                self.Vx1=Vx1
                self.Vx2=Vx2
                self.Vy1=Vy1
                self.Vy2=Vy2
            # self.pixmap2.save("C:/Users/ENERGY/Desktop/abc.png")
    def dragEnterEvent(self, evn):
        evn.accept()

    def dropEvent(self, evn):
        filename = evn.mimeData().text().split("///")[1]
        print(filename)
        if not( os.path.isdir(filename)):
            self.FilepathSignal.emit(filename)
        else:
            self.MessageSignal.emit("文件夹无效，请选择图像文件！")

    def dragMoveEvent(self, evn):
        _ ,filename = os.path.split(evn.mimeData().text().split("///")[1])
        filename , _=os.path.splitext(filename)
        self.MessageSignal.emit("正在拖入'"+filename+"'文件...")

    def modechanged(self,id):
        self.mode=id
        # print(id)