from PIL import Image
import cv2
import numpy as np
from PyQt5.QtGui import QImage

# colorimg = cv2.imdecode(np.fromfile("D:/工作文件2/李同据1118/ltj7-左侧内关注射荧光素钠22min后.png", dtype=np.uint8), cv2.IMREAD_COLOR)
# # print(colorimg)
# # colorimg = cv2.cvtColor(colorimg, cv2.COLOR_BGR2GRAY)
# # # colorimg = cv2.cvtColor(colorimg, cv2.COLOR_BGR2GRAY)
# # cv2.imshow("aaa",colorimg)
# # k=cv2.waitKey(0)

# height, width, bytesPerComponent = colorimg.shape
# print(height, width, bytesPerComponent)
# bytesPerLine = bytesPerComponent * width
# QImg = QImage(colorimg.data, width, height, bytesPerLine, QImage.Format_RGB888)


for i in range(1):
    print(i)