import numpy as np
import matplotlib.pyplot as plt
import math

#计算路径
def countPosition2(x1, y1, x2, y2,data,wide=30):

    wide = 10
    # print("countelem", x1, y1, x2, y2)
    listx = []
    listy = []
    xDis = x2 - x1  # x的增量
    yDis = y2 - y1  # y的增量
    if (abs(xDis) > abs(yDis)):
        maxstep = abs(xDis)
    else:
        maxstep = abs(yDis)
    xUnitstep = xDis / maxstep  # x每步骤增量
    yUnitstep = yDis / maxstep  # y的每步增量
    x = x1
    y = y1
    xtemp = []
    ytemp = []
    wtemp = []
    for k in range(maxstep):
        x = x + xUnitstep
        y = y + yUnitstep
        # 添加中心点
        if(round(data[round(y),round(x)])>0):
            xtemp.append(round(x))
            ytemp.append(round(y))
            # print("round(x),round(y):",round(x),round(y))
            # print(data)
            wtemp.append(round(data[round(y),round(x)]))
        xup = x
        yup = y
        xlow = x
        ylow = y
        for j in range(wide):
            # 添加上边点
            xup = xup + yUnitstep
            yup = yup - xUnitstep
            if (round(data[round(yup), round(xup)]) > 0):
                xtemp.append(round(xup))
                ytemp.append(round(yup))
                wtemp.append(round(data[ round(yup),round(xup)]))
            # 添加下边点
            xlow = xlow - yUnitstep
            ylow = ylow + xUnitstep
            if (round(data[round(ylow), round(xlow)]) > 0):
                xtemp.append(round(xlow))
                ytemp.append(round(ylow))
                wtemp.append(round(data[round(ylow),round(xlow)]))
    # plt.scatter(xtemp,ytemp)
    # plt.show()

    #伽马函数图像增强
    wmax=max(wtemp)
    for i in range(len(wtemp)):
        wtemp[i]=math.pow(wtemp[i] / wmax, 5) * wmax


    if (abs(xDis) > abs(yDis)):
        print("X轴范围大:")
        z=np.polyfit(xtemp,ytemp,10,w=wtemp)
        print(z)
        poly_fit1 = np.poly1d(z)
        if(x1<x2):
            rx=range(x1,x2+1)
            ry=poly_fit1(rx)
        else:
            ry = range(x1, x2-1,-1)
            rx = poly_fit1(ry)
    else:
        print("Y轴范围大:")
        z = np.polyfit(ytemp,xtemp, 10, w=wtemp)
        print(z)
        poly_fit1 = np.poly1d(z)
        if(y1<y2):
            ry = range(y1, y2 + 1)
            rx = poly_fit1(ry)
        else:
            ry = range(y1, y2-1,-1)
            rx = poly_fit1(ry)
    # print(rx,ry)
    # plt.scatter()
    # plt.plot(rx,ry)
    # plt.show()
    # print(len(rx),len(ry))
    return rx,ry
    # return xtemp,ytemp
    # plt.savefig("C:/Users/ENERGY/Desktop/plllll.jpg")


#计算路径积分
def countway(x1,y1,x2,y2,img):

    np.polyfit







    return