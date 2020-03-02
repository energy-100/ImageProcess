
import numpy as np

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

def countPositionV(x1, y1, x2, y2,data,wide,len):
    print("len:",len)
    print("countelem", x1, y1, x2, y2)
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

    #整合每组点的数据
    return countline(listx, listy,data)

def countline(x, y,data):
    linelist = []
    for i in range(len(x)):
        sum = 0
        for j in range(len(x[0])):
            sum = sum + data[y[i][j], x[i][j]]
            # print(data[y[i][j], x[i][j]])
        linelist.append(sum / len(x[0]))
    # print()
    return linelist
    # plt.plot(linelist)
    # plt.show()