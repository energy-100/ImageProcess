from partB import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout
from PyQt5.QtCore import QTimer
import sys, time
import numpy as np

from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
import matplotlib
import matplotlib.cbook as cbook


class ImgDisp(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(ImgDisp, self).__init__(parent)
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = ImgDisp()
    ui.show()
    sys.exit(app.exec_())
