import sys
import matplotlib
import os
matplotlib.use("Qt5Agg")
if hasattr(sys, 'frozen'):
    os.environ['PATH'] = sys._MEIPASS + ";" + os.environ['PATH']
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QSizePolicy, QWidget,QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import *
from mpl_toolkits.mplot3d import Axes3D
# sns.set_style("whitegrid")

# sns.set_style("darkgrid", {"axes.facecolor": "0"})



class Mydemo(FigureCanvas):
    def __init__(self, parent=None, width=10, height=10, dpi=100):

        plt.rcParams['font.family'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        # self.fig = Figure()
        self.axes = self.fig.add_subplot(1, 1, 1)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


class Mydemo3D(FigureCanvas):
    def __init__(self, parent=None, width=10, height=10, dpi=100):

        plt.rcParams['font.family'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.gca(projection='3d')
        # self.ax3d.plot_surface(self.X, self.Y, self.Z, cmap='rainbow')
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)