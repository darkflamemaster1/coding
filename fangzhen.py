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
#L_cell=30m

#定义空间大小和时间步
L = input_para.readline()
L = int(int(L[:len(L) - 1])/10)
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
L1 = int(int(L1[:len(L1) - 1])/10)
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
W = int((A + 2 * C)/10)

#读取转向角fai和转弯半径R
fai = input_para.readline()
fai = int(fai[:len(fai) - 1])*np.pi/180
R = input_para.readline()
R = int(int(R[:len(R) - 1])/10)
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
k = []
turn = []
for i in range(0,ShipNum_inbound):        #将inbound的船只面向对象
        ves.append(Vessel(int(ShipType[i][0]/30),int(ShipType[i][1]/30),ShipType[i][2],ShipType[i][3],v[i]))
        if FX == 1:
                k.append(1)                                                 #方向为从左往右
        else:   
                k.append(random.randint(0,1))                               #初始方向随机生成,k=1 or k=0
        if xs == 'sancha':
                turn.append(random.randint(0,1))
for i in range(ShipNum_inbound,ShipNum):    #将outbound的船只面向对象
        if FX == 1:
                break
        else:     
                ves.append(Vessel(int(ShipType[i][0]/30),int(ShipType[i][1]/30),ShipType[i][2],ShipType[i][3],v[i]))
                k.append(random.randint(0,1))
                if xs == 'sancha':
                        turn.append(random.randint(0,1))  


