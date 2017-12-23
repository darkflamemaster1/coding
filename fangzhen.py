#!/usr/bin/env python
#_*_coding:utf-8_*_
#fangzhen.py

import random
import os
import safe as sf
import waterway_ship as ws
import numpy as np
import math

#定义元胞尺寸
#L_cell=30

#=================================开始仿真========================================
#定义空间大小和时间步
input_para=open('input_data.txt')
L=input_para.readline()
L=int(int(L[:len(L)-1])/30)
a=[([2]*L) for i in range(L)]
T=60  #仿真1分钟

b=[([0]*L) for i in range(L)]                      #元胞自动机规则，整体更新建立b数组来保存t时刻的值

#选择单双向航道
fx=input_para.readline()
FX=int(fx[:len(fx)-1])                   #选择航道是单向航道还是双向航道
L1=input_para.readline()
L1=int(int(L1[:len(L1)-1])/30)
v=input_para.readline()
v=float(v[:len(v)-1])
if v<=0.25:
        n=1.81
        r=3*np.pi/180
elif v>0.25 and v<=0.5:
        n=1.69
        r=7*np.pi/180
elif v>0.5 and v<=0.75:
        n=1.59 
        r=10*np.pi/180
elif (v>0.75 and v<=1.0) or v>1.0:
        n=1.45
        r=14*np.pi/180

A=n*(398*np.sin(r)+56.4)           #航迹带宽度

#输入航速得到富裕宽度C
vn=input_para.readline()
vn=int(vn[:len(vn)-1])
if vn<=6:
        C=56.4
else:   
        C=84.6
#计算航道宽度
W=int((A+2*C)/30)

#获取Z0
if vn==4:
        Z0=0.31
elif vn==6:
        Z0=0.48
elif vn==8:
        Z0=0.62
elif vn==10:
        Z0=0.9
elif vn==12:
        Z0=1.3

#航道水深
Dep=int(24.5+Z0+0.8+0.15+0.4+0.52)
 
#读取转向角fai和转弯半径R
fai=input_para.readline()
fai=int(fai[:len(fai)-1])*np.pi/180
R=input_para.readline()
R=int(int(R[:len(R)-1])/30)

xs=input_para.readline()         #“sancha”表示三叉形式，“z”表示之字形
xs=str(xs[:len(xs)-1])

#形成边界
if FX==1:                                #单向航道
        if xs=='sancha':
                x1=L1+(R-W/2)*np.tan(fai/2)
                x2=L1+(R+W/2)*np.tan(fai/2)
                for i in range(0,W):
                        for j in range(0,L):
                                a[i][j]=0
                for i in range(W,L):
                        for j in range(int(x1),int(x2)):
                                if i>int((j-x1)*np.tan(fai)-1+W):
                                        a[i][j]=2
                                else:
                                        a[i][j]=0
                for i in range(W,L):
                        for j in range(int(x2),L):
                                if i<int((j-x1-W/np.tan(fai))*np.tan(fai)) or i>int((j-x1)*np.tan(fai)+W/np.cos(fai)-W):
                                        a[i][j]=2
                                else:
                                        a[i][j]=0
                
        elif xs=='z':
                x1=L1+(R-W/2)*np.tan(fai/2)
                x2=L1+(R+W/2)*np.tan(fai/2)
                x3=L-L1-(R+W/2)*np.tan(fai/2)
                x4=L-L1-(R-W/2)*np.tan(fai/2)
                Li=int(W+(x3-x1)*np.tan(fai))              
                for i in range(0,L):
                        for j in range(0,int(x1)):
                                if i>=W:
                                        a[i][j]=2
                                else:
                                        a[i][j]=0
                for i in range(0,L):
                        for j in range(int(x4),L):
                                if i<(Li-W) or i>Li:
                                        a[i][j]=2
                                else:
                                        a[i][j]=0
                for i in range(0,L):
                        for j in range(int(x1),int(x2)):
                                if i>int((j-x1)*np.tan(fai)+W-1):
                                        a[i][j]=2
                                else:
                                        a[i][j]=0
                for i in range(0,L):
                        for j in range(int(x3),int(x4)):
                                if i<=int((j-x3)*np.tan(fai)+Li-W*(1+np.tan(fai/2))) or i>Li:
                                        a[i][j]=2
                                else:
                                        a[i][j]=0
                for i in range(0,L):
                        for j in range(int(x2),int(x3)):
                                if i<int((j-x2)*np.tan(fai)) or i>int((j-x2)*np.tan(fai)+W/np.cos(fai)):
                                        a[i][j]=2
                                else:
                                        a[i][j]=0
       
                                
        f=open('oneway_waterway.txt','w')
        for i in range(0,L):
                for j in range(0,L):
                        f.write(str(a[i][j]))
                f.write('\n')
        f.close()
        

#定义船
#输入仿真船的种类数
#Shiptype=input_para.readline()
#ShipTypeNum=int(Shiptype[:len(ShipType)-1])
#ShipType=[([0]*4) for i in range(ShipTypeNum)]
#for i in range(0,ShipTypeNum):
#        Type=input_para.readline()
#        Type=int(Type[:len(Type)-1])             #杂货船=1，散货船=2，油船=3，集装箱船=4
#        DWT=input_para.readline()
#        DWT=int(DWT[:len(DWT)-1])              #单位：t
#        for j in range(0,4):
#                ShipType[i][j]=waterway_ship.Ship_Size(i,j,Type,DWT)               #获取第i类船的船型信息


#新建一个txt文件，用来存放数据
#f=open('fangzhen.txt','a')
#for i in range(0,L/30):
#    for j in range(0,L/30):
#        f.write(str(a[i][j]))
#    f.write('\n')
#文档中换行
#f.write('\n')
#f.close()

