
from datetime import datetime
from myLabel import *
from imageWindows import *
from countelems import countPosition
# from imageMarge import joinf
import datetime
import numpy as np
from sonWindow import SecondWindow
#解决不能读取中文路径的问题

def cv_imread(file_path):

    # # 用matplotlib的路径
    # img = plt.imread(path)
    # # 因为opencv读取是按照BGR的顺序，所以这里转换一下即可
    # img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    file_path_gbk = file_path.encode('gbk')  # unicode转gbk，字符串变为字节数组
    img_mat = cv2.imread(file_path_gbk.decode())  # 字节数组直接转字符串，不解码
    return img_mat


class main(QMainWindow):
    OpenSonWinwowSignal = QtCore.pyqtSignal(object)
    CloseSonWinwowSignal = QtCore.pyqtSignal(object)
    def __init__(self, parent=None):
        super(main, self).__init__(parent)
        # self.setWindowIcon(QIcon('xyjk.png'))
        # self.setFont(QFont("Microsoft YaHei", 12))
        self.statusBar().showMessage("请选择图片文件...")
        self.setAcceptDrops(True)
        self.drawimage=""
        self.img=""
        self.datawide=5
        self.sx=-1
        self.sy=-1
        self.ex=-1
        self.ey=-1
        # 网格布局
        self.grid = QGridLayout(self)

        # 显示图片
        self.lb = MyLabel("请选择图片，或将图片文件拖拽至此！")
        self.lb.setAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
        self.lb.MessageSignal.connect(self.showmessage)
        self.lb.PressedSignal.connect(self.press)
        self.lb.ReleasedSignal.connect(self.release)
        self.lb.MoveedSignal.connect(self.moved)
        self.lb.FilepathSignal.connect(self.filepathdrop)
        self.lb.setAcceptDrops(True)

        # self.lb.setGeometry(QRect(400, 400, 400, 400))
        # self.lb.setFixedSize(3,3)
        self.grid.addWidget(self.lb, 0, 0, 1, 6)

        # 显示折线
        self.figure1 = Mydemo(width=10, height=5, dpi=100)
        self.grid.addWidget(self.figure1, 1, 0, 1, 6)


        # 文件路径显示框
        self.filepathline=QLineEdit()
        self.filepathline.setPlaceholderText('可拖拽数据文件至此')
        self.filepathline.setReadOnly(True)
        self.grid.addWidget(self.filepathline,2,0,1,2)


        # 浏览文件按钮
        self.readfilebutton=QPushButton("选择图片文件")
        self.readfilebutton.clicked.connect(lambda:self.readfile())
        self.grid.addWidget(self.readfilebutton,2, 2, 1, 1)



        #数据宽度滑块
        self.splider = QSlider(Qt.Horizontal)
        self.splider.setMinimum(0)  # 最小值
        self.splider.setMaximum(10)  # 最大值
        self.splider.setSingleStep(1)  # 步长
        self.splider.setTickPosition(QSlider.TicksBelow)  # 设置刻度位置，在下方
        self.splider.setValue(5)
        self.splider.sliderMoved.connect(self.sliderMoved)
        self.grid.addWidget(self.splider, 3, 3, 1, 3)

        #刻度标签
        self.spliderlabel=QLabel("积分宽度:"+str((self.splider.value())*2+1))
        self.spliderlabel.setAlignment(Qt.AlignVCenter|Qt.AlignHCenter)
        self.grid.addWidget(self.spliderlabel, 2, 3, 1, 3)

        # 保存画图
        self.saverawimage=QPushButton("保存绘制图")
        self.saverawimage.clicked.connect(self.saverawimageclicked)
        self.grid.addWidget(self.saverawimage, 3, 0, 1, 1)

        # 保存折线图
        self.savelineimage=QPushButton("保存折线图")
        self.savelineimage.clicked.connect(self.savelineimageclicked)
        self.grid.addWidget(self.savelineimage, 3, 1, 1, 1)

        # 保存整合图
        self.savemargeimage=QPushButton("保存整合图")
        self.savemargeimage.clicked.connect(self.savemargeimageclicked)
        self.grid.addWidget(self.savemargeimage, 3, 2, 1, 1)

        #显示3D图复选框
        self.threeDcb = QCheckBox('显示3D图', self)
        # self.threeDcb.stateChanged.connect(self.threeDcbchannged)
        self.grid.addWidget(self.threeDcb, 4, 0, 1, 1)


        # 布局配置
        self.lb.setFixedSize(350, 350)
        self.figure1.setFixedSize(350, 350)
        self.widget=QWidget()
        self.widget.setLayout(self.grid)
        self.setCentralWidget(self.widget)
        print(self.widget.sizeHint())
        print(self.widget.sizeHint())


    def readfile(self):
        path,_ = QFileDialog.getOpenFileName(self, '请选择图片文件','','Image Files (*.jpg *.png *.jpeg)')
        self.loadimage(path)

    def press(self,x,y):
        self.statusBar().showMessage("["+str(x)+","+str(y)+"]")

    def release(self,sx,sy,ex,ey,image):
        self.sx = sx
        self.sy = sy
        self.ex = ex
        self.ey = ey
        self.drawimage=image
        self.statusBar().showMessage("[" + str(sx) + "," + str(sy) + "]->["+str(ex)+","+str(ey)+"]")
        list=countPosition(sx,sy,ex,ey,self.img)

        self.figure1.fig.canvas.draw_idle()
        self.figure1.axes.clear()
        # self.figure1.axes.mouse_init()
        self.figure1.axes.plot(list)
        self.figure1.axes.grid()
        self.figure1.axes.set_title("["+str(sx)+","+str(sy)+"]->["+str(ex)+","+str(ey)+"] 像素数:"+str(len(list))+"宽度:"+str(self.datawide*2+1))
        # self.figure1.axes.set_title("文件名:"+self.filename+"["+str(sx)+","+str(sy)+"]->["+str(ex)+","+str(ey)+"] 总点数:"+str(len(list))+"积分宽度(单边):"+str(self.width))

    def moved(self,sx,sy,ex,ey):
        self.statusBar().showMessage("[" + str(sx) + "," + str(sy) + "]->[" + str(ex) + "," + str(ey) + "]")
        pass

    # 滑块滑动函数
    def sliderMoved(self,index):
        self.spliderlabel.setText("积分宽度:"+str(index*2+1))
        self.datawide=int(index)
        self.lb.linewide=int(index)

    # 保存原图片函数
    def saverawimageclicked(self):
        height, width, bytesPerComponent = self.colorimg.shape
        bytesPerLine = 3 * width
        QImg = QImage(self.imgshow.data, width, height, bytesPerLine, QImage.Format_RGB888)
        self.temppixmap = QPixmap.fromImage(QImg)
        painter = QPainter(self.temppixmap)
        painter.setPen(QPen(Qt.red, self.datawide * 2, Qt.DotLine))
        painter.setFont(QtGui.QFont("Roman times", 15))
        # print(self.sx, self.sy, self.ex, self.ey)
        painter.drawLine(self.sx, self.sy, self.ex, self.ey)
        painter.drawText(self.sx, self.sy, "[" + str(self.sx) + "," + str(self.sy) + "]")
        painter.drawText(self.ex, self.ey, "[" + str(self.ex) + "," + str(self.ey) + "]")
        self.temppixmap.save(self.filedir + "/" + self.filename + "(数据选择)" + ".png")

    def savelineimageclicked(self):
        self.figure1.axes.get_figure().savefig(self.filedir + "/" + self.filename + "(折线图)" + ".png")

    def savemargeimageclicked(self):
        pass
        # height, width, bytesPerComponent = self.colorimg.shape
        # bytesPerLine = 3 * width
        # QImg = QImage(self.imgshow.data, width, height, bytesPerLine, QImage.Format_RGB888)
        # self.temppixmap = QPixmap.fromImage(QImg)
        # painter = QPainter(self.temppixmap)
        # painter.setPen(QPen(Qt.red, self.datawide * 2, Qt.DotLine))
        # painter.setFont(QtGui.QFont("Roman times", 15))
        # # print(self.sx, self.sy, self.ex, self.ey)
        # painter.drawLine(self.sx, self.sy, self.ex, self.ey)
        # painter.drawText(self.sx, self.sy, "[" + str(self.sx) + "," + str(self.sy) + "]")
        # painter.drawText(self.ex, self.ey, "[" + str(self.ex) + "," + str(self.ey) + "]")
        # print(type(self.figure1.axes.get_figure()))
        # join(self.temppixmap.toImage(),QImage(self.figure1.axes),self.filedir + "/" + self.filename + "(拼接图)" + ".png")

    def showmessage(self,str):
        self.statusBar().showMessage(str)

    def filepathdrop(self,path):
        self.loadimage(path)

    def loadimage(self,path):
        print(path)
        self.filepathline.setText(path)
        self.path = path
        filedir, allfilename = os.path.split(path)
        self.filename, self.fileextension = os.path.splitext(allfilename)
        self.filedir = filedir
        self.statusBar().showMessage("已加载图片：" + self.filename)
        # cv2.imdecode(np.fromfile(path, dtype=np.uint8), -1)
        self.colorimg = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)
        # self.colorimg=cv_imread(path) #彩色
        self.imgshow = self.colorimg.copy()  # 彩色
        self.img = cv2.cvtColor(self.colorimg, cv2.COLOR_BGR2GRAY)  # 转化为灰度图
        height, width, bytesPerComponent = self.colorimg.shape
        # bytesPerLine =  width
        bytesPerLine = 3 * width
        QImg = QImage(self.imgshow.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(QImg)
        self.lb.setFixedSize(width, height)
        self.figure1.setFixedSize(width,height)

        # self.lb.setMaximumSize(height,width)
        self.lb.setPixmap(pixmap)
        self.lb.setCursor(Qt.CrossCursor)
        # self.figure2.setFixedSize(width,height)
        # if(self.threeDcb.isChecked()==True):
            # self.load3Dimage(self.img)



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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = main()
    sonwin=SecondWindow()
    ui.OpenSonWinwowSignal.connect(sonwin.handle_click)
    ui.show()
    sys.exit(app.exec_())