#形成边界
if FX == 1:                                #单向航道
        if xs == 'sancha':
                x1 = L1 + (R - W/2) * np.tan(fai/2)
                x2 = L1 + (R + W/2) * np.tan(fai/2)
                x4 = L - 1
                for i in range(0,W):
                        for j in range(0,L):
                                a[i][j] = 0
                for i in range(W,L):
                        for j in range(int(x1),L):
                                if i > int((j - x1) * np.tan(fai) + W) or i < int((j - x1 - W/np.sin(fai)) * np.tan(fai) + W):
                                        a[i][j] = '*'
                                else:
                                        a[i][j] = 0
                
        elif xs == 'z':
                x1=L1 + (R - W/2) * np.tan(fai/2)
                x2=L1 + (R + W/2) * np.tan(fai/2)
                x3=L - L1 - (R + W/2) * np.tan(fai/2)
                x4=L - L1 - (R + W/2) * np.tan(fai) * (R - W)/R
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
                                if i < int((j - x2) * np.tan(fai)) or i > Li:
                                        a[i][j] = '*'
                                else:
                                        a[i][j] = 0
                for i in range(0,L):
                        for j in range(int(x2),int(x3)):
                                if i < int((j - x2) * np.tan(fai)) or i > int((j - x1) * np.tan(fai) + W):
                                        a[i][j] = '*'
                                else:
                                        a[i][j] = 0

        if xs == 'z':
                L_B = int((x3 - x1) * np.tan(fai) + W)
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
                        if (row[m - 1] - ves[m - 1].__s1__() >= 0 and row[m - 1] + ves[m - 1].__s1__() <= W and a[row[m - 1]][col[m - 1]] == 0):
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
                for m in range(1,ShipNum + 1):
                        n = m - 1
                        LY_L = int(ves[n].__s2__() + v[n])     #邻域长度
                        LY_B = int(ves[n].__s1__())            #邻域半宽度
                        f_ship = []                            #记录邻域前进范围内前船的编号　
                        col_f_ship = []                        #前船距离本船的列距离
                        row_f_ship = []                        #前船距离本船的行距离
                        free_cell_num = 0                      #空元胞个数
                        ocean = False                          #前方前进范围内距离航道边缘的距离
                        lane_change_L1 = False                 #判断是否在直道变道
                        lane_change_L2 = False                 #判断是否在斜道变道
                        out_bound = False                      #边界条件                       
                     
                        if k[n] == 1:
                                if (col[n] < x1 or col[n] > x4) and (col[n] + LY_L + v[n]) <= (L - 1):
                                        for i in range(row[n] - LY_B,row[n] + LY_B + 1):             #在邻域范围内循环查找
                                                for j in range(col[n] + LY_L,col[n] + LY_L + v[n]):
                                                        if a[i][j] != 0 and a[i][j] != '*':      #判断邻域前进的范围内是否有船只
                                                                f_ship.append(a[i][j])
                                                                col_f_ship.append(j)
                                                                if v[n] > 1:
                                                                        v[n] = v[n] - 1
                                elif (col[n] + LY_L +v[n]) > (L - 1):
                                        col[n] = L - 1
                                        out_bound = True
                                elif col[n] >= x1 and col[n] <= x4 and xs == 'z':
                                        for i in range(row[n] + int(LY_L * np.sin(fai)),row[n] + int((LY_L  + v[n]) * np.sin(fai))):
                                                for j in range(col[n] + int(LY_L * np.cos(fai)),col[n] + int((LY_L + v[n]) * np.cos(fai))):
                                                        if a[i][j] != 0 and a[i][j] != '*':
                                                                f_ship.append(a[i][j])
                                                                col_f_ship.append(j)
                                                                row_f_ship.append(i)
                                                                if v[n] > 1:
                                                                        v[n] = v[n] - 1
                                                        if a[i][j] == '*':
                                                                ocean = True
                                                                if v[n] > 1:
                                                                        v[n] = v[n] - 1
                                elif col[n] >= x1 and col[n] <= x4 and xs == 'sancha':
                                        if turn[n] == 0:
                                                for i in range(row[n] - LY_B,row[n] + LY_B + 1):
                                                        for j in range(col[n] + LY_L,col[n] + LY_L + v[n]):
                                                                if a[i][j] != 0 and a[i][j] != '*':
                                                                        f_ship.append(a[i][j])
                                                                        col_f_ship.append(j)
                                                                        if v[n] > 1:
                                                                                v[n] = v[n] - 1
                                        elif turn[n] == 1:
                                                for i in range(row[n] + int(LY_L * np.sin(fai)),row[n] + int((LY_L  + v[n]) * np.sin(fai))):
                                                        for j in range(col[n] + int(LY_L * np.cos(fai)),col[n] + int((LY_L + v[n]) * np.cos(fai))):
                                                                if a[i][j] != 0 and a[i][j] != '*':
                                                                        f_ship.append(a[i][j])
                                                                        col_f_ship.append(j)
                                                                        row_f_ship.append(i)
                                                                        if v[n] > 1:
                                                                                v[n] = v[n] - 1
                                                                if a[i][j] == '*':
                                                                        ocean = True
                                                                        if v[n] > 1:
                                                                                v[n] = v[n] - 1
                                
                                if LY_B == 0 and len(f_ship) == 0 and ocean == False:                        
                                        if v[n] < v_sjhs[n]:
                                                v[n] = v[n] + 1
                                elif LY_B > 0 and len(f_ship) == 0 and ocean == False:
                                        if v[n] < v_sjhs[n]:
                                                v[n] = v[n] + 1

                                if len(f_ship) != 0 and (col[n] < x1 or col[n] > x4):
                                        for i in range(0,len(f_ship)):
                                                if v[n] > v[f_ship[i] - 1]:
                                                        lane_change_L1 = True
                                elif len(f_ship) != 0 and (col[n] <= x4 and col[n] >= x1):
                                        for i in range(0,len(f_ship)):
                                                if v[n] > v[f_ship[i] - 1]:
                                                        lane_change_L2 = True
                                

                                while lane_change_L1 and (xs == 'z' or (xs == 'sancha' and turn[n] == 0)):
                                        row_up = int(row[n] - LY_B * 2 - 1)
                                        row_down = int(row[n] + LY_B * 2 + 1)
                                        if row_up < 0  or a[row_up][col[n] + min(col_f_ship)] != 0 or a[row[n]][col[n] + ves[n].__s2__() + v[n]] == '*':
                                                row_next_time = int(row[n] + v[n] * np.cos(45 * np.pi/180))
                                                col_next_time = int(col[n] + v[n] * np.sin(45 * np.pi/180) + ves[n].__s2__())
                                                a[row_next_time][col_next_time] = m
                                                row[n] = row_next_time
                                                col[n] = col_next_time
                                                lane_change_L1 = False
                                        elif row_down > W or a[row_down][col[n] + min(col_f_ship)] != 0 or a[row[n]][col[n] + ves[n].__s2__() + v[n]] =='*': 
                                                row_next_time = int(row[n] - v[n] * np.cos(45 * np.pi/180))
                                                col_next_time = int(col[n] + v[n] * np.sin(45 * np.pi/180)+ ves[n].__s2__())
                                                a[row_next_time][col_next_time] = m
                                                row[n] = row_next_time
                                                col[n] = col_next_time
                                                lane_change_L1 = False
                        
                                while lane_change_L2 and (xs == 'z' or (xs == 'sancha' and turn[n] == 1)):
                                        if a[row[n] + int(v[n] * np.sin(fai))][col[n]] != 0 and a[row[n]][col[n] + int(v[n] * np.cos(fai))] == 0:
                                                col_next_time = col[n] + int(v[n] * np.cos(fai))
                                                a[row[n]][col_next_time] = m
                                                col[n] = col_next_time
                                                lane_change_L2 = False
                                        elif a[row[n]][col[n] + int(v[n] * np.cos(fai))] != 0 and a[row[n] + int(v[n] * np.sin(fai))][col[n]] == 0:
                                                row_next_time = row[n] + int(v[n] * np.sin(fai))
                                                a[row_next_time][col[n]] = m
                                                row[n] = row_next_time
                                                lane_change_L2 = False
                                        else:
                                                lane_change_L2 = False
                                                        
                                if out_bound == True and (xs == 'z' or (xs == 'sancha' and turn[n] == 0)):
                                        a[row[n]][L - 1] = m
                                        col[n] = L - 1
                                elif out_bound == True and (xs == 'z' or (xs == 'sancha' and turn[n] == 1)):
                                        for i in range(0,int(v[n] * np.sin(fai) + ves[n].__s2__())):
                                                if (row[n] + i <= L_B) and a[row[n] + i][L - 1] == 0:
                                                        a[row[n] + i][L - 1] = m
                                                        row[n] = row[n] + i
                                                        col[n] = L - 1
                                                elif (row[n] + i) > L_B and a[row[n]][L - 1] == 0:
                                                        a[row[n]][L - 1] = m
                                                        col[n] = L - 1
                                else:
                                        if (col[n] < x1 or col[n] > x4) and a[row[n]][col[n] + v[n] + ves[n].__s2__()] == 0 and ocean == False:
                                                a[row[n]][col[n] + v[n] + ves[n].__s2__()] = m
                                                col[n] = col[n] + v[n] + ves[n].__s2__()
                                        elif (col[n] <= x4 and col[n] >= x1) and a[row[n] + int(LY_L * np.sin(fai))][col[n] + int(LY_L * np.cos(fai))] == 0 and ocean == False and (xs == 'z' or (xs == 'sancha' and turn[n] == 1)):
                                                row_next_time = row[n] + int(LY_L * np.sin(fai))
                                                col_next_time = col[n] + int(LY_L * np.cos(fai))
                                                a[row_next_time][col_next_time] = m
                                                row[n] = row_next_time
                                                col[n] = col_next_time
                                        elif (col[n] >= x1 and col[n] <= x4) and a[row[n]][col[n] + v[n] + ves[n].__s2__()] == 0 and ocean == False and (xs == 'sancha' and turn[n] == 0):
                                                a[row[n]][col[n] + v[n] + ves[n].__s2__()] = m
                                                col[n] = col[n] + v[n] + ves[n].__s2__()
                                        elif ocean == True:
                                                for i in range(0,int(v[n] * np.sin(fai) + ves[n].__s2__())):
                                                        for j in range(i,int(v[n] * np.cos(fai) + ves[n].__s2__())):
                                                                if a[row[n] + i][col[n] + j] == 0:
                                                                        a[row[n] + i][col[n] + j] = m
                                                                        row[n] = row[n] + i
                                                                        col[n] = col[n] + j
                        
                        #elif k[n] == 0:                              #若该船从右侧进入，左侧驶出

                        del f_ship
                        del col_f_ship
                        del row_f_ship
                        del free_cell_num
                        del ocean
                        del lane_change_L1
                        del lane_change_L2
                        del out_bound
 
        fl = open('simulation_result.txt','w')
        for i in range(0,L):
                for j in range(0,L):
                        fl.write(str(a[i][j]))
                fl.write('\n')
        fl.close()
