#定义安全距离
def dsafe(k):
    if k==1:
        dsafe1=round(max(3*Li,1.8*Lf1))
        dsafe2=round(max(3*Li,1.8*Lf2))
        dsafe3=round(max(3*Lf1,1.8*Li))
        dsafe4=round(3*Li+3*Lf1_0)
        dsafe5=round(max(1.8*Lb1_0,1.8*Li))
        return [dsafe1,dsafe2,dsafe3,dsafe4,dsafe5]
    else:
        dsafe1=round(3*Li+3*Lf1)
        dsafe2=round(3*Li+3*Lf2)
        dsafe3=round(max(1.8*Lf1,1.8*Li))
        dsafe4=round(max(3*Li,1.8*Lf1_0))
        dsafe5=round(max(3*Lb1_0,1.8*Li))
        return [dsafe1,dsafe2,dsafe3,dsafe4,dsafe5]
    
#时间、距离参数
def d1(k,t):
    if k==1:
        return f1+Vf1(t)-i-Vi(t)-Li
    else:
        return f1-Vf1(t)-Lf1-i-Vi(t)-Li+1
    if kf1==1 and kf2==1:
        return f2+Vf2(t)-f1-Vf1(t)-Lf1
    elif kf1==1 and kf2==0:
        return f2-Vf2(t)-Lf2-f1-Vf1(t)-Lf1+1
    elif kf1==0 and kf2==1:
        return f2+Vf2(t)-f1+Vf1(t)-1
    else:
        return f2-Vf2(t)-Lf2-f1+Vf1(t)

def d1_0(k,t):
    if k==1:
        return f1_0+Vf1_0(t)-f1-Vf1(t)-Lf1
    else:
        return f1_0+Vf1_0(t)-Lf2-kf1-Vf1(t)-Lf1+1

def db1_0(k,t):
    if k==1:
        return f1+Vf1(t)-f1_0-Vf1_0(t)-Lf1_0
    else:
        return f1+Vf1(t)-f1_0+Vf1_0(t)-1

def db1(k,t):
    if k==1:
        return i+Vi(t)-f1-Vf1(t)-Lf1
    else:
        return i+Vi(t)-f1+Vf1(t)-1

def df1(k,t):
    if k==1:
        return f2+Vf2(t)-i-Vi(t)-Li
    else:
        return f2-Vf2(t)-Lf1-i-Vi(t)-Li+1

def tovertake(k):
    if k==1:
        return (f1-i+dsafe3)/((Vi(t)+Vmax)/2-Vf1(t))
    else:
        return float(inf)

def headon(k):
    if k==1:
        return (f1_0-i-Li-Lf1_0-dsafe2)/((Vi(t)+Vmax)/2+Vf1_0(t))
    else:
        return 0




