
import numpy as np
from imageWindows import *




class SecondWindow(QWidget):
    def __init__(self, parent=None):
        super(SecondWindow, self).__init__(parent)
        self.resize(500, 500)
        self.grid = QGridLayout(self)
        self.setStyleSheet("background: black")
        self.figure=Mydemo3D(width=5, height=4, dpi=100)
        self.grid.addWidget(self.figure)
        self.setLayout(self.grid)
    def handle_click(self,img):
        if not self.isVisible():
            self.figure.fig.canvas.draw_idle()
            self.figure.axes.clear()
            self.figure.axes.mouse_init()
            X = range(1, len(img) + 1)
            Y = range(1, len(img[0]) + 1)
            X, Y = np.meshgrid(Y, X)
            print("长度：", X.shape, Y.shape, np.array(img).shape)
            self.figure.axes.plot_surface(X, Y, np.array(img), rstride=1, cstride=1, cmap='rainbow')
            self.show()

    def handle_close(self):
        self.close()