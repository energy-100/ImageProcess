# -*- coding:utf-8 -*-

from PIL import Image


def join(png1, png2, path,flag='horizontal'):
    """
    :param png1: path
    :param png2: path
    :param flag: horizontal or vertical
    :return:
    """
    img1 = png1
    img2 = png2
    size1, size2 = img1.size, img2.size
    if flag == 'horizontal':
        joint = Image.new('RGB', (size1[0]+size2[0], size1[1]))
        loc1, loc2 = (0, 0), (size1[0], 0)
        joint.paste(img1, loc1)
        joint.paste(img2, loc2)
        joint.save(path)
    elif flag == 'vertical':
        joint = Image.new('RGB', (size1[0], size1[1]+size2[1]))
        loc1, loc2 = (0, 0), (0, size1[1])
        joint.paste(img1, loc1)
        joint.paste(img2, loc2)
        joint.save(path)


# if __name__ == '__main__':
    # png = 'lena.png'
    # join(png, png)
    # join(png, png, flag='vertical')
