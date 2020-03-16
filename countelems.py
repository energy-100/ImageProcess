
import numpy as np

# 计算所选直线及其邻域上的坐标
def countPosition(x1, y1, x2, y2,data,wide):
    # wide = 0
    print("countelem", x1, y1, x2, y2)
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
    for k in range(maxstep):
        xtemp = []
        ytemp = []
        x = x + xUnitstep
        y = y + yUnitstep

        # 添加中心点
        xtemp.append(round(x))
        ytemp.append(round(y))
        xup = x
        yup = y
        xlow = x
        ylow = y
        for j in range(wide):
            # 添加上边点
            xup = xup + yUnitstep
            yup = yup - xUnitstep
            xtemp.append(round(xup))
            ytemp.append(round(yup))
            # 添加下边点
            xlow = xlow - yUnitstep
            ylow = ylow + xUnitstep
            xtemp.append(round(xlow))
            ytemp.append(round(ylow))
        listx.append(xtemp)
        listy.append(ytemp)
    listx = np.array(listx)
    listy = np.array(listy)
    # print(listx)
    # print(listy)
    # for i in range(len(listx)):
    #     # if i==0:
    #         # print(listx[i])
    #         # print(listy[i])
    #         plt.scatter(listx[i],listy[i])
    # plt.plot(listx[:,0],listy[:,0])
    # print(listx[:,0])
    # print(listy[:,0])
    # plt.show()

    #整合每组点的数据
    return countline(listx, listy,data)

# 计算垂直位置及其邻域上的坐标
def countPositionV(x1, y1, x2, y2,data,wide,len):
    # print("len:",len)
    # print("countelem", x1, y1, x2, y2)
    Vx1 = round(
        x1 + (y2 - y1) * len / ((y2 - y1) ** 2 + (x1 - x2) ** 2) ** 0.5)
    Vy1 = round(
        y1 - (x2 - x1) * len / ((y2 - y1) ** 2 + (x1 - x2) ** 2) ** 0.5)
    Vx2 = round(
        x1 - (y2 - y1) * len / ((y2 - y1) ** 2 + (x1 - x2) ** 2) ** 0.5)
    Vy2 = round(
        y1 + (x2 - x1) * len / ((y2 - y1) ** 2 + (x1 - x2) ** 2) ** 0.5)
    listx = []
    listy = []
    xDis = Vx2 - Vx1  # x的增量
    yDis = Vy2 - Vy1  # y的增量
    if (abs(xDis) > abs(yDis)):
        maxstep = abs(xDis)
    else:
        maxstep = abs(yDis)
    xUnitstep = xDis / maxstep  # x每步骤增量
    yUnitstep = yDis / maxstep  # y的每步增量
    x = Vx1
    y = Vy1
    for k in range(maxstep):
        xtemp = []
        ytemp = []

        # 添加中心点
        xtemp.append(round(x))
        ytemp.append(round(y))
        xup = x
        yup = y
        xlow = x
        ylow = y
        for j in range(wide):
            # 添加上边点
            xup = xup + yUnitstep
            yup = yup - xUnitstep
            xtemp.append(round(xup))
            ytemp.append(round(yup))
            # 添加下边点
            xlow = xlow - yUnitstep
            ylow = ylow + xUnitstep
            xtemp.append(round(xlow))
            ytemp.append(round(ylow))
        listx.append(xtemp)
        listy.append(ytemp)
        x = x + xUnitstep
        y = y + yUnitstep
    listx = np.array(listx)
    listy = np.array(listy)
    # print(listx)
    # print(listy)
    # for i in range(len(listx)):
    #     # if i==0:
    #         # print(listx[i])
    #         # print(listy[i])
    #         plt.scatter(listx[i],listy[i])
    # plt.plot(listx[:,0],listy[:,0])
    # print(listx[:,0])
    # print(listy[:,0])
    # plt.show()

    #整合每组点（邻域）的数据
    return countline(listx, listy,data)


def autoPositionV(x1, y1, x2, y2,data,wide,len):
    # print("len:",len)
    # print("countelem", x1, y1, x2, y2)
    Vx1 = round(
        x1 + (y2 - y1) * len / ((y2 - y1) ** 2 + (x1 - x2) ** 2) ** 0.5)
    Vy1 = round(
        y1 - (x2 - x1) * len / ((y2 - y1) ** 2 + (x1 - x2) ** 2) ** 0.5)
    Vx2 = round(
        x1 - (y2 - y1) * len / ((y2 - y1) ** 2 + (x1 - x2) ** 2) ** 0.5)
    Vy2 = round(
        y1 + (x2 - x1) * len / ((y2 - y1) ** 2 + (x1 - x2) ** 2) ** 0.5)
    listx = []
    listy = []
    xDis = Vx2 - Vx1  # x的增量
    yDis = Vy2 - Vy1  # y的增量
    if (abs(xDis) > abs(yDis)):
        maxstep = abs(xDis)
    else:
        maxstep = abs(yDis)
    xUnitstep = xDis / maxstep  # x每步骤增量
    yUnitstep = yDis / maxstep  # y的每步增量
    x = Vx1
    y = Vy1
    for k in range(maxstep):
        xtemp = []
        ytemp = []

        # 添加中心点
        xtemp.append(round(x))
        ytemp.append(round(y))
        xup = x
        yup = y
        xlow = x
        ylow = y
        for j in range(wide):
            # 添加上边点
            xup = xup + yUnitstep
            yup = yup - xUnitstep
            xtemp.append(round(xup))
            ytemp.append(round(yup))
            # 添加下边点
            xlow = xlow - yUnitstep
            ylow = ylow + xUnitstep
            xtemp.append(round(xlow))
            ytemp.append(round(ylow))
        listx.append(xtemp)
        listy.append(ytemp)
        x = x + xUnitstep
        y = y + yUnitstep
    listx = np.array(listx)
    listy = np.array(listy)
    # print(listx)
    # print(listy)
    # for i in range(len(listx)):
    #     # if i==0:
    #         # print(listx[i])
    #         # print(listy[i])
    #         plt.scatter(listx[i],listy[i])
    # plt.plot(listx[:,0],listy[:,0])
    # print(listx[:,0])
    # print(listy[:,0])
    # plt.show()

    #整合每组点（邻域）的数据
    return countline(listx, listy,data)

# 将邻域坐标合并
def countline(x, y,data):
    xmax=len(data[0])
    ymax=len(data)
    linelist = []
    for i in range(len(x)):
        sum = 0
        for j in range(len(x[i])):
            #防止超出图片边界
            datanum=0
            if(y[i][j]<ymax and x[i][j]<ymax):
                sum = sum + data[y[i][j], x[i][j]]
                datanum+=1
            # print(data[y[i][j], x[i][j]])
        #防止整个数组为空时，分子分母均为0，出现分母=0异常
        if(sum!=0):
            linelist.append(sum / datanum)
    # print()
    return linelist
    # plt.plot(linelist)
    # plt.show()