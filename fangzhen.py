#!/usr/bin/env python
#_*_coding:utf-8_*_
#fangzhen.py

import random,os,math
import safe as sf
import waterway_ship as ws
import numpy as np

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
v = [0] * ShipNum             #设计航速
v_sjhs = [0] * ShipNum
for i in range(0,ShipNum):
        Type = input_para.readline()
        Type = int(Type[:len(Type) - 1])             #杂货船=1，散货船=2，油船=3，集装箱船=4
        DWT = input_para.readline()
        DWT = int(DWT[:len(DWT) - 1])              #单位：t
        vel = input_para.readline()
        v[i] = int(vel[:len(vel) - 1])    
        v_sjhs[i] = ws.hs(DWT)
        for j in range(0,4):
                ShipType[i][j] = ws.Ship_Size(i,j,Type,DWT)               #获取第i类船的船型信息

#定义元胞尺寸
#L_cell=30

#定义空间大小和时间步
L = input_para.readline()
L = int(int(L[:len(L) - 1])/30)
a = [(['*'] * L) for i in range(L)]
T = input_para.readline()                              #时间单位：小时
T = int(int(T[:len(T) - 1]))

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
vn = int(max(v))
if vn <= 6:
        C = 56.4
else:   
        C = 84.6
#计算航道宽度
W = int((A + 2 * C)/30)

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

ves = []
k = [0] * ShipNum
for i in range(0,ShipNum_inbound):        #将inbound的船只面向对象
        ves.append(Vessel(int(ShipType[i][0]/30),int(ShipType[i][1]/30),ShipType[i][2],ShipType[i][3],v[i]))
        if FX == 1:
                k[i] = 1
        else:   
                k[i] = random.randint(0,2)                               #初始方向随机生成,k=1 or k=0
                
for i in range(ShipNum_inbound,ShipNum):    #将outbound的船只面向对象
        ves.append(Vessel(int(ShipType[i][0]/30),int(ShipType[i][1]/30),ShipType[i][2],ShipType[i][3],v[i]))
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

        if xs == 'z':
                L_B = int((x3 - x2) * np.tan(fai) + W +(R + W/2) * np.tan(fai) * np.tan(fai))
        elif xs == 'sancha':
                L_B = int(W + (L - x1) * np.tan(fai))
        #创建行和列数组分别存放每艘船的位置信息。进行初始化，便于之后进行演化
        row = [0] * ShipNum
        col = [0] * ShipNum
        for m in range(1,ShipNum + 1):
                row[m - 1] = random.randint(0,L)
                col[m - 1] = random.randint(0,L1)
                pd = True
                while pd:
                        if (row[m - 1] >= 0 and row[m - 1] <= W and a[row[m - 1]][col[m - 1]] == 0):
                                a[row[m - 1]][col[m - 1]] = m
                                pd = False
                        else:
                                row[m - 1] = random.randint(0,L)
                                col[m - 1] = random.randint(0,L1)


        f = open('oneway_waterway.txt','w')
        for i in range(0,L):
                for j in range(0,L):
                        f.write(str(a[i][j]))
                f.write('\n')
        f.close()                

        #=============================================（单向航道）开始仿真==================================================
        for time in range(0,T):
                t = time + 1 
                for m in range(1,ShipNum + 1):
                        n = m - 1 
                        #判断前方一定范围内是否有船
                        l = ves[n].__s2__() + v[n]
                        if_have_ship = 0
                        if_out_of_waterway = 0
                        for i in range(1,l + 1):
                                if a[row[n]][col[n] + i + ves[n].__s2__()] != 0 and a[row[n]][col[n] +i + ves[n].__s2__()] != '*':
                                        if_have_ship = 1
                                        break
                             
                        #判断前方一定范围内是否超出航道
                        for i in range(1,l + 1):
                                if a[row[n]][col[n] + i + ves[n].__s2__()]  == '*':
                                        if_out_of_waterway = 1
                                        break

                        if if_have_ship == 1:   #如果前方领域范围内有船
                                #判断是否需要追越前船
                                overtaking = ws.ifovertaking(a,n,v,row,col,l,ves)
                                print(overtaking)
                                #获取前船的编号
                                foreship_Number = a[row[n]][col[n] + ves[n].__s2__() + overtaking - 1]
                                print(foreship_Number)
                                if overtaking != 0:     #如果需追越则先换道再追越
                                        if (row[n] - ves[n].__s1__() <= 0 or a[row[n] - ves[n].__s1__()][col[n]] != 0) and a[row[n] + 1 + ves[n].__s1__()][col[n] + 1] == 0:
                                                a[row[n] + 1 + ves[n].__s1__()][col[n] + 1 + v[n]] = m
                                                row[n] = row[n] + 1 + ves[n].__s1__()
                                                col[n] = col[n] + 1 + v[n]
                                        elif (a[row[n] + ves[n].__s1__()][col[n]] != 0 or row[n] + ves[n].__s1__() >= L_B) and a[row[n] - 1 - ves[n].__s1__()][col[n] + 1 + ves[n].__s2__() + v[n]] == 0:
                                                a[row[n] - 1 - ves[n].__s1__()][col[n] + 1 + v[n] + ves[n].__s2__()] = m
                                                row[n] = row[n] - 1 - ves[n].__s1__()
                                                col[n] = col[n] + 1 + v[n] + ves[n].__s2__()
                                else:                   #如果周边情况不满足追越条件，只能减速 
                                        pd = True
                                        while pd:
                                                v[n] = int((v[n] + v[foreship_Number - 1])/2-1)
                                                if a[row[n]][col[n] + v[n] + ves[n].__s2__()] == 0:
                                                        a[row[n]][col[n] + v[n] + ves[n].__s2__()] = m
                                                        col[n] = col[n] + v[n] + ves[n].__s2__()
                                                        pd = False
  
                        elif if_have_ship == 0 and if_out_of_waterway == 1:     #如果前方领域范围内没有船但是会驶出航道
                                row_ = int(v[n] * np.sin(fai))
                                col_ = int(v[n] * np.cos(fai))
                                if v[n] == 1 and a[row[n] + row_ + ves[n].__s1__()][col[n] + ves[n].__s2__() + col_] == 0:
                                        a[row[n] + row_ + ves[n].__s1__()][col[n] + ves[n].__s2__() + col_] = m
                                        row[n] = row[n] + row_ + ves[n].__s1__()
                                        col[n] = col[n] + col_ + ves[n].__s2__()
                                elif v[n] > 1:
                                        v[n] = v[n] - 1
                                        if a[row[n] + row_ + ves[n].__s1__()][col[n] + col_ + ves[n].__s2__()] == 0:
                                                a[row[n] + row_ + ves[n].__s1__()][col[n] +  ves[n].__s2__() + col_] = m
                                                row[n] = row[n] + row_ + ves[n].__s1__()
                                                col[n] = col[n] + ves[n].__s2__() + col_
                                        elif a[row[n]][col[n] + ves[n].__s2__() + v[n]] == '*':
                                                v[n] = v[n] - 1
                                                a[row[n] + ves[n].__s1__() + row_][col[n] + ves[n].__s2__() + col_] = m
                                                col[n] = col[n] + ves[n].__s2__() + col_
                                                row[n] = row[n] + ves[n].__s1__() + row_

                        elif if_have_ship ==0 and if_out_of_waterway == 0:
                                if v[n] < v_sjhs[n]:
                                        v[n] = v[n] + 1
                                a[row[n]][col[n] + v[n] + ves[n].__s2__()] = m
                                col[n] = col[n] + v[n] + ves[n].__s2__()

        fl = open('oneway_result.txt','w')
        for i in range(0,L):
                for j in range(0,L):
                        fl.write(str(a[i][j]))
                fl.write('\n')
        fl.close()
