from pico2d import *
import main_state
import math
import random
import store_state
#   ----    모든 게임 오브젝트를 여기서 설계  ----



class bullet:
    img=None
    sp=None
    lockon=None
    dm=None
    x=None
    y=None
    mx=None#날아갈 x방향
    my=None#날아갈 y방향
    BoundR=None
    delobj=None
    lockonlist=None
    def __init__(self,image,sp,lockon,lockonlist,dm,x,y,br,l,b,w,h):
        self.img=image
        self.lockon=lockon
        self.dm=dm
        self.x=x
        self.y=y
        self.mx=lockon.x-self.x
        self.my=lockon.y-self.y
        self.sp = sp*1/math.sqrt((self.mx)*(self.mx) + (self.my)*(self.my))
        self.mx*=self.sp
        self.my*=self.sp
        self.BoundR=br
        self.delobj=False
        self.left=l
        self.bottom=b
        self.width=w
        self.height=h
        self.lockonlist=lockonlist

    def Update(self):#해당방향으로 매틱마다 움직임 그리고 충돌할 경우 자신을 제거대상에 올림
        self.x+=self.mx
        self.y+=self.my

        if self.y<0:
            self.delobj=True

        if self.y>800:
            self.delobj=True

        for p in self.lockonlist:
            x = p.x - self.x
            y = p.y - self.y
            l = math.sqrt(x * x + y * y)
            if l <= self.BoundR+p.BoundR:
                d=(self.dm-p.df)
                if d<=0:
                    d=1
                p.hp-=d
                self.delobj=True

    def Draw(self):
        self.img.clip_draw(self.left,self.bottom,self.width,self.height, self.x, self.y)



class Enemy1:
    STATE = ['Attack', 'Dodge']
    curState=STATE[0]
    threat=0
    image=None
    bulletimg=None
    wave=0
    hp=100#체력
    df=0#방어력
    dm=10#공격력
    sp=2#속도
    fs=100#발사속도
    rg=300#사거리
    fireframe=0
    BoundR=60
    delobj=False
    def __init__(self,i):
        self.wave=i
        self.x=800+random.randint(-450,450)
        self.y=500+random.randint(-50,55)+self.wave*400
        if Enemy1.image==None:
            Enemy1.image =load_image('Enemy12.png')
            Enemy1.bulletimg=load_image('EnemyBullet.png')

    def Draw(self):
        self.image.clip_draw(150,265,130,100,self.x,self.y)

    def Update(self):
        if self.AI()==True:#아무행동도 안했으면
            self.y-=self.sp#움직이게함
        if self.hp<0:
            self.delobj=True


    def Attack(self,p):
        if self.fireframe==0:
            main_state.Enemybullet+=[bullet(self.bulletimg,10,p,main_state.player,self.dm,self.x,self.y,10,170, 303, 25, 25)]
            p.threat+=self.dm
            self.fireframe+=1
        elif self.fireframe <self.fs:
            self.fireframe+=1
        else:
            self.fireframe=0

    def AI(self):
        ai = True  # 특정행동을 했으면 False로 바뀜
        for p in main_state.player:
            x = p.x - self.x
            y = p.y - self.y
            l = math.sqrt(x * x + y * y)
            if l <= self.rg:
                self.Attack(p)
                ai = False

        return ai

class Enemy2:
    STATE = ['Attack', 'Dodge']
    curState='Attack'
    threat=0
    image=None
    bulletimg=None
    wave=0
    hp=50#체력
    df=0#방어력
    dm=30#공격력
    sp=2#속도
    fs=300#발사속도
    rg=500#사거리
    fireframe=0
    BoundR=60
    delobj=False
    def __init__(self,i):
        self.wave=i
        self.x=800+random.randint(-450,450)
        self.y=500+random.randint(-50,55)+self.wave*400
        if Enemy2.image==None:
            Enemy2.image =load_image('Enemy2.png')
            Enemy2.bulletimg=load_image('EnemyBullet.png')

    def Draw(self):
        self.image.draw(self.x,self.y)

    def Update(self):
        if self.AI()==True:#아무행동도 안했으면
            self.y-=self.sp#움직이게함
        if self.hp<0:
            self.delobj=True


    def Attack(self,p):
        if self.fireframe==0:
            main_state.Enemybullet+=[bullet(self.bulletimg,16,p,main_state.player,self.dm,self.x,self.y,10,170, 330, 25, 25)]
            p.threat+=self.dm
            self.fireframe+=1
        elif self.fireframe <self.fs:
            self.fireframe+=1
        else:
            self.fireframe=0


    def AI(self):
        ai=True#특정행동을 했으면 False로 바뀜

        if self.curState==self.STATE[0]:
            for p in main_state.player:
                x=p.x-self.x
                y=p.y-self.y
                l=math.sqrt(x*x+y*y)
                if l<=self.rg:
                    self.Attack(p)
                    ai=False
            if self.threat > 40:  # 만약 어느정도 위험하다 생각되면
                self.curState=self.STATE[1]
                d=1

        elif self.curState==self.STATE[1]:
            ai=False
            self.x+=random.randint(20,80)

            self.threat=0
            self.curState=self.STATE[0]
        return ai




class Unit1:
    STATE = ['Attack', 'Dodge']
    curState = 'Attack'
    threat=0
    d=0
    image=None
    bulletimg=None
    hp=150+(store_state.Upgrade3*(25))#체력
    df=1+(store_state.Upgrade2*(1))#방어력
    dm=7+(store_state.Upgrade1*(3))#공격력
    sp=2#속도
    fs=100-(store_state.Upgrade4*(5))#발사속도
    rg=400#사거리
    BoundR=60
    fireframe=0
    delobj=False

    def __init__(self,x,y):
        self.x=x
        self.y=y
        if Unit1.image==None:
            Unit1.image =load_image('Unit1.png')
            Unit1.bulletimg=load_image('EnemyBullet.png')

    def Draw(self):
        self.image.draw(self.x,self.y+40)

    def Update(self):
        if self.AI() == True:  # 아무행동도 안했으면
            self.y += self.sp  # 움직이게함
        if self.hp<0:
            self.delobj=True

    def Attack(self,p):
        if self.fireframe==0:
            main_state.playerbullet+=[bullet(self.bulletimg,8,p,main_state.Enemy,self.dm,self.x,self.y,10,85, 303, 25,25)]
            p.threat+=self.dm
            self.fireframe+=1
        elif self.fireframe <self.fs:
            self.fireframe+=1
        else:
            self.fireframe=0

    def Dodge(self):
        self.d+=1
        if self.d<10:
            self.x+=25
        elif self.d>=10 and self.d<30:
            self.x-=25
        elif self.d>=30and self.d<40:
            self.x+=25
        else:
            self.curState=self.STATE[0]
            self.threat=0

    def AI(self):
        ai = True  # 특정행동을 했으면 False로 바뀜

        for p in main_state.Enemy:
            x = p.x - self.x
            y = p.y - self.y
            l = math.sqrt(x * x + y * y)
            if l <= self.rg:
                self.Attack(p)
                ai = False
        if self.threat > 40:  # 만약 어느정도 위험하다 생각되면
            self.curState = self.STATE[1]

        if self.curState==self.STATE[1]:# 회피상태가 오면 와리가리 무빙샷
            self.Dodge()

        return ai

