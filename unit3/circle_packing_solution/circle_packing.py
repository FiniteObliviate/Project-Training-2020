#载入random用于随机取点作为圆心
import random
#载入optimize用于求取函数在多个约束条件下的最优化问题
from scipy.optimize import minimize
#载入time用于记录执行程序所需时间
import time

#创建圆类，封装圆的3个参数和9个函数
class circle:

    x=0
    y=0
    radius=0

#初始化一个新的圆
    def __init__(self, x, y, r):
        self.x=x
        self.y=y
        self.radius=abs(r)

#以复数形式返回圆心信息
    def center(self):
        return complex(self.x,self.y)

#计算并返回两圆之间的距离（圆面上的点的最短距离）
#由于圆心坐标由复数表示，所以对圆心求差再取模就是圆心之间的距离
#圆心间的距离与半径和相减，圆面上的点的最短距离
    def distance(self, other):
        c_1=self.center()
        c_2=other.center()
        r_1=self.radius
        r_2=other.radius
        return abs(c_1-c_2)-(r_1+r_2)

#测试两圆是否相交，并返回bool运算值
#使用distance函数，如果圆面上的点的最短距离为负，意味着圆面没有重叠部分，反之亦然
    def test_overlap(self,other):
        d=self.distance(other)
        if d<0:
            return True
        elif d>=0:
            return False

#测试c_list中有没有两圆内含的情况，并返回bool运算值
#两圆心之间的距离如果比半径还短，则是内含情况，也不满足要求
#这个函数弥补了test_overlap判断圆与圆之间的关系是否符合要求的漏洞
    def test_contain(self, c_list):
        if len(c_list)==0:
            return False
        else:
            flag=False
            for c in c_list:
                c_1=c.center()
                r_1=c.radius
                d=abs(self.center()-c_1)
                if d<=r_1:
                    flag+=True
                    break
                else:
                    flag+=False
            return flag

#测试圆是否在给定的正方形区域内
    def test_rec(self):
        x=self.x
        y=self.y
        r=self.radius
        left=abs(x-r)
        right=abs(x+r)
        up=abs(y+r)
        down=abs(y-r)
        if max(left, right, up, down)>1:
           return False
        else:
           return True

#判测试圆是否满足所有要要求，并返回bool运算值
#整合了上面三个函数的功能，经过测试的圆满足：在正方形内，不和别的圆重叠，不内含别的圆
    def test_cir(self, c_list):
        if self.test_rec():
            flag=True
            if len(c_list)==0:
                return True
            else:
                flag=not self.test_contain(c_list)
                for c in c_list:
                    flag=flag and not self.test_overlap(c)
                if flag:
                    return True
                else:
                    return False
        else:
            return False

#将满足要求的圆加在c_list列表中
    def add_cir(self, c_list):
        if self.test_cir(c_list):
            c_list.append(self)
        else:
            return False

#打印圆心坐标和半径
    def print(self):
        x=self.x
        y=self.y
        r=self.radius
        print("Center\t(%f,%f) \t Radius\t%f" % (x,y,r))


#下面4个函数在圆类封装之外
#计算半径能取到的最大值
#r_list包含了圆和正方形的四条边，和现有其他圆之间的所有距离值
#r_list中的最小值就是保证圆不和正方形和其他圆相交的最大半径
def max_radius(c, c_list):
    x=c.x
    y=c.y
    r_list=[1-x, 1+x, 1-y, 1+y]
    if not len(c_list)==0:
        for cir in c_list:
            r=cir.distance(c)+c.radius
            r_list.append(r)
    return min(r_list)

#找出使得R^2最大的一系列圆，返回这个圆列表c_list
#以4为周期是因为人为事先预测：
#从第二个圆开始，满足条件的圆每次都是在正方形的四个角的空闲区域取到的
def opti_max_r2(c_num): #参数是圆的个数
    c_list=[]
    while len(c_list)<c_num: #最外层循环：判断是否已经生成了要求数量的圆
        count=len(c_list)
        mod=(count+1)%4
        if count==0: #第一个圆不纳入周期为4的循环
            x=0
            y=0
            c=circle(x,y,1)
            c.add_cir(c_list)
        else: #从第二个圆开始，以4为周期轮番在正方形的四个角找合适位置画圆
            if mod==0: #右上角
                x=random.uniform(0,1)
                y=random.uniform(0,1)
            elif mod==1: #左上角
                x=random.uniform(-1,0)
                y=random.uniform(0,1)
            elif mod==2: #左下角
                x=random.uniform(-1,0)
                y=random.uniform(-1,0)
            elif mod==3: #右下角
                x=random.uniform(0,1)
                y=random.uniform(-1,0)
            c=circle(x,y,0)
            #由于要用minimize函数求最大值，所以加了一个负号
            fun=lambda x: -max_radius(circle(x[0],x[1],0), c_list)
            #利用scipy模块的minimize函数解非线性规划问题
            #找到使得max_radius最大这个条件下的圆心坐标
            #minimize函数的3个参数分别是需要最小化的函数，初值，解决方案的种类
            opti_c=minimize(fun,(c.x,c.y),method='SLSQP')
            #将找出的圆的坐标与半径信息存入c_list
            c.x=float(opti_c.x[0])
            c.y=float(opti_c.x[1])
            c.radius=max_radius(c,c_list)
            c.add_cir(c_list)
    return c_list

#计算并返回求出的一系列圆的R^2之和
def sum_r2(c_list): #计算半径r的平方和
    r2=0
    for c in c_list:
         r2+=c.radius**2
    return r2

#打印圆的信息
def print_circle(c_list):
    num=0
    for c in c_list:
        num=num+1
        print("Circle\t%d: " % (num))
        c.print()


if __name__=="__main__":
    t1=time.time() #为程序运行计时
    circle_num=10 #圆的个数
    c_list=opti_max_r2(circle_num) #找到满足条件的一系列圆
    print("The coordinate and radius are:") #打印圆心坐标，半径，R^2的和，所用时间
    print_circle(c_list)
    r2=sum_r2(c_list)
    print("The maximum sum of R^2 we find:", r2)
    t2=time.time()
    print('Time cost:',t2-t1)
