# -*- coding:utf-8 -*-
import io
from PIL import Image
from PyQt5.QtGui import QImage
import numpy as np
from PyQt5.QtCore import QBuffer

def QImageToCvMat(incomingImage):
    '''  Converts a QImage into an opencv MAT format  '''

    incomingImage = incomingImage.convertToFormat(QImage.Format.Format_RGBA8888)

    width = incomingImage.width()
    height = incomingImage.height()

    ptr = incomingImage.bits()
    ptr.setsize(height * width * 4)
    arr = np.frombuffer(ptr, np.uint8).reshape((height, width, 4))
    return arr

def QImage2PILImage(img):
    buffer = QBuffer()
    buffer.open(QBuffer.ReadWrite)
    img.save(buffer, "PNG")
    pil_im = Image.open(io.BytesIO(buffer.data()))
    return pil_im

def join(png1, png2, path,flag='h'):
    """
    :param png1: path
    :param png2: path
    :param flag: horizontal or vertical
    :return:
    """

    img1 = QImage2PILImage(png1)
    img2 = QImage2PILImage(png2)
    size1, size2 = img1.size, img2.size
    if flag == 'h':
        print("**************",img1.size,img2.size)
        joint = Image.new('RGB', (size1[0]+size2[0], size1[1]))
        loc1, loc2 = (0, 0), (size1[0], 0)
        joint.paste(img1, loc1)
        joint.paste(img2, loc2)
        joint.save(path)
    elif flag == 'v':
        joint = Image.new('RGB', (size1[0], size1[1]+size2[1]))
        loc1, loc2 = (0, 0), (0, size1[1])
        joint.paste(img1, loc1)
        joint.paste(img2, loc2)
        joint.save(path)


# if __name__ == '__main__':
#     png = 'lena.png'
#     print(type(png))
#     join(png, png)
#     join(png, png, flag='vertical')
