#!/usr/bin/env python
#_*_coding:utf-8_*_
#fangzhen.py

import random,os,math
import safe as sf
import waterway_ship as ws
import numpy as np
import time
#import matplotlib

#try:
#        matplotlib.use('Qt5Agg')
#except ValueError as e:
#        print('Error: matplotlib backend\n',e)
#        print('Trying:',matplotlib.get_backend())
#finally:
#        import matplotlib.pyplot as plt


#定义从文件input_data.txt读入数据的变量
input_para = open('input_data.txt')

#定义船
#输入仿真船的种类数
Shipnum = input_para.readline()
ShipNum = int(Shipnum[:len(Shipnum) - 1])
ShipType = [([0] * 4) for i in range(ShipNum)]
v = [0] * ShipNum
for i in range(0,ShipNum):
        Type = input_para.readline()
        Type = int(Type[:len(Type) - 1])             #杂货船=1，散货船=2，油船=3，集装箱船=4
        DWT = input_para.readline()
        DWT = int(DWT[:len(DWT) - 1])              #单位：t
        vel = input_para.readline()
        v[i] = int(vel[:len(vel) - 1])
        for j in range(0,4):
                ShipType[i][j] = ws.Ship_Size(i,j,Type,DWT)               #获取第i类船的船型信息

#定义元胞尺寸
#L_cell=30

#=================================开始仿真========================================
#定义空间大小和时间步
L = input_para.readline()
L = int(int(L[:len(L) - 1])/30)
a = [(['*'] * L) for i in range(L)]
Time = 60  #仿真1分钟

b = [([0] * L) for i in range(L)]                      #元胞自动机规则，整体更新建立b数组来保存t时刻的值

#选择单双向航道
fx = input_para.readline()
FX = int(fx[:len(fx) - 1])                   #选择航道是单向航道还是双向航道

if FX == 1:
        ShipNum_inbound = ShipNum
        ShipNum_outbound = 0
else:
        ShipNum_inbound = random.randint(0,ShipNum)
        ShipNum_outbound = ShipNum - ShipNum_inbound
 
L1 = input_para.readline()                  #从左往右第一横段的长度
L1 = int(int(L1[:len(L1) - 1])/30)
v0 = input_para.readline()
v0 = float(v0[:len(v0) - 1])                   #横流速

if v0 <= 0.25:
        n = 1.81
        r = 3 * np.pi/180
elif v0 > 0.25 and v0 <= 0.5:
        n = 1.69
        r = 7 * np.pi/180
elif v0 > 0.5 and v0 <= 0.75:
        n = 1.59 
        r = 10 * np.pi/180
elif v0 > 0.75:
        n = 1.45
        r = 14 * np.pi/180

A = n * (398 * np.sin(r) + 56.4)           #航迹带宽度

#由最大航速得到富裕宽度C
vn = max(v)

if vn <= 6:
        C = 56.4
else:   
        C = 84.6
#计算航道宽度
W = int( ( A + 2 * C )/30 )

#获取Z0
if vn == 4:
        Z0 = 0.31
elif vn == 6:
        Z0 = 0.48
elif vn == 8:
        Z0 = 0.62
elif vn == 10:
        Z0 = 0.9
elif vn == 12:
        Z0 = 1.3

#航道水深
Dep = int(24.5 + Z0 + 0.8 + 0.15 + 0.4 + 0.52)
 
#读取转向角fai和转弯半径R
fai = input_para.readline()
fai = int(fai[:len(fai) - 1])*np.pi/180
R = input_para.readline()
R = int(int(R[:len(R) - 1])/30)
xs = input_para.readline()         #“sancha”表示三叉形式，“z”表示之字形
xs = str(xs[:len(xs) - 1])

#船舶的类                        
class Vessel:
        def __init__(self,length,width,depth,draft,v):    #型长，型宽，型深，满载吃水，航速（kn）
                self.length = length
                self.width = width
                self.depth = depth
                self.draft = draft
                self.v = v

        def __s1__(self):
                return int(self.width/2)

        def __s2__(self):
                return int(self.length/2)        

        def dsafe1(self,k,Lf1):     #dsafe1表示该船与前船的安全距离，Lf1表示超越船前的最近船舶的长度，k表示方向，k=0表示方向向左，k=1表示方向向右
                if k == 1:
                        return round(max(3 * self.length,1.8 * Lf1))
                else:
                        return round(3 * self.length + 3 * Lf1)

        def dsafe2(self,k,Lf2):             #Lf2表示超越船前的第二近船舶的长度,dsafe2和dsafe3表示在超船完成后船和它前、后船的安全距离
                if k == 1:
                        return round(max(3 * self.length,1.8 * Lf2))
                else:
                        return round(3 * self.length + 3 * Lf2)

        def dsafe3(self,k,Lf1):
                if k == 1:
                        return round(max(3 * Lf1,1.8 * self.length))
                else:
                        return round(max(1.8 * Lf1,1.8 * self.length))
 
        def dsafe4(self,k,Lf1_0):           #Lf1_0表示位于其邻近车道的前船的长度，dsafe4和dsafe5表示船和它相邻通道的前船和后船的安全距离
                if k == 1:
                        return round(3 * self.length + 3 * Lf1_0)
                else:
                        return round(max(3 * self.length,1.8 * Lf1_0))

        def dsafe5(self,k,Lb1_0):           #Lb1_0表示位于其邻近车道的后船的长度
                if k == 1:
                        return round(max(1.8 * Lb1_0,1.8 * self.length))
                else:
                        return round(max(3 * Lb1_0,1.8 * self.length))

