def Waterway_Whole(a,b,x,y):
    Length = 0
    for i in range(0,y):
        Length += a[i]
    W_E = int(b[0])
    W_O = int(b[x - 1])
    return [int(Length),int(W_E),int(W_O)]

def W(x,input_para):
    w = []
    for i in range(0,x):
        a = input_para.readline()
        w.append(int(int(a[:len(a) - 1])/30))
    return w

def H(y,input_para):
    h = []
    for i in range(0,y):
        a = input_para.readline()
        h.append(int(int(a[:len(a) - 1])/30))
    return h

def depth_one(z,input_para):
    dep = []
    for i in range(0,z):
        a = input_para.readline()    
        dep.append(int(int(a[:len(a) - 1])/30))
    return dep

def SLM(x,a,b):
    d_slm = []                                           #建立按SLM规则转换后的分段长度数组
    for i in range(0,x):
        if i != 0 and i != (x - 1) and a[i - 1] < a[i] and a[i] < a[i + 1]:
            d_slm.append(b[i] + b[i + 1])
        elif i != 0 and i != (x - 1) and a[i - 1] > a[i] and a[i]>a[i + 1]:
            d_slm.append(b[i + 1]+b[i + 2])
        elif i != 0 and i != (x - 1) and a[i] > a[i + 1] and a[i]>a[i - 1]:
            d_slm.append(b[2 * i])
        elif i != 0 and i != (x - 1) and a[i] < a[i + 1] and a[i]<a[i - 1]:
            d_slm.append(b[i - 1] + b[i] + b[i + 1])
        elif i == 0 and a[0] < a[1]:
            d_slm.append(b[0] + b[1])
        elif i == 0 and a[0] > a[1]:
            d_slm.append(b[0])
        elif i == (x - 1) and a[i] > a[i-1]:
            d_slm.append(b[x-1])
        elif i == (x - 1) and a[i] < a[i - 1]:
            d_slm.append(b[2 * x - 2] + b[2 * x - 3])
    return d_slm



