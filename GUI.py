
from datetime import datetime
from myLabel import *
from imageWindows import *
from countelems import countPosition,countPositionV
from imageMarge import join
import datetime
import numpy as np
import cv2
import math
from sonWindow import SecondWindow
from PyQt5.QtGui import QIcon
from autoWayCount import countPosition2
#解决不能读取中文路径的问题

# def cv_imread(file_path):
#
#     # # 用matplotlib的路径
#     # img = plt.imread(path)
#     # # 因为opencv读取是按照BGR的顺序，所以这里转换一下即可
#     # img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     file_path_gbk = file_path.encode('gbk')  # unicode转gbk，字符串变为字节数组
#     img_mat = cv2.imread(file_path_gbk.decode())  # 字节数组直接转字符串，不解码
#     return img_mat


class main(QMainWindow):
    OpenSonWinwowSignal = QtCore.pyqtSignal(object)
    CloseSonWinwowSignal = QtCore.pyqtSignal(object)
    ModeSignal = QtCore.pyqtSignal(int)
    def __init__(self, parent=None):
        super(main, self).__init__(parent)
        self.setWindowTitle('图像灰度值变化统计软件')
        self.setWindowIcon(QIcon('xyjk.png'))
        # self.setWindowIcon(QIcon('xyjk.png'))
        # self.setFont(QFont("Microsoft YaHei", 12))
        self.statusBar().showMessage("请选择或拖拽图片文件...")
        self.setAcceptDrops(True)
        self.drawimage=""
        self.img=""
        self.datawide=5
        self.linelen=50
        self.sx=-1
        self.sy=-1
        self.ex=-1
        self.ey=-1
        self.sxV = -1
        self.syV = -1
        self.exV = -1
        self.eyV = -1
        # 网格布局
        self.grid = QGridLayout(self)

        # LCD模块
        self.led=QLCDNumber()
        self.led.setSegmentStyle(QLCDNumber.Flat)
        self.led.setStyleSheet("background-color:silver;color:black;")
        self.grid.addWidget(self.led, 1, 7, 2, 1)

        # 显示图片
        self.lb = MyLabel("请选择图片，或将图片文件拖拽至此！")
        self.lb.setAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
        self.lb.MessageSignal.connect(self.showmessage)
        self.lb.PressedSignal.connect(self.press)
        self.lb.ReleasedSignal.connect(self.release)
        self.lb.MoveedSignal.connect(self.moved)
        self.lb.LcdSignal.connect(self.led.display)
        self.lb.FilepathSignal.connect(self.filepathdrop)
        self.lb.setAcceptDrops(True)

        # self.lb.setGeometry(QRect(400, 400, 400, 400))
        # self.lb.setFixedSize(3,3)
        self.grid.addWidget(self.lb, 0, 0, 1, 4)

        # 显示折线
        self.figure1 = Mydemo(width=3, height=3, dpi=90)
        self.grid.addWidget(self.figure1, 0, 4, 1, 4)


        # 文件路径显示框
        self.filepathline=QLineEdit()
        self.filepathline.setPlaceholderText('请点击右侧按钮选择图片→')
        self.filepathline.setReadOnly(True)
        self.grid.addWidget(self.filepathline,1,0,1,3)


        # 浏览文件按钮
        self.readfilebutton=QPushButton("选择图片文件")
        self.readfilebutton.clicked.connect(lambda:self.readfile())
        self.grid.addWidget(self.readfilebutton,1, 3, 1, 1)



        #数据宽度滑块
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)  # 最小值
        self.slider.setMaximum(10)  # 最大值
        self.slider.setSingleStep(1)  # 步长
        self.slider.setTickPosition(QSlider.TicksBelow)  # 设置刻度位置，在下方
        self.slider.setValue(5)
        self.slider.sliderMoved.connect(self.sliderMoved)
        self.grid.addWidget(self.slider, 2, 4, 1, 2)

        #数据宽度刻度标签
        self.sliderlabel=QLabel("积分宽度:"+str((self.slider.value())*2+1))
        self.sliderlabel.setAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
        self.grid.addWidget(self.sliderlabel, 1, 4, 1, 2)
        
        #数据长度滑块
        self.sliderlen = QSlider(Qt.Horizontal)
        self.sliderlen.setMinimum(1)  # 最小值
        self.sliderlen.setMaximum(100)  # 最大值
        self.sliderlen.setSingleStep(10)  # 步长
        self.sliderlen.setTickPosition(QSlider.TicksBelow)  # 设置刻度位置，在下方
        self.sliderlen.setValue(50)
        self.sliderlen.sliderMoved.connect(self.sliderlenMoved)
        self.grid.addWidget(self.sliderlen, 4, 4, 1, 2)

        #数据长度刻度标签
        self.sliderlenlabel=QLabel("像素长度:"+str((self.sliderlen.value())*2))
        self.sliderlenlabel.setAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
        self.grid.addWidget(self.sliderlenlabel, 3, 4, 1, 2)


        #图像增强滑块
        self.sliderenhanceimage = QSlider(Qt.Horizontal)
        self.sliderenhanceimage.setMinimum(1)  # 最小值
        self.sliderenhanceimage.setMaximum(20)  # 最大值
        self.sliderenhanceimage.setSingleStep(1)  # 步长
        self.sliderenhanceimage.setTickPosition(QSlider.TicksBelow)  # 设置刻度位置，在下方
        self.sliderenhanceimage.setValue(3)
        self.sliderenhanceimage.sliderMoved.connect(self.sliderenhanceimageMoved)
        self.grid.addWidget(self.sliderenhanceimage, 6, 4, 1, 2)

        #图像增强刻度标签
        self.sliderenhanceimagelabel=QLabel("增强Gamma值:"+str((self.sliderenhanceimage.value()))+"(无效)")
        self.sliderenhanceimagelabel.setAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
        self.grid.addWidget(self.sliderenhanceimagelabel, 5, 4, 1, 2)

        # 保存画图
        self.saverawimage=QPushButton("保存绘制图")
        self.saverawimage.clicked.connect(self.saverawimageclicked)
        self.grid.addWidget(self.saverawimage, 2, 0, 1, 1)

        # 保存折线图
        self.savelineimage=QPushButton("保存折线图")
        self.savelineimage.clicked.connect(self.savelineimageclicked)
        self.grid.addWidget(self.savelineimage, 2, 1, 1, 1)

        # 保存横向整合图
        self.savemargeimage=QPushButton("保存横向拼接图")
        self.savemargeimage.clicked.connect(self.savemargeimageclickedH)
        self.grid.addWidget(self.savemargeimage, 2, 2, 1, 1)

        # 保存纵向整合图
        self.savemargeimage=QPushButton("保存纵向拼接图")
        self.savemargeimage.clicked.connect(self.savemargeimageclickedV)
        self.grid.addWidget(self.savemargeimage, 2, 3, 1, 1)

        #显示3D图复选框
        self.threeDcb = QCheckBox('显示3D图')
        # self.threeDcb.stateChanged.connect(self.threeDcbchannged)
        # self.grid.addWidget(self.threeDcb, 4, 2, 1, 1)

        #模式单选框
        self.showpicturebox = QGroupBox('原图显示模式')
        self.showpictureboxGrid = QGridLayout()
        self.showpicture1RadioButton = QRadioButton("原图")
        self.showpicture2RadioButton = QRadioButton("灰度图")
        self.showpicture3RadioButton = QRadioButton("增强图")
        self.showpictureboxGrid.addWidget(self.showpicture1RadioButton,0,0,1,1)
        self.showpictureboxGrid.addWidget(self.showpicture2RadioButton,0,1,1,1)
        self.showpictureboxGrid.addWidget(self.showpicture3RadioButton,0,2,1,1)
        self.showpictureButtonGroup = QButtonGroup()
        self.showpictureButtonGroup.addButton(self.showpicture1RadioButton)
        self.showpictureButtonGroup.addButton(self.showpicture2RadioButton)
        self.showpictureButtonGroup.addButton(self.showpicture3RadioButton)
        self.showpictureButtonGroup.setId(self.showpicture1RadioButton, 1)  # 设定ID
        self.showpictureButtonGroup.setId(self.showpicture2RadioButton, 2)  # 设定ID
        self.showpictureButtonGroup.setId(self.showpicture3RadioButton, 3)  # 设定ID
        self.showpicture2RadioButton.setChecked(True)
        self.showpictureButtonGroup.buttonClicked[int].connect(self.showpicture)
        self.showpicturebox.setLayout(self.showpictureboxGrid)
        self.grid.addWidget(self.showpicturebox,3,0,2,4)

        # 模式单选框
        self.modebox = QGroupBox('模式选择')
        self.modeboxGrid = QGridLayout()
        # self.modebox.addStretch(1)
        self.mode1RadioButton = QRadioButton("直线计算")
        self.mode2RadioButton = QRadioButton("垂直计算")
        self.mode3RadioButton = QRadioButton("路径识别")
        self.modeboxGrid.addWidget(self.mode1RadioButton, 0, 0, 1, 1)
        self.modeboxGrid.addWidget(self.mode2RadioButton, 0, 1, 1, 1)
        self.modeboxGrid.addWidget(self.mode3RadioButton, 0, 2, 1, 1)
        self.modeButtonGroup = QButtonGroup()
        self.modeButtonGroup.addButton(self.mode1RadioButton)
        self.modeButtonGroup.addButton(self.mode2RadioButton)
        self.modeButtonGroup.addButton(self.mode3RadioButton)
        self.modeButtonGroup.setId(self.mode1RadioButton, 1)  # 设定ID
        self.modeButtonGroup.setId(self.mode2RadioButton, 2)  # 设定ID
        self.modeButtonGroup.setId(self.mode3RadioButton, 3)  # 设定ID
        self.mode2RadioButton.setChecked(True)
        self.modeButtonGroup.buttonClicked[int].connect(self.modechanged)
        self.modebox.setLayout(self.modeboxGrid)
        self.grid.addWidget(self.modebox, 5, 0, 2, 4)

        # 布局配置
        self.lb.setFixedSize(350, 350)
        self.figure1.setFixedSize(350, 350)
        self.widget=QWidget()
        self.widget.setLayout(self.grid)
        self.setCentralWidget(self.widget)
        self.setFixedSize(self.minimumSize())
        print(self.widget.sizeHint())
        print(self.widget.sizeHint())
        self.move(20,10)

    def readfile(self):
        path,_ = QFileDialog.getOpenFileName(self, '请选择图片文件','','Image Files (*.jpg *.png *.jpeg)')
        self.loadimage(path)

    def press(self,x,y):
        self.statusBar().showMessage("["+str(x)+","+str(y)+"]")

    def release(self,sx,sy,ex,ey):
        if(self.img==""):
            return

        # 计算折线图数据
        self.sx = sx
        self.sy = sy
        self.ex = ex
        self.ey = ey
        # self.drawimage=image
        # self.statusBar().showMessage("[" + str(sx) + "," + str(sy) + "]->["+str(ex)+","+str(ey)+"]")
        if(self.modeButtonGroup.checkedId()==1):
            list = countPosition(sx,sy,ex,ey,self.img,self.slider.value())
        elif(self.modeButtonGroup.checkedId()==2):
            self.sxV = round(self.sx + (self.ey - self.sy) * self.sliderlen.value() / (
                        (self.ey - self.sy) ** 2 + (self.sx - self.ex) ** 2) ** 0.5)
            self.syV = round(self.sy - (self.ex - self.sx) * self.sliderlen.value() / (
                        (self.ey - self.sy) ** 2 + (self.sx - self.ex) ** 2) ** 0.5)
            self.exV = round(self.sx - (self.ey - self.sy) * self.sliderlen.value() / (
                        (self.ey - self.sy) ** 2 + (self.sx - self.ex) ** 2) ** 0.5)
            self.eyV = round(self.sy + (self.ex - self.sx) * self.sliderlen.value() / (
                        (self.ey - self.sy) ** 2 + (self.sx - self.ex) ** 2) ** 0.5)
            list = countPosition(self.sxV, self.syV, self.exV, self.eyV, self.img, self.slider.value())
            # list = countPositionV(sx, sy, ex, ey, self.img, self.slider.value(), self.sliderlen.value())
        elif(self.modeButtonGroup.checkedId()==3):

            pass

        # 绘制折线图
        if(self.modeButtonGroup.checkedId()!=3):
            self.figure1.fig.canvas.draw_idle()
            self.figure1.axes.clear()
            # self.figure1.axes.mouse_init()
            self.figure1.axes.plot(list)
            self.figure1.axes.grid()
            self.figure1.axes.set_ylabel("灰度值")
            self.figure1.axes.set_xlabel("像素数")

            # 垂直统计折线图标题
            if(self.modeButtonGroup.checkedId()==2):
                self.figure1.axes.set_title(
                    "[" + str(self.sxV) + "," + str(self.syV) + "]->[" + str(self.exV) + "," + str(self.eyV) + "] 像素数:" + str(
                        len(list)) + "宽度:" + str(self.datawide * 2 + 1))
            # 其他统计折线图标题
            else:
                self.figure1.axes.set_title("["+str(self.sx)+","+str(self.sy)+"]->["+str(self.ex)+","+str(self.ey)+"] 像素数:"+str(len(list))+"宽度:"+str(self.datawide*2+1))
            # self.figure1.axes.set_title("文件名:"+self.filename+"["+str(sx)+","+str(sy)+"]->["+str(ex)+","+str(ey)+"] 总点数:"+str(len(list))+"积分宽度(单边):"+str(self.width))

    def moved(self,sx,sy,ex,ey):
        self.statusBar().showMessage("[" + str(sx) + "," + str(sy) + "]->[" + str(ex) + "," + str(ey) + "]")
        pass



    def modechanged(self,id):
        self.lb.modechanged(id)
        if(id==2):
            self.sliderlenlabel.setText("积分长度:"+str(self.sliderlen.value()))
            self.sliderlen.setEnabled(True)
        else:
            self.sliderlenlabel.setText("积分长度无效")
            self.sliderlen.setEnabled(False)

    # 宽度滑块滑动函数
    def sliderMoved(self,index):
        self.sliderlabel.setText("积分宽度:"+str(index*2+1))
        self.datawide=int(index)
        self.lb.linewide=int(index)

    # 长度滑块滑动函数
    def sliderlenMoved(self,index):
        self.sliderlenlabel.setText("像素长度:"+str(index*2))
        print("像素长度:",index,str(index*2))
        self.linelen=int(index)
        self.lb.linelen=int(index)



    # 保存原图片函数
    def saverawimageclicked(self):
        height, width, bytesPerComponent = self.colorimg.shape
        bytesPerLine = 3 * width
        QImg = QImage(self.imgshow.data, width, height, bytesPerLine, QImage.Format_RGB888)
        self.temppixmap = QPixmap.fromImage(QImg)
        painter = QPainter(self.temppixmap)

        if (self.modeButtonGroup.checkedId() == 1):
            painter.setPen(QPen(Qt.red, self.datawide * 2 + 1, Qt.SolidLine, Qt.FlatCap))
            painter.setFont(QtGui.QFont("Roman times", 15))
            painter.setOpacity(0.5)
            painter.drawLine(self.sx, self.sy, self.ex, self.ey)
            painter.drawText(self.sx, self.sy, "[" + str(self.sx) + "," + str(self.sy) + "]")
            painter.drawText(self.ex, self.ey, "[" + str(self.ex) + "," + str(self.ey) + "]")
        elif (self.modeButtonGroup.checkedId() == 2):
            painter.setPen(QPen(Qt.blue, 3, Qt.DotLine))
            painter.setFont(QtGui.QFont("Roman times", 15))
            painter.drawLine(self.sx, self.sy, self.ex, self.ey)
            # painter.drawText(self.sx, self.sy, "["+str(self.sx)+","+str(self.sy)+"]")
            # painter.drawText(self.ex, self.ey, "["+str(self.ex)+","+str(self.ey)+"]")

            # 计算垂直线段起始坐标
            Vx1 = round(self.sx + (self.ey - self.sy) * self.linelen / (
                        (self.ey - self.sy) ** 2 + (self.sx - self.ex) ** 2) ** 0.5)
            Vy1 = round(self.sy - (self.ex - self.sx) * self.linelen / (
                        (self.ey - self.sy) ** 2 + (self.sx - self.ex) ** 2) ** 0.5)
            Vx2 = round(self.sx - (self.ey - self.sy) * self.linelen / (
                        (self.ey - self.sy) ** 2 + (self.sx - self.ex) ** 2) ** 0.5)
            Vy2 = round(self.sy + (self.ex - self.sx) * self.linelen / (
                        (self.ey - self.sy) ** 2 + (self.sx - self.ex) ** 2) ** 0.5)

            # 绘制垂直线段
            painter.setPen(QPen(Qt.red, self.datawide * 2 + 1, Qt.SolidLine, Qt.FlatCap))
            painter.setOpacity(0.5)
            painter.drawLine(self.sx, self.sy, Vx1, Vy1)
            painter.drawLine(self.sx, self.sy, Vx2, Vy2)
            painter.drawText(Vx1, Vy1, "[" + str(Vx1) + "," + str(Vy1) + "]")
            painter.drawText(Vx2, Vy2, "[" + str(Vx2) + "," + str(Vy2) + "]")

            # 绘制中央基准线段
            painter.setPen(QPen(Qt.red, 1, Qt.SolidLine, Qt.FlatCap))
            painter.setOpacity(1.0)
            painter.drawLine(self.sx, self.sy, Vx1, Vy1)
            painter.drawLine(self.sx, self.sy, Vx2, Vy2)
            self.Vx1 = Vx1
            self.Vx2 = Vx2
            self.Vy1 = Vy1
            self.Vy2 = Vy2

        if (self.modeButtonGroup.checkedId() == 3):
            rx, ry = countPosition2(self.sx, self.sy, self.ex, self.ey, self.img)
            painter.setPen(QPen(Qt.red, 1, Qt.SolidLine))
            painter.setFont(QtGui.QFont("Roman times", 15))
            # painter.drawLine(self.sx, self.sy, self.ex, self.ey)
            painter.drawText(self.sx, self.sy, "[" + str(self.sx) + "," + str(self.sy) + "]")
            painter.drawText(self.ex, self.ey, "[" + str(self.ex) + "," + str(self.ey) + "]")
            painter.setOpacity(0.1)
            # painter.setPen(QPen(Qt.red,self.linewide*2+1, Qt.SolidLine,Qt.FlatCap))
            painter.setPen(QPen(Qt.red, 2, Qt.SolidLine, Qt.FlatCap))
            for i in range(len(rx)):
                painter.drawPoint(round(rx[i]), round(ry[i]))
            painter.setOpacity(1.0)
            painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
            for i in range(len(rx)):
                painter.drawPoint(round(rx[i]), round(ry[i]))

            # if(self.modeButtonGroup.checkedId()==1):
        #     painter.setPen(QPen(Qt.red, self.datawide * 2, Qt.DotLine))
        #     painter.setFont(QtGui.QFont("Roman times", 15))
        #     # print(self.sx, self.sy, self.ex, self.ey)
        #     painter.drawLine(self.sx, self.sy, self.ex, self.ey)
        #     painter.drawText(self.sx, self.sy, "[" + str(self.sx) + "," + str(self.sy) + "]")
        #     painter.drawText(self.ex, self.ey, "[" + str(self.ex) + "," + str(self.ey) + "]")
        #     self.temppixmap.save(self.filedir + "/" + self.filename + "(直线数据)" + ".png")
        # elif(self.modeButtonGroup.checkedId()==2):
        #     painter.setPen(QPen(Qt.red, 3, Qt.DotLine))
        #     painter.setFont(QtGui.QFont("Roman times", 15))
        #     painter.drawLine(self.sx, self.sy, self.ex, self.ey)
        #     # painter.drawText(self.sx, self.sy, "["+str(self.sx)+","+str(self.sy)+"]")
        #     # painter.drawText(self.ex, self.ey, "["+str(self.ex)+","+str(self.ey)+"]")
        #     painter.setPen(QPen(Qt.blue, self.slider.value() * 2 + 1, Qt.DotLine))
        #     Vx1 = round(self.sx + (self.ey - self.sy) * self.sliderlen.value() / (
        #                 (self.ey - self.sy) ** 2 + (self.sx - self.ex) ** 2) ** 0.5)
        #     Vy1 = round(self.sy - (self.ex - self.sx) * self.sliderlen.value() / (
        #                 (self.ey - self.sy) ** 2 + (self.sx - self.ex) ** 2) ** 0.5)
        #     Vx2 = round(self.sx - (self.ey - self.sy) * self.sliderlen.value() / (
        #                 (self.ey - self.sy) ** 2 + (self.sx - self.ex) ** 2) ** 0.5)
        #     Vy2 = round(self.sy + (self.ex - self.sx) * self.sliderlen.value() / (
        #                 (self.ey - self.sy) ** 2 + (self.sx - self.ex) ** 2) ** 0.5)
        #     painter.drawLine(self.sx, self.sy, Vx1, Vy1)
        #     painter.drawLine(self.sx, self.sy, Vx2, Vy2)
        #     painter.drawText(Vx1, Vy1, "[" + str(Vx1) + "," + str(Vy1) + "]")
        #     painter.drawText(Vx2, Vy2, "[" + str(Vx2) + "," + str(Vy2) + "]")


        self.temppixmap.save(self.filedir + "/" + self.filename + "(垂直数据)" + ".png")
    def savelineimageclicked(self):
        self.figure1.axes.get_figure().savefig(self.filedir + "/" + self.filename + "(折线图)" + ".png")

    def savemargeimageclickedH(self):
        self.margeimage("h")

    def savemargeimageclickedV(self):
        self.margeimage("v")

    def margeimage(self,direction):
        height, width, bytesPerComponent = self.colorimg.shape
        bytesPerLine = 3 * width
        QImg = QImage(self.imgshow.data, width, height, bytesPerLine, QImage.Format_RGB888)
        self.temppixmap = QPixmap.fromImage(QImg)
        painter = QPainter(self.temppixmap)

        if (self.modeButtonGroup.checkedId() == 1):
            painter.setPen(QPen(Qt.red, self.datawide * 2 + 1, Qt.SolidLine, Qt.FlatCap))
            painter.setFont(QtGui.QFont("Roman times", 15))
            painter.setOpacity(0.5)
            painter.drawLine(self.sx, self.sy, self.ex, self.ey)
            painter.drawText(self.sx, self.sy, "[" + str(self.sx) + "," + str(self.sy) + "]")
            painter.drawText(self.ex, self.ey, "[" + str(self.ex) + "," + str(self.ey) + "]")
        elif (self.modeButtonGroup.checkedId() == 2):
            painter.setPen(QPen(Qt.blue, 3, Qt.DotLine))
            painter.setFont(QtGui.QFont("Roman times", 15))
            painter.drawLine(self.sx, self.sy, self.ex, self.ey)
            # painter.drawText(self.sx, self.sy, "["+str(self.sx)+","+str(self.sy)+"]")
            # painter.drawText(self.ex, self.ey, "["+str(self.ex)+","+str(self.ey)+"]")

            # 计算垂直线段起始坐标
            Vx1 = round(self.sx + (self.ey - self.sy) * self.linelen / (
                        (self.ey - self.sy) ** 2 + (self.sx - self.ex) ** 2) ** 0.5)
            Vy1 = round(self.sy - (self.ex - self.sx) * self.linelen / (
                        (self.ey - self.sy) ** 2 + (self.sx - self.ex) ** 2) ** 0.5)
            Vx2 = round(self.sx - (self.ey - self.sy) * self.linelen / (
                        (self.ey - self.sy) ** 2 + (self.sx - self.ex) ** 2) ** 0.5)
            Vy2 = round(self.sy + (self.ex - self.sx) * self.linelen / (
                        (self.ey - self.sy) ** 2 + (self.sx - self.ex) ** 2) ** 0.5)

            # 绘制垂直线段
            painter.setPen(QPen(Qt.red, self.datawide * 2 + 1, Qt.SolidLine, Qt.FlatCap))
            painter.setOpacity(0.5)
            painter.drawLine(self.sx, self.sy, Vx1, Vy1)
            painter.drawLine(self.sx, self.sy, Vx2, Vy2)
            painter.drawText(Vx1, Vy1, "[" + str(Vx1) + "," + str(Vy1) + "]")
            painter.drawText(Vx2, Vy2, "[" + str(Vx2) + "," + str(Vy2) + "]")

            # 绘制中央基准线段
            painter.setPen(QPen(Qt.red, 1, Qt.SolidLine, Qt.FlatCap))
            painter.setOpacity(1.0)
            painter.drawLine(self.sx, self.sy, Vx1, Vy1)
            painter.drawLine(self.sx, self.sy, Vx2, Vy2)
            self.Vx1 = Vx1
            self.Vx2 = Vx2
            self.Vy1 = Vy1
            self.Vy2 = Vy2

        if (self.modeButtonGroup.checkedId() == 3):
            rx, ry = countPosition2(self.sx, self.sy, self.ex, self.ey, self.img)
            painter.setPen(QPen(Qt.red, 1, Qt.SolidLine))
            painter.setFont(QtGui.QFont("Roman times", 15))
            # painter.drawLine(self.sx, self.sy, self.ex, self.ey)
            painter.drawText(self.sx, self.sy, "[" + str(self.sx) + "," + str(self.sy) + "]")
            painter.drawText(self.ex, self.ey, "[" + str(self.ex) + "," + str(self.ey) + "]")
            painter.setOpacity(0.1)
            # painter.setPen(QPen(Qt.red,self.linewide*2+1, Qt.SolidLine,Qt.FlatCap))
            painter.setPen(QPen(Qt.red, 2, Qt.SolidLine, Qt.FlatCap))
            for i in range(len(rx)):
                painter.drawPoint(round(rx[i]), round(ry[i]))
            painter.setOpacity(1.0)
            painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
            for i in range(len(rx)):
                painter.drawPoint(round(rx[i]), round(ry[i]))

        # if (self.modeButtonGroup.checkedId() == 1):
        #     painter.setPen(QPen(Qt.red, self.datawide * 2, Qt.DotLine))
        #     painter.setFont(QtGui.QFont("Roman times", 15))
        #     # print(self.sx, self.sy, self.ex, self.ey)
        #     painter.drawLine(self.sx, self.sy, self.ex, self.ey)
        #     painter.drawText(self.sx, self.sy, "[" + str(self.sx) + "," + str(self.sy) + "]")
        #     painter.drawText(self.ex, self.ey, "[" + str(self.ex) + "," + str(self.ey) + "]")
        # elif (self.modeButtonGroup.checkedId() == 2):
        #     painter.setPen(QPen(Qt.red, 3, Qt.DotLine))
        #     painter.setFont(QtGui.QFont("Roman times", 15))
        #     painter.drawLine(self.sx, self.sy, self.ex, self.ey)
        #     # painter.drawText(self.sx, self.sy, "["+str(self.sx)+","+str(self.sy)+"]")
        #     # painter.drawText(self.ex, self.ey, "["+str(self.ex)+","+str(self.ey)+"]")
        #     painter.setPen(QPen(Qt.blue, self.slider.value() * 2 + 1, Qt.DotLine))
        #     Vx1 = round(self.sx + (self.ey - self.sy) * self.sliderlen.value() / (
        #             (self.ey - self.sy) ** 2 + (self.sx - self.ex) ** 2) ** 0.5)
        #     Vy1 = round(self.sy - (self.ex - self.sx) * self.sliderlen.value() / (
        #             (self.ey - self.sy) ** 2 + (self.sx - self.ex) ** 2) ** 0.5)
        #     Vx2 = round(self.sx - (self.ey - self.sy) * self.sliderlen.value() / (
        #             (self.ey - self.sy) ** 2 + (self.sx - self.ex) ** 2) ** 0.5)
        #     Vy2 = round(self.sy + (self.ex - self.sx) * self.sliderlen.value() / (
        #             (self.ey - self.sy) ** 2 + (self.sx - self.ex) ** 2) ** 0.5)
        #     painter.drawLine(self.sx, self.sy, Vx1, Vy1)
        #     painter.drawLine(self.sx, self.sy, Vx2, Vy2)
        #     painter.drawText(Vx1, Vy1, "[" + str(Vx1) + "," + str(Vy1) + "]")
        #     painter.drawText(Vx2, Vy2, "[" + str(Vx2) + "," + str(Vy2) + "]")
        buf = self.figure1.fig.canvas.print_to_buffer()
        res_x, res_y = buf[1]
        img = QImage(buf[0], res_x, res_y, QImage.Format_RGBA8888)
        if direction=="h":
            margefilename = self.filedir + "/" + self.filename + "(横向整合图)" + ".png"
        elif direction=="v":
            margefilename =self.filedir + "/" + self.filename + "(纵向整合图)" + ".png"
        join(self.temppixmap.toImage(), img, margefilename, flag=direction)
    def showmessage(self,str):
        self.statusBar().showMessage(str)

    def filepathdrop(self,path):
        self.loadimage(path)

    def loadimage(self,path):
        print(path)
        self.filepathline.setText(path)
        self.path = path
        self.lb.linewide = self.slider.value()
        self.lb.linelen = self.sliderlen.value()
        self.lb.mode=self.modeButtonGroup.checkedId()
        filedir, allfilename = os.path.split(path)
        self.filename, self.fileextension = os.path.splitext(allfilename)
        self.filedir = filedir
        # cv2.imdecode(np.fromfile(path, dtype=np.uint8), -1)
        self.colorimg = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)
        self.imgshow = cv2.cvtColor(self.colorimg, cv2.COLOR_BGR2RGB)#彩色
        self.img = cv2.cvtColor(self.colorimg, cv2.COLOR_BGR2GRAY)#灰度
        self.lb.img = self.img
        self.showpicture(self.showpictureButtonGroup.checkedId())

        # # self.colorimg = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.COLOR_BGR2GRAY)#原始语句
        # # self.colorimg=cv_imread(path) #彩色
        # # self.imgshow = self.colorimg.copy()  # 彩色
        # # self.img = self.colorimg
        # # self.img = cv2.cvtColor(self.colorimg, cv2.IMREAD_GRAYSCALE)  # 转化为灰度图
        # self.lb.img=self.img
        # # height, width, bytesPerComponent = self.colorimg.shape
        # height, width = self.img.shape
        # # bytesPerLine =  width
        # # bytesPerLine = bytesPerComponent * width
        # # QImg = QImage(self.img.data, width, height, bytesPerLine, QImage.Format_RGB888)
        # # QImg = QImage(self.img.data, width, height, bytesPerLine, QImage.Format_RGB888)
        # QImg = QImage(self.img.data, width, height, QImage.Format_Indexed8)
        # pixmap = QPixmap.fromImage(QImg)
        # self.lb.setFixedSize(width, height)
        # self.figure1.setFixedSize(width,width)
        #
        # # self.lb.setMaximumSize(height,width)
        # self.lb.setPixmap(pixmap)
        # self.lb.setCursor(Qt.CrossCursor)
        # # print("********1",self.widget.minimumSize())
        # # print("********1",self.minimumSize())
        # # print("********1",self.grid.minimumSize())
        # self.setFixedSize(self.minimumSize())
        # # print()self.widget.sizeHint()
        # # self.setFixedSize(self.widget.sizeHint())
        # # self.figure2.setFixedSize(width,height)
        # # if(self.threeDcb.isChecked()==True):
        #     # self.load3Dimage(self.img)
        self.statusBar().showMessage("已加载图片：" + self.filename)


    def threeDcbchannged(self,state):
        if state == Qt.Checked:
            if(self.img!=""):
                self.OpenSonWinwowSignal.emit(self.img)
                # self.load3Dwindow()
                # self.load3Dimage(self.img)
        else:
            self.CloseSonWinwowSignal.emit(self.img)
            # self.grid.removeWidget(self.figure2)
            # sip.delete(self.figure2)
            # print("大小：")
            # print(self.widget.sizeHint())
            # print(self.widget.sizeHint())
            # self.setFixedSize(self.widget.sizeHint())

    #加载3D窗体
    def load3Dwindow(self):
        starttime = datetime.datetime.now()
        self.figure2 = Mydemo3D(width=5, height=4, dpi=100)
        self.figure2.setFixedSize(700, 700)
        self.grid.addWidget(self.figure2, 0, 7, 6, 2)
        endtime = datetime.datetime.now()
        print('加载3d窗体 The time cost: ', str(endtime - starttime))

    # 加载3D图像
    def load3Dimage(self, img):
        starttime = datetime.datetime.now()
        # self.figure2.setFixedSize(width,height)
        width, height = self.figure1.get_width_height()
        self.figure2.setFixedSize(width * 2, height * 2)
        self.figure2.fig.canvas.draw_idle()
        self.figure2.axes.clear()
        self.figure2.axes.mouse_init()
        X = range(1, len(img) + 1)
        Y = range(1, len(img[0]) + 1)
        X, Y = np.meshgrid(Y, X)
        print("长度：", X.shape, Y.shape, np.array(img).shape)
        endtime0 = datetime.datetime.now()
        self.figure2.axes.plot_surface(X, Y, np.array(img), rstride=1, cstride=1, cmap='rainbow')
        endtime = datetime.datetime.now()
        print('加载3D图像1 The time cost: ', str(endtime0 - starttime))
        print('加载3D图像2 The time cost: ', str(endtime - starttime))


    #显示图片
    def showpicture(self,id):
        if self.img=="":
            return
        height, width, bytesPerComponent = self.imgshow.shape
        if id==1:
            #原彩图
            bytesPerLine=bytesPerComponent * width
            QImg = QImage(self.imgshow.data, width, height, bytesPerLine, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(QImg)
            self.lb.setFixedSize(width, height)
            self.figure1.setFixedSize(width, width)
            self.lb.setPixmap(pixmap)
            self.lb.setCursor(Qt.CrossCursor)
        elif id==2:
            # 灰度图
            # cv2.imshow("aaa", self.img)
            # k = cv2.waitKey(0)
            QImg = QImage(self.img.data, width, height, width, QImage.Format_Indexed8)
            pixmap = QPixmap.fromImage(QImg)
            self.lb.setFixedSize(width, height)
            self.figure1.setFixedSize(width, width)
            self.lb.setPixmap(pixmap)
            self.lb.setCursor(Qt.CrossCursor)
        elif id==3:

            self.statusBar().showMessage("增在增强图片..." + self.filename)
            #增强图
            print(type(self.img))
            wmax = self.img.max()
            print(self.img.max())
            enhanceimg =np.zeros( (len(self.img),len(self.img[0])),dtype='uint8')
            for i in range(len(self.img)):
                for j in range(len(self.img[i])):
                    enhanceimg[i,j] = math.pow(self.img[i,j] / wmax, self.sliderenhanceimage.value()) * wmax
                    # self.enhanceimg[i,j] = self.img[i,j]
            QImg = QImage(enhanceimg.data, width, height,width, QImage.Format_Indexed8)
            pixmap = QPixmap.fromImage(QImg)
            self.lb.setFixedSize(width, height)
            self.figure1.setFixedSize(width, width)
            self.lb.setPixmap(pixmap)
            self.lb.setCursor(Qt.CrossCursor)
            self.statusBar().showMessage("图片已增强！" + self.filename)

    def sliderenhanceimageMoved(self,value):

        if (self.img!="" and self.showpictureButtonGroup.checkedId()==3):
            self.sliderenhanceimagelabel.setText("增强Gamma值:" + str(self.sliderenhanceimage.value()))
            self.showpicture(3)
        else:
            self.sliderenhanceimagelabel.setText("增强Gamma值:" + str(self.sliderenhanceimage.value())+"(无效)")
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = main()
    # sonwin=SecondWindow()
    # ui.OpenSonWinwowSignal.connect(sonwin.handle_click)
    ui.show()
    sys.exit(app.exec_())