ves = [0] * ShipNum
k = [0] * ShipNum
for i in range(0,ShipNum_inbound):        #将inbound的船只面向对象
        ves[i] = Vessel(int(ShipType[i][0]/30),int(ShipType[i][1]/30),ShipType[i][2],ShipType[i][3],v[i])
        if FX == 1:
                k[i] = 0
        else:   
                k[i] = random.randint(0,2)                               #初始方向随机生成,k=1 or k=0
                
for i in range(ShipNum_inbound,ShipNum):    #将outbound的船只面向对象
        ves[i] = Vessel(int(ShipType[i][0]/30),int(ShipType[i][1]/30),ShipType[i][2],ShipType[i][3],v[i])
        k[i] = random.randint(0,2)  


#形成边界
if FX == 1:                                #单向航道
        if xs == 'sancha':
                x1 = L1 + (R - W/2) * np.tan(fai/2)
                x2 = L1 + (R + W/2) * np.tan(fai/2)
                for i in range(0,W):
                        for j in range(0,L):
                                a[i][j] = 0
                for i in range(W,L):
                        for j in range(int(x1),int(x2)):
                                if i > int((j - x1) * np.tan(fai) - 1 + W):
                                        a[i][j] = '*'
                                else:
                                        a[i][j] = 0
                for i in range(W,L):
                        for j in range(int(x2),L):
                                if i < int((j - x1 - W/np.tan(fai)) * np.tan(fai)) or i > int((j - x1) * np.tan(fai) + W/np.cos(fai) - W):
                                        a[i][j] = '*'
                                else:
                                        a[i][j] = 0
                
        elif xs == 'z':
                x1=L1 + (R - W/2) * np.tan(fai/2)
                x2=L1 + (R + W/2) * np.tan(fai/2)
                x3=L - L1 - (R + W/2) * np.tan(fai/2)
                x4=L - L1 - (R - W/2) * np.tan(fai/2)
                Li=int(W + (x3 - x1) * np.tan(fai))             
                for i in range(0,L):
                        for j in range(0,int(x1)):
                                if i >= W:
                                        a[i][j] = '*'
                                else:
                                        a[i][j] = 0
                for i in range(0,L):
                        for j in range(int(x4),L):
                                if i < (Li - W) or i > Li:
                                        a[i][j] = '*'
                                else:
                                        a[i][j] = 0
                for i in range(0,L):
                        for j in range(int(x1),int(x2)):
                                if i > int((j - x1) * np.tan(fai) + W):
                                        a[i][j] = '*'
                                else:
                                        a[i][j] = 0
                for i in range(0,L):
                        for j in range(int(x3),int(x4)):
                                if i <= int((j - x3)*np.tan(fai) + Li - W * (1 + np.tan(fai/2))) or i > Li:
                                        a[i][j] = '*'
                                else:
                                        a[i][j] = 0
                for i in range(0,L):
                        for j in range(int(x2),int(x3)):
                                if i < int((j - x2)*np.tan(fai)) or i > int((j - x2)*np.tan(fai) + W/np.cos(fai)):
                                        a[i][j] = '*'
                                else:
                                        a[i][j] = 0
        #创建行和列数组分别存放每艘船的位置信息。进行初始化，便于之后进行演化
        row = [0] * ShipNum
        col = [0] * ShipNum
        for m in range(1,ShipNum + 1):
                row[m - 1] = random.randint(0,L)
                pd = True
                while pd:
                        if (row[m - 1] >= 0 and row[m - 1] <= W and a[row[m - 1]][0] == 0) :
                                a[row[m - 1]][0] = m
                                col[m - 1] = 0
                                pd = False
                        elif (row[m - 1] <= ((x3 - x2) * np.tan(fai) + W) and row[m - 1] >= (x3 - x2) * np.tan(fai) and a[row[m - 1]][L-1] == 0):
                                a[row[m - 1]][L - 1] = m
                                col[m - 1] = L - 1
                                pd = False
                        else:
                                row[m - 1] = random.randint(0,L)



        f = open('oneway_waterway.txt','w')
        for i in range(0,L):
                for j in range(0,L):
                        f.write(str(a[i][j]))
                f.write('\n')
        f.close()                