#定义船型
def Ship_Size(i,y,Type,DWT):
        if Type == 1:
                if DWT == 1000:
                        if y == 0:
                                return 85
                        elif y == 1:
                                return 12.3
                        elif y == 2:
                                return 7.0
                        elif y == 3:
                                return 4.3
                elif DWT == 2000:
                        if y == 0:
                                return 86
                        elif y == 1:
                                return 13.5
                        elif y == 2:
                                return 7.0
                        elif y == 3:
                                return 4.9
                elif DWT == 3000:
                        if y == 0:
                                return 108
                        elif y == 1:
                                return 16.0
                        elif y == 2:
                                return 7.8
                        elif y == 3:
                                return 5.9
                elif DWT == 5000:
                        if y == 0:
                                return 124
                        elif y == 1:
                                return 18.4
                        elif y == 2:
                                return 10.3
                        elif y == 3:
                                return 7.4
                elif DWT == 10000:
                        if y == 0:
                                return 146
                        elif y == 1:
                                return 22.0
                        elif y == 2:
                                return 13.1
                        elif y == 3:
                                return 8.7
                elif DWT == 15000:
                        if y == 0:
                                return 157
                        elif y == 1:
                                return 23.3
                        elif y == 2:
                                return 13.6
                        elif y == 3:
                                return 9.6
                elif DWT == 20000:
                        if y == 0:
                                return 166
                        elif y == 1:
                                return 25.2
                        elif y == 2:
                                return 14.1
                        elif y == 3:
                                return 10.1
                elif DWT==30000:
                        if y == 0:
                                return 192
                        elif y == 1:
                                return 27.6
                        elif y == 2:
                                return 15.5
                        elif y == 3:
                                return 11.0
                elif DWT == 40000:
                        if y == 0:
                                return 200
                        elif y == 1:
                                return 32.2
                        elif y == 2:
                                return 19.0
                        elif y == 3:
                                return 12.3
                else:
                        print('Data error!!!')
        
        elif Type == 2:
                if DWT == 2000:
                        if y == 0:
                                return 78
                        elif y == 1:
                                return 14.3
                        elif y == 2:
                                return 6.2
                        elif y == 3:
                                return 5.0
                elif DWT == 3000:
                        if y == 0:
                                return 96
                        elif y == 1:
                                return 16.6
                        elif y == 2:
                                return 7.8
                        elif y == 3:
                                return 5.8
                elif DWT == 5000:
                        if y == 0:
                                return 115
                        elif y == 1:
                                return 18.8
                        elif y == 2:
                                return 9.0
                        elif y == 3:
                                return 7.0
                elif DWT == 10000:
                        if y == 0:
                                return 135
                        elif y == 1:
                                return 20.5
                        elif y == 2:
                                return 11.4
                        elif y == 3:
                                return 8.5
                elif DWT == 15000:
                        if y == 0:
                                return 150
                        elif y == 1:
                                return 23.0
                        elif y == 2:
                                return 12.5
                        elif y == 3:
                                return 9.1
                elif DWT == 20000:
                        if y == 0:
                                return 164
                        elif y == 1:
                                return 25.0
                        elif y == 2:
                                return 13.5
                        elif y == 3:
                                return 9.8
                elif DWT == 35000:
                        if y == 0:
                                return 190
                        elif y == 1:
                                return 30.4
                        elif y == 2:
                                return 15.8
                        elif y == 3:
                                return 11.2
                elif DWT == 50000:
                        if y == 0:
                                return 223
                        elif y == 1:
                                return 32.3
                        elif y == 2:
                                return 17.9
                        elif y == 3:
                                return 12.8
                elif DWT == 70000:
                        if y == 0:
                                return 228
                        elif y == 1:
                                return 32.3
                        elif y == 2:
                                return 19.6
                        elif y == 3:
                                return 14.2
                elif DWT == 100000:
                        if y == 0:
                                return 250
                        elif y == 1:
                                return 43.0
                        elif y == 2:
                                return 20.3
                        elif y == 3:
                                return 14.5
                elif DWT == 120000:
                        if y == 0:
                                return 266
                        elif y == 1:
                                return 43.0
                        elif y == 2:
                                return 23.5
                        elif y == 3:
                                return 16.7
                elif DWT == 150000:
                        if y == 0:
                                return 289
                        elif y == 1:
                                return 45.0
                        elif y == 2:
                                return 24.3
                        elif y == 3:
                                return 17.9
                elif DWT == 200000:
                        if y == 0:
                                return 312
                        elif y == 1:
                                return 50.0
                        elif y == 2:
                                return 25.5
                        elif y == 3:
                                return 18.5
                elif DWT == 250000:
                        if y == 0:
                                return 325
                        elif y == 1:
                                return 50.0
                        elif y == 2:
                                return 26.5
                        elif y == 3:
                                return 20.5
                elif DWT == 300000:
                        if y == 0:
                                return 339
                        elif y == 1:
                                return 58.0
                        elif y == 2:
                                return 30.0
                        elif y == 3:
                                return 23.0
                elif DWT == 350000:
                        if y == 0:
                                return 342
                        elif y == 1:
                                return 63.5
                        elif y == 2:
                                return 30.2
                        elif y == 3:
                                return 23.0
                else:
                        print('Data error!!!')
           
        elif Type == 3:
                if DWT == 1000:
                        if y == 0:
                                return 70
                        elif y == 1:
                                return 13.0
                        elif y == 2:
                                return 5.2
                        elif y == 3:
                                return 4.3
                elif DWT == 2000:
                        if y == 0:
                                return 86
                        elif y == 1:
                                return 13.6
                        elif y == 2:
                                return 6.1
                        elif y == 3:
                                return 5.1
                elif DWT == 3000:
                        if y == 0:
                                return 97
                        elif y == 1:
                                return 15.2
                        elif y == 2:
                                return 7.2
                        elif y == 3:
                                return 5.9
                elif DWT == 5000:
                        if y == 0:
                                return 125
                        elif y == 1:
                                return 17.5
                        elif y == 2:
                                return 8.6
                        elif y == 3:
                                return 7.0
                elif DWT == 10000:
                        if y == 0:
                                return 141
                        elif y == 1:
                                return 20.4
                        elif y == 2:
                                return 10.7
                        elif y == 3:
                                return 8.3
                elif DWT == 20000:
                        if y == 0:
                                return 164
                        elif y == 1:
                                return 26.0
                        elif y == 2:
                                return 13.4
                        elif y == 3:
                                return 10.0
                elif DWT == 30000:
                        if y == 0:
                                return 185
                        elif y == 1:
                                return 31.5
                        elif y == 2:
                                return 17.3
                        elif y == 3:
                                return 12.0
                elif DWT == 50000:
                        if y == 0:
                                return 229
                        elif y == 1:
                                return 32.2
                        elif y == 2:
                                return 19.1
                        elif y == 3:
                                return 12.8
                elif DWT == 80000:
                        if y == 0:
                                return 243
                        elif y == 1:
                                return 42.0
                        elif y == 2:
                                return 20.8
                        elif y == 3:
                                return 14.3
                elif DWT == 100000:
                        if y == 0:
                                return 246
                        elif y == 1:
                                return 43.0
                        elif y == 2:
                                return 21.4
                        elif y == 3:
                                return 14.8
                elif DWT == 120000:
                        if y == 0:
                                return 265
                        elif y == 1:
                                return 45.0
                        elif y == 2:
                                return 23.0
                        elif y == 3:
                                return 16.0
                elif DWT == 150000:
                        if y == 0:
                                return 274
                        elif y == 1:
                                return 50.0
                        elif y == 2:
                                return 24.2
                        elif y == 3:
                                return 17.1
                elif DWT == 250000:
                        if y == 0:
                                return 333
                        elif y == 1:
                                return 60.0
                        elif y == 2:
                                return 29.7
                        elif y == 3:
                                return 19.9
                elif DWT == 300000:
                        if y == 0:
                                return 334
                        elif y == 1:
                                return 60.0
                        elif y == 2:
                                return 31.2
                        elif y == 3:
                                return 22.5
                elif DWT == 450000:
                        if y == 0:
                                return 380
                        elif y == 1:
                                return 68.0
                        elif y == 2:
                                return 34.0
                        elif y == 3:
                                return 24.5
                else:
                        print('Data error!!!')

        elif Type == 4:
                if DWT == 1000:
                        if y == 0:
                                return 90
                        elif y == 1:
                                return 15.4
                        elif y == 2:
                                return 6.8
                        elif y == 3:
                                return 4.8
                elif DWT == 3000:
                        if y == 0:
                                return 106
                        elif y == 1:
                                return 17.6
                        elif y == 2:
                                return 8.7
                        elif y == 3:
                                return 5.8
                elif DWT == 5000:
                        if y == 0:
                                return 121
                        elif y == 1:
                                return 19.2
                        elif y == 2:
                                return 9.2
                        elif y == 3:
                                return 6.9
                elif DWT == 10000:
                        if y == 0:
                                return 141
                        elif y == 1:
                                return 22.6
                        elif y == 2:
                                return 11.3
                        elif y == 3:
                                return 8.3
                elif DWT == 20000:
                        if y == 0:
                                return 183
                        elif y == 1:
                                return 27.6
                        elif y == 2:
                                return 14.4
                        elif y == 3:
                                return 10.5
                elif DWT == 30000:
                        if y == 0:
                                return 241
                        elif y == 1:
                                return 32.3
                        elif y == 2:
                                return 19.0
                        elif y == 3:
                                return 12.0
                elif DWT == 50000:
                        if y == 0:
                                return 293
                        elif y == 1:
                                return 32.3
                        elif y == 2:
                                return 21.8
                        elif y == 3:
                                return 13.0
                elif DWT == 70000:
                        if y == 0:
                                return 300
                        elif y == 1:
                                return 40.3
                        elif y == 2:
                                return 24.3
                        elif y == 3:
                                return 14.0
                elif DWT == 100000:
                        if y == 0:
                                return 346
                        elif y == 1:
                                return 45.6
                        elif y == 2:
                                return 24.8
                        elif y == 3:
                                return 14.5
                elif DWT == 120000:
                        if y == 0:
                                return 367
                        elif y == 1:
                                return 45.6
                        elif y == 2:
                                return 27.2
                        elif y == 3:
                                return 15.0
                elif DWT == 150000:
                        if y == 0:
                                return 398
                        elif y == 1:
                                return 56.4
                        elif y == 2:
                                return 30.2
                        elif y == 3:
                                return 16.5
                else:
                        print('Data error!!!')
            
#定义船类型，Ls=1，Lm=2，Ll=3. 其中L已经转化为以元胞为单位的长度
def Ship_Type(L,v):
    if (L == 1 or L == 2) and v <= 6:
        return 1
    elif (L <= 6 and L >= 3) and v <= 16:
        return 2
    elif L > 6 and v <= 12:
        return 3
    else:
        return 0                        #本元胞自动机中不存在该船型

