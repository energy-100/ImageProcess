# coding: utf-8
import cv2
import numpy as np
import matplotlib.pyplot as plt
from myLabel import *

# img = cv2.imread("C:/Users/ENERGY/Desktop/aaaa.png")

# -*- coding: utf-8 -*-
import cv2
import os


#解决不能读取中文路径的问题

def cv_imread(path):
    # 用matplotlib的路径
    img = plt.imread(path)
    # 因为opencv读取是按照BGR的顺序，所以这里转换一下即可
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img_rgb




class imagepro:
    def __init__(self,path):
        self.colorimg=cv_imread(path) #彩色
        self.imgshow=self.colorimg.copy() #灰度
        self.img = cv2.cvtColor(self.colorimg, cv2.COLOR_BGR2GRAY)  # 转化为灰度图
        self.count = 0
        self.sx=-1
        self.sy=-1
        self.ex=-1
        self.ey=-1


    def onmouse(self,event, x, y, flags, param):   #标准鼠标交互函数
        # print(x,x,img[y, x])
        if event==cv2.EVENT_LBUTTONDOWN:      #当鼠标移动时
            if (self.count==0 or self.count==2):
                self.sx = x
                self.sy = y
                self.ex = -1
                self.ey = -1
                self.count=1
                self.imgshow=self.colorimg.copy()
            elif(self.count==1):
                self.ex = x
                self.ey = y
                self.count=2
                cv2.arrowedLine(self.imgshow, (self.sx, self.sy), (self.ex, self.ey),  (0,0,255), 2)
                self.countelem(self.sx,self.sy,self.ex,self.ey)
            cv2.imshow("test", self.imgshow)
            print(self.sx,self.sy,self.ex,self.ey,self.count)


    def countelem(self,x1,y1,x2,y2):
        wide=0
        print("countelem",x1,y1,x2,y2)
        listx=[]
        listy=[]
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
            xtemp=[]
            ytemp=[]
            x = x + xUnitstep
            y = y + yUnitstep

            #添加中心点
            xtemp.append(round(x))
            ytemp.append(round(y))
            xup = x
            yup = y
            xlow = x
            ylow = y
            for j in range(wide):
                #添加上边点
                xup = xup + yUnitstep
                yup = yup - xUnitstep
                xtemp.append(round(xup))
                ytemp.append(round(yup))
                #添加下边点
                xlow = xlow - yUnitstep
                ylow = ylow + xUnitstep
                xtemp.append(round(xlow))
                ytemp.append(round(ylow))
            listx.append(xtemp)
            listy.append(ytemp)
        listx=np.array(listx)
        listy=np.array(listy)
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
        self.countline(listx,listy)


    def countline(self,x,y):
        linelist=[]
        for i in range(len(x)):
            sum=0
            for j in range(len(x[0])):
                sum=sum+self.img[x[i][j],y[i][j]]
            linelist.append(sum/len(x[0]))
        print()
        plt.plot(linelist)
        plt.show()
    def do(self):
        cv2.namedWindow("test")          #构建窗口
        cv2.setMouseCallback("test", self.onmouse)   #回调绑定窗口
        while True:               #无限循环
            print(type(cv2.imshow("test",self.imgshow)))        #显示图像
            if cv2.waitKey() == ord('q'):break  #按下‘q'键，退出
        cv2.destroyAllWindows()         #关闭窗口


if __name__ == '__main__':          #运行
    # a=imagepro("C:/Users/ENERGY/Desktop/aaaa.png")
    a=imagepro("D:/工作文件2/李同据1118/ltj8-左侧内关注射荧光素钠22min后.png")
    a.do()