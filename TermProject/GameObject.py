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
    pattern=None
    aframe=0
    accel=1.03
    def __init__(self,image,sp,lockon,lockonlist,dm,x,y,br,l,b,w,h,pattern=0):
        self.img=image
        self.lockon=lockon
        self.dm=dm
        self.x=x
        self.y=y
        self.pattern=pattern
        tx=0
        ty=0
        if type(lockon)==list:
            self.mx=lockon[0]
            self.my=lockon[1]

        elif self.lockon==0:
            self.mx=0
            self.my=sp
        else:
            tx=lockon.x-self.x
            ty=lockon.y-self.y
            self.mx=tx
            self.my=ty

            self.sp = sp
            self.mx*=self.sp*1/math.sqrt((tx) * (tx) + (ty) * (ty))
            self.my*=self.sp*1/math.sqrt((tx) * (tx) + (ty) * (ty))
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
        tx=0
        ty=0

        if self.y<-200:
            self.delobj=True

        if self.y>1000:
            self.delobj=True

        if self.pattern ==0:
            pass
        elif self.pattern==1:

            tx=self.lockon.x - self.x
            ty=self.lockon.y - self.y
            self.mx=tx
            self.my=ty
            t=math.sqrt((tx) * (tx) + (ty) * (ty))
            if t!=0:
                self.mx *= self.sp * 1 / t
                self.my *= self.sp * 1 / t

            if self.lockon.delobj==True:
                self.delobj=True

            if main_state.stage%2==0:
                if self.aframe>=2:
                    self.aframe=0
                else:
                    self.aframe+=1
            else:
                self.aframe=0


        elif self.pattern==2:
            self.aframe=1
        elif self.pattern==3:
            self.mx*=self.accel
            self.my*=self.accel


        for p in self.lockonlist:
            x = p.x - self.x
            y = p.y - self.y
            l = math.sqrt(x * x + y * y)

            if p.BoundR==0:
                pass
            else:
                if l <= self.BoundR+p.BoundR:
                    d=(self.dm-p.df)
                    if d<=1:
                        d=1
                    p.hp-=d
                    self.delobj=True

    def Draw(self):
        self.img.clip_draw(self.left+int(self.aframe)*self.width,self.bottom,self.width,self.height, self.x, self.y)


class Enemy1:
    STATE = ['Attack', 'Dodge']
    curState=STATE[0]
    threat=0
    image=None
    bulletimg=None
    wave=0
    hp=160#체력
    maxhp=hp
    df=0#방어력
    dm=10#공격력
    sp=2.2#속도
    fs=100#발사속도
    rg=270#사거리
    fireframe=0
    BoundR=50
    delobj=False
    dframe=-1#피가 0일때 폭팔이미지
    bomb = None
    sound=None
    hpbar=None
    def __init__(self,i):
        self.dframe=-1
        self.wave=i
        self.hp=160.1+20*main_state.stage
        self.maxhp=self.hp
        self.x=800+random.randint(-450,450)
        self.y=600+random.randint(-50,55)+self.wave*400
        if Enemy1.image==None:
            Enemy1.image =load_image('Enemy12.png')
            Enemy1.bulletimg=load_image('EnemyBullet.png')
            Enemy1.bomb=load_image('bomb.png')
            Enemy1.sound=load_wav('boom.wav')
            Enemy1.sound.set_volume(35)
            Enemy1.hpbar = load_image('hpbar.png')

    def Draw(self):

        self.hpbar.draw(self.x,self.y+15,30*self.hp/self.maxhp,30)
        if self.hp>0:
            self.image.clip_draw(150,265,130,100,self.x,self.y-20,50,50)
        else:
            self.bomb.clip_draw(self.dframe*95,0,95,70,self.x,self.y,50,50)

    def Update(self):
        if self.AI()==True:#아무행동도 안했으면
            self.y-=self.sp#움직이게함
        if self.hp<0 and self.dframe<0:

            self.dframe=0
            #self.delobj=True
        if self.dframe>=7:
            self.delobj=True
        else:
            if self.hp<=0:
                self.sound.play(1)
                self.dframe+=1


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
        if self.y<700:
            self.BoundR=60
            for p in main_state.player:
                x = p.x - self.x
                y = p.y - self.y
                l = math.sqrt(x * x + y * y)
                if l <= self.rg:
                    self.Attack(p)
                    ai = False
        else:
            self.BoundR=0

        return ai

class Enemy2:
    STATE = ['Attack', 'Dodge']
    curState='Attack'
    threat=0
    image=None
    bulletimg=None
    wave=0
    hp=120#체력
    maxhp=hp
    df=1#방어력
    dm=50#공격력
    sp=1.5#속도
    fs=300#발사속도
    rg=500#사거리
    fireframe=0
    BoundR=50
    delobj=False
    dframe=-1#피가 0일때 폭팔이미지
    bomb = None
    sound=None
    hpbar=None
    def __init__(self,i):
        self.wave=i
        self.x=800+random.randint(-450,450)
        self.y=600+random.randint(-50,55)+self.wave*400
        if Enemy2.image==None:
            Enemy2.image =load_image('Enemy2.png')
            Enemy2.bulletimg=load_image('EnemyBullet.png')
            Enemy2.bomb=load_image('bomb.png')
            Enemy2.sound = load_wav('boom.wav')
            Enemy2.sound.set_volume(35)
            Enemy2.hpbar=load_image('hpbar.png')
    def Draw(self):
        self.hpbar.draw(self.x, self.y + 45, 30 * self.hp / self.maxhp, 30)
        if self.hp>0:
            self.image.draw(self.x, self.y,60,80)
        else:
            self.bomb.clip_draw(self.dframe*95,0,95,70,self.x,self.y,80,80)


    def Update(self):
        if self.AI()==True:#아무행동도 안했으면
            self.y-=self.sp#움직이게함
        if self.hp<0 and self.dframe<0:
            self.dframe=0
        if self.dframe>=7:
            self.delobj=True
        else:
            if self.hp<=0:
                self.sound.play(1)
                self.dframe+=1


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
        if self.y<700:
            self.BoundR=60
            if self.curState==self.STATE[0]:
                for p in main_state.player:
                    x=p.x-self.x
                    y=p.y-self.y
                    l=math.sqrt(x*x+y*y)
                    if l<=self.rg:
                        self.Attack(p)
                        ai=False
                if self.threat > 130:  # 만약 어느정도 위험하다 생각되면
                    self.curState=self.STATE[1]
                    d=1

            elif self.curState==self.STATE[1]:
                ai=False
                self.x+=random.randint(20,80)

                self.threat=0
                self.curState=self.STATE[0]
        else:
            self.BoundR=0
        return ai

class Enemy3:
    STATE = ['Attack', 'Dodge']
    curState = 'Attack'
    threat=0
    d=0
    image=None
    bulletimg=None
    hp=170
    maxhp=hp
    df=7
    dm=6
    sp=4#속도
    fs=30
    rg=300#사거리
    BoundR=35
    fireframe=0
    delobj=False
    dframe=-1#피가 0일때 폭팔이미지
    bomb = None
    sound=None
    hpbar=None

    def __init__(self,i):
        self.wave=i
        self.x=800+random.randint(-450,450)
        self.y=600+random.randint(-50,55)+self.wave*300
        self.aframe=0
        if Enemy3.image==None:
            Enemy3.image =load_image('Enemy3.png')
            Enemy3.bulletimg=load_image('EnemyBullet.png')
            Enemy3.bomb=load_image('bomb.png')
            Enemy3.sound = load_wav('boom.wav')
            Enemy3.sound.set_volume(35)
            Enemy3.hpbar=load_image('hpbar.png')

#8 71
    def Draw(self):
        self.hpbar.draw(self.x, self.y + 60, 30 * self.hp / self.maxhp, 30)
        if self.hp>0:
            self.image.clip_draw(self.aframe*64+8,0,63,79,self.x, self.y + 20,)
        else:
            self.bomb.clip_draw(self.dframe*95,0,95,70,self.x,self.y)

    def Update(self):
        if self.AI() == True:  # 아무행동도 안했으면
            self.y -= self.sp  # 움직이게함
        if self. hp>0:
            self.aframe+=1
        if self.aframe>=4:
            self.aframe=0
        if self.hp<0 and self.dframe<0:
            self.dframe=0
        if self.dframe>=7:
            self.delobj=True
        else:
            if self.hp<=0:
                self.sound.play(1)
                self.dframe+=1

    def Attack(self,p):
        if self.fireframe==0:
            main_state.Enemybullet += [bullet(self.bulletimg, 8, p, main_state.player, self.dm, self.x, self.y, 10, 400, 453, 25, 25,1)]
            p.threat+=self.dm
            self.fireframe+=1
        elif self.fireframe <self.fs:
            self.fireframe+=1
        else:
            self.fireframe=0

    def Dodge(self):
        self.d += 1
        if self.d < 10:
            self.x += 15
        elif self.d >= 10 and self.d < 30:
            self.x -= 15
        elif self.d >= 30 and self.d < 40:
            self.x += 15
        else:
            self.curState = self.STATE[0]
            self.threat = 0
            self.d = 0

    def AI(self):
        ai = True  # 특정행동을 했으면 False로 바뀜
        if self.y<700:
            self.BoundR=45
            for p in main_state.player:
                x = p.x - self.x
                y = p.y - self.y
                l = math.sqrt(x * x + y * y)
                if l <= self.rg:
                    self.Attack(p)
                    ai = False
                    break
            if self.threat > 40:  # 만약 어느정도 위험하다 생각되면
                self.curState = self.STATE[1]

            if self.curState==self.STATE[1]:# 회피상태가 오면 뒤로 회피 이때 무적
                self.Dodge()
        else:
            self.BoundR=0

        return ai




class Unit1:
    STATE = ['Attack', 'Dodge']
    curState = 'Attack'
    threat=0
    d=0
    image=None
    bulletimg=None
    hp=200+(store_state.Upgrade3*(25))#체력
    df=1+(store_state.Upgrade2*(1))#방어력
    dm=10+(store_state.Upgrade1*(4))#공격력
    sp=2.2#속도
    fs=100-(store_state.Upgrade4*(5))#발사속도
    rg=310#사거리
    BoundR=50
    fireframe=0
    delobj=False
    dframe=-1#피가 0일때 폭팔이미지
    bomb = None
    sound1=None
    sound=None
    maxhp=hp
    hpbar=None
    powershot=True
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.hp = 200 + (store_state.Upgrade3 * (35))  # 체력
        self.df = 1 + (store_state.Upgrade2 * (2))  # 방어력
        self.dm = 10 + (store_state.Upgrade1 * (4))  # 공격력
        self.sp = 2.2  # 속도
        self.fs = 90 - (store_state.Upgrade4 * (5))  # 발사속도
        self.maxhp=self.hp
        if Unit1.image==None:
            Unit1.image =load_image('Unit1.png')
            Unit1.bulletimg=load_image('EnemyBullet.png')
            Unit1.bomb=load_image('bomb.png')
            Unit1.sound1=load_wav('laser2.wav')
            Unit1.sound1.set_volume(40)
            Unit1.sound = load_wav('boom.wav')
            Unit1.sound.set_volume(25)
            Unit1.hpbar=load_image('hpbar.png')


    def Draw(self):
        self.hpbar.draw(self.x, self.y + 50, 30 * self.hp / self.maxhp, 30)
        if self.hp>0:
            self.image.draw(self.x, self.y + 20,50,50)
        else:
            self.bomb.clip_draw(self.dframe*95,0,95,70,self.x,self.y,50,50)

    def Update(self):
        if self.AI() == True and self.y<=600:  # 아무행동도 안했으면
            self.y += self.sp  # 움직이게함
        if self.hp<0 and self.dframe<0:
            self.sound.play(1)
            self.dframe=0
        if self.dframe>=7:
            self.delobj=True
        else:
            if self.hp<=0:
                self.dframe+=1

    def Attack(self,p):
        if self.fireframe==0:
            self.sound1.play(1)
            main_state.playerbullet+=[bullet(self.bulletimg,8,p,main_state.Enemy,self.dm,self.x,self.y,10,85, 303, 25,25)]
            if self.powershot==True:
                main_state.playerbullet += [
                    bullet(self.bulletimg, 16, [-2,2], main_state.Enemy, self.dm, self.x, self.y, 10, 85, 303, 25, 25)]
                main_state.playerbullet += [
                    bullet(self.bulletimg, 16, [2,2], main_state.Enemy, self.dm, self.x, self.y, 10, 85, 303, 25, 25)]

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
            self.d=0

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

class Unit2:
    STATE = ['Attack', 'Dodge']
    curState = 'Attack'
    threat=0
    d=0
    image=None
    bulletimg=None
    hp=80+(store_state.Upgrade3*(25))#체력
    df=0+(store_state.Upgrade2*(1))#방어력
    dm=60+(store_state.Upgrade1*(30))#공격력
    sp=1#속도
    fs=200-(store_state.Upgrade4*(1))#발사속도
    rg=650#사거리
    BoundR=60
    fireframe=0
    delobj=False
    dframe=-1#피가 0일때 폭팔이미지
    bomb = None
    sound1=None
    sound=None
    maxhp=hp
    hpbar=None
    powershot=True
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.hp = 80 + (store_state.Upgrade3 * (25))  # 체력
        self.df = 0 + (store_state.Upgrade2 * (1))  # 방어력
        self.dm = 60 + (store_state.Upgrade1 * (30))  # 공격력
        self.sp = 1  # 속도
        self.fs = 200 - (store_state.Upgrade4 * (1))  # 발사속도
        self.maxhp=self.hp
        self.aframe=0
        if Unit2.image==None:
            Unit2.image =load_image('Unit2.png')
            Unit2.bulletimg=load_image('EnemyBullet.png')
            Unit2.bomb=load_image('bomb.png')
            Unit2.sound1=load_wav('laser1.wav')
            Unit2.sound1.set_volume(20)
            Unit2.sound = load_wav('boom.wav')
            Unit2.sound.set_volume(25)
            Unit2.hpbar=load_image('hpbar.png')
    def Draw(self):
        self.hpbar.draw(self.x, self.y + 55, 30 * self.hp / self.maxhp, 30)
        if self.hp>0:
            self.image.clip_draw(self.aframe*80,0,80,101,self.x, self.y + 20,50,60)
        else:
            self.bomb.clip_draw(self.dframe*95,0,95,70,self.x,self.y,60,60)

    def Update(self):
        if self.AI() == True and self.y<=600:  # 아무행동도 안했으면
            self.y += self.sp  # 움직이게함
        if self. hp>0:
            self.aframe+=1
        if self.aframe>=3:
            self.aframe=0
        if self.hp<0 and self.dframe<0:
            self.sound.play(1)
            self.dframe=0
        if self.dframe>=7:
            self.delobj=True
        else:
            if self.hp<=0:
                self.dframe+=1

    def Attack(self,p):
        if self.fireframe==0:

            self.sound1.play(1)
            main_state.playerbullet += [bullet(self.bulletimg, 8, p, main_state.Enemy, self.dm, self.x, self.y, 10, 400, 453, 25, 25,1)]
            if self.powershot == True:
                main_state.playerbullet += [
                    bullet(self.bulletimg, 8, [0, 10], main_state.Enemy, self.dm*2, self.x, self.y, 10, 145, 330, 25, 25)]

            p.threat+=self.dm
            self.fireframe+=1
        elif self.fireframe <self.fs:
            self.fireframe+=1
        else:
            self.fireframe=0

    def Dodge(self):
        self.d+=1
        if self.d<35:
            self.BoundR=0
            self.y+=3
        else:
            self.curState=self.STATE[0]
            self.threat=0
            self.BoundR = 30
            self.d=0

    def AI(self):
        ai = True  # 특정행동을 했으면 False로 바뀜

        for p in main_state.Enemy:
            x = p.x - self.x
            y = p.y - self.y
            l = math.sqrt(x * x + y * y)
            if l <= self.rg:
                self.Attack(p)
                ai = False
                break
        if self.threat > 50:  # 만약 어느정도 위험하다 생각되면
            self.curState = self.STATE[1]

        if self.curState==self.STATE[1]:# 회피상태가 오면 뒤로 회피 이때 무적
            self.Dodge()

        return ai


class Unit3:
    STATE = ['Attack', 'Defence']
    curState = 'Attack'
    threat=0
    d=0
    tdf=0
    image=None
    image2=None
    bulletimg=None
    hp=900+(store_state.Upgrade3*(100))#체력
    df=5+(store_state.Upgrade2*(5))#방어력
    dm=2+(store_state.Upgrade1*(1))#공격력
    sp=2#속도
    fs=50#발사속도
    rg=200#사거리
    BoundR=150
    fireframe=0
    delobj=False
    dframe=-1#피가 0일때 폭팔이미지
    bomb = None
    sound1 = None
    sound=None
    maxhp=hp
    hpbar=None
    powershot=True

    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.hp = 900 + (store_state.Upgrade3 * (100))  # 체력
        self.df = 5 + (store_state.Upgrade2 * (5))  # 방어력
        self.dm = 2 + (store_state.Upgrade1 * (1))  # 공격력
        self.tdf=self.df
        self.maxhp=self.hp

        if Unit3.image==None:
            Unit3.image =load_image('Unit3.png')
            Unit3.bulletimg=load_image('EnemyBullet.png')
            Unit3.bomb=load_image('bomb.png')
            Unit3.image2=load_image('Unit3_s.png')
            Unit3.sound1=load_wav('laser4.wav')
            Unit3.sound1.set_volume(20)
            Unit3.sound = load_wav('boom.wav')
            Unit3.sound.set_volume(25)
            Unit3.hpbar=load_image('hpbar.png')

    def Draw(self):
        self.hpbar.draw(self.x, self.y + 85, 100 * self.hp / self.maxhp, 30)
        if self.hp>0:
            self.image.draw(self.x, self.y + 20,150,100)
            if self.curState==self.STATE[1]:
                self.image2.draw(self.x,self.y+20,150,100)
        else:
            self.bomb.clip_draw(self.dframe*95,0,95,70,self.x,self.y,150,150)

    def Update(self):
        if self.AI() == True and self.y<=600:  # 아무행동도 안했으면
            self.y += self.sp  # 움직이게함
        if self.hp<0 and self.dframe<0:
            self.sound.play(1)
            self.dframe=0
        if self.dframe>=7:
            self.delobj=True
        else:
            if self.hp<=0:
                self.dframe+=1

    def Attack(self,p):
        if self.fireframe==0:
            self.sound1.play(1)

            main_state.playerbullet+=[bullet(self.bulletimg,8,p,main_state.Enemy,self.dm,self.x,self.y,10,85, 303, 25,25)]
            if self.powershot==True:
                main_state.playerbullet += [
                    bullet(self.bulletimg, 8, [-2, 6], main_state.Enemy, 1, self.x, self.y, 10, 85, 303, 25, 25)]
                main_state.playerbullet += [
                    bullet(self.bulletimg, 8, [2, 6], main_state.Enemy, 1, self.x, self.y, 10, 85, 303, 25, 25)]
                main_state.playerbullet += [
                    bullet(self.bulletimg, 8, [-4, 4], main_state.Enemy, 1, self.x, self.y, 10, 85, 303, 25, 25)]
                main_state.playerbullet += [
                    bullet(self.bulletimg, 8, [4, 4], main_state.Enemy, 1, self.x, self.y, 10, 85, 303, 25, 25)]
                main_state.playerbullet += [
                    bullet(self.bulletimg, 8, [-6, 2], main_state.Enemy, 1, self.x, self.y, 10, 85, 303, 25, 25)]
                main_state.playerbullet += [
                    bullet(self.bulletimg, 8, [6, 2], main_state.Enemy, 1, self.x, self.y, 10, 85, 303, 25, 25)]
                main_state.playerbullet += [
                    bullet(self.bulletimg, 8, [-6, 0], main_state.Enemy, 1, self.x, self.y, 10, 85, 303, 25, 25)]
                main_state.playerbullet += [
                    bullet(self.bulletimg, 8, [6, 0], main_state.Enemy, 1, self.x, self.y, 10, 85, 303, 25, 25)]
                main_state.playerbullet += [
                    bullet(self.bulletimg, 8, [-4, -2], main_state.Enemy, 1, self.x, self.y, 10, 85, 303, 25, 25)]
                main_state.playerbullet += [
                    bullet(self.bulletimg, 8, [4, -2], main_state.Enemy, 1, self.x, self.y, 10, 85, 303, 25, 25)]
                main_state.playerbullet += [
                    bullet(self.bulletimg, 8, [-2, -4], main_state.Enemy, 1, self.x, self.y, 10, 85, 303, 25, 25)]
                main_state.playerbullet += [
                    bullet(self.bulletimg, 8, [2, -4], main_state.Enemy, 1, self.x, self.y, 10, 85, 303, 25, 25)]
                main_state.playerbullet += [
                    bullet(self.bulletimg, 8, [-4, -4], main_state.Enemy, 1, self.x, self.y, 10, 85, 303, 25, 25)]
                main_state.playerbullet += [
                    bullet(self.bulletimg, 8, [-4, -4], main_state.Enemy, 1, self.x, self.y, 10, 85, 303, 25, 25)]

            p.threat+=self.dm
            self.fireframe+=1
        elif self.fireframe <self.fs:
            self.fireframe+=1
        else:
            self.fireframe=0

    def Dodge(self):
        self.d+=1
        if self.d<60:
            self.df=100
        else:
            self.curState=self.STATE[0]
            self.threat=0
            self.d=0
            self.df=self.tdf

    def AI(self):
        ai = True  # 특정행동을 했으면 False로 바뀜

        for p in main_state.Enemy:
            x = p.x - self.x
            y = p.y - self.y
            l = math.sqrt(x * x + y * y)
            if l <= self.rg:
                self.Attack(p)
                ai = False
        if self.threat > 100:  # 만약 어느정도 위험하다 생각되면
            self.curState = self.STATE[1]

        if self.curState==self.STATE[1]:# 회피상태가 오면 방어력증가
            self.Dodge()

        return ai





class Boss1:
    STATE = ['Attack1', 'Attack2']
    phase=0
    curState=STATE[0]
    threat=0
    image=None
    bulletimg=None
    hp=3000#체력
    df=2#방어력
    dm=13#공격력
    sp=2#속도
    fs=30#발사속도
    bomb = None
    maxhp=hp
    hpbar=None
    fireframe=0
    BoundR=60
    delobj=False
    def __init__(self):
        self.dframe=-1
        self.x=800
        self.y=1000

        if Boss1.image==None:
            Boss1.image =load_image('boss1_p1.png')
            Boss1.bulletimg=load_image('EnemyBullet.png')
            Boss1.bomb=load_image('bomb.png')
            Boss1.hpbar=load_image('hpbar.png')


    def Draw(self):
        self.hpbar.draw(self.x, self.y + 165, 130 * self.hp / self.maxhp, 30)
        if self.hp>0:
            self.image.draw(self.x, self.y)
        else:
            self.bomb.clip_draw(self.dframe*95,0,95,70,self.x,self.y)

        if self.phase==2:
            self.bomb.clip_draw(self.dframe*95,0,95,70,self.x-20,self.y)
            self.bomb.clip_draw(self.dframe*95,0,95,70,self.x+20,self.y)



    def Update(self):
        if self.y>600:
            self.y-=self.sp#움직이게함
        else:
            self.y=600

        if self.phase==2 and self.dframe<0:
            self.dframe=0
        if self.dframe>=7 and self.phase==2:
            self.dframe=-1
            self.phase=3
        elif self.phase==2 and self.dframe<7:
            self.dframe+=1

        if self.hp <=0  and self.dframe < 0:
            self.dframe = 0

        if self.dframe >= 7 and self.hp<=0:
            self.delobj = True
            main_state.Enemy.clear()

        elif self.hp<=0 and self.dframe<7:
            self.dframe += 1

        self.AI()


    def Attack(self,p):
        if self.fireframe==0:
            if self.curState=='Attack1':
                main_state.Enemybullet+=[bullet(self.bulletimg,5,p,main_state.player,self.dm,self.x,self.y,10,170, 303, 25, 25)]
                main_state.Enemybullet += [
                    bullet(self.bulletimg, 10, [-4,-4], main_state.player, self.dm, self.x, self.y, 10, 170, 303, 25, 25)]
                main_state.Enemybullet += [
                    bullet(self.bulletimg, 10, [4,-4], main_state.player, self.dm, self.x, self.y, 10, 170, 303, 25, 25)]
                main_state.Enemybullet += [bullet(self.bulletimg, 15, p, main_state.player, self.dm, self.x, self.y, 10, 170, 303, 25, 25)]
                p.threat+=self.dm
                self.fireframe+=1
            elif self.curState=='Attack2':
                main_state.Enemybullet += [bullet(self.bulletimg, 10, p, main_state.player, self.dm, self.x, self.y, 10, 170, 303, 25, 25)]
                main_state.Enemybullet += [
                    bullet(self.bulletimg, 10, [0,-5], main_state.player, self.dm, self.x, self.y, 10, 170, 303, 25, 25)]
                main_state.Enemybullet += [
                    bullet(self.bulletimg, 10, [-3,-2], main_state.player, self.dm, self.x, self.y, 10, 170, 303, 25, 25)]
                main_state.Enemybullet += [
                    bullet(self.bulletimg, 10, [3,-2], main_state.player, self.dm, self.x, self.y, 10, 170, 303, 25, 25)]
                main_state.Enemybullet += [
                    bullet(self.bulletimg,10, [4,-1], main_state.player, self.dm, self.x, self.y, 10, 170, 303, 25, 25)]
                main_state.Enemybullet += [
                    bullet(self.bulletimg, 10,[-4,-1],  main_state.player, self.dm, self.x, self.y, 10, 170, 303, 25, 25)]
                main_state.Enemybullet += [
                    bullet(self.bulletimg, 10, [-2,-2], main_state.player, self.dm, self.x, self.y, 10, 170, 303, 25, 25)]
                main_state.Enemybullet += [
                    bullet(self.bulletimg, 10, [2,-2], main_state.player, self.dm, self.x, self.y, 10, 170, 303, 25, 25)]

                main_state.Enemybullet += [bullet(self.bulletimg, 15, p, main_state.player, self.dm, self.x, self.y, 10, 170, 303, 25, 25)]
                p.threat += self.dm
                self.fireframe += 1
        elif self.fireframe <self.fs:
            self.fireframe+=1
        else:
            self.fireframe=0

    def AI(self):

        if len(main_state.player)>0:
            self.Attack(main_state.player[0])
        if self.hp<1000 and self.phase==0:
            self.phase=1
        if self.phase==1:
            self.image = load_image('boss1_p2.png')
            main_state.Enemy += [Enemy1(i+1) for i in range(20)]
            main_state.Enemy += [Enemy2(i+1) for i in range(5)]
            self.phase=2
            self.curState=self.STATE[1]


class Boss2:
    STATE = ['Attack1', 'Attack2']
    phase=0
    curState=STATE[0]
    threat=0
    image=None
    bulletimg=None
    hp=8000#체력
    df=5#방어력
    dm=25#공격력
    sp=3#속도
    fs=18#발사속도
    a=0
    bomb = None
    r=7
    fireframe=0
    BoundR=60
    maxhp=hp
    hpbar=None
    delobj=False
    def __init__(self):
        self.dframe=-1
        self.x=800
        self.y=1000
        if Boss2.image==None:
            Boss2.image =load_image('boss2_1.png')
            Boss2.bulletimg=load_image('EnemyBullet.png')
            Boss2.bomb=load_image('bomb.png')
            Boss2.hpbar=load_image('hpbar.png')


    def Draw(self):

        if self.hp>0:
            self.image.draw(self.x, self.y)

        else:
            self.bomb.clip_draw(self.dframe*95,0,95,70,self.x,self.y)

        if self.phase==1:
            self.hpbar.draw(self.x, self.y - 220, 160 * self.hp / self.maxhp, 30)
        else:
            self.hpbar.draw(self.x, self.y - 120, 160 * self.hp / self.maxhp, 30)

        if self.phase==2:
            self.bomb.clip_draw(self.dframe*95,0,95,70,self.x-20,self.y)
            self.bomb.clip_draw(self.dframe*95,0,95,70,self.x+20,self.y)





    def Update(self):
        if self.y>600:
            self.y-=self.sp#움직이게함
        else:
            self.y=600





        if self.phase==2 and self.dframe<0:
            self.dframe=0
        if self.dframe>=7 and self.phase==2:
            self.dframe=-1
            self.phase=3
        elif self.phase==2 and self.dframe<7:
            self.dframe+=1

        if self.hp <=0  and self.dframe < 0:
            self.dframe = 0

        if self.dframe >= 7 and self.hp<=0:
            self.delobj = True
            main_state.Enemy.clear()

        elif self.hp<=0 and self.dframe<7:
            self.dframe += 1

        self.AI()


    def Attack(self,p):
        if self.fireframe==0:
            if self.r<=7:
                self.r-=1
            if self.r == -7:
                self.r = 7
            if self.curState=='Attack1':
                main_state.Enemybullet+=[bullet(self.bulletimg,2,p,main_state.player,self.dm,self.x,self.y,10,170, 303, 25, 25,3)]
                main_state.Enemybullet += [bullet(self.bulletimg, 1, p, main_state.player, self.dm, self.x, self.y, 10, 170, 303, 25, 25,3)]
                main_state.Enemybullet+=[bullet(self.bulletimg,3,[0,-4], main_state.player,self.dm,self.x,self.y,10,170,303,25,25)]
                main_state.Enemybullet += [bullet(self.bulletimg, 23, [self.r, -4], main_state.player, self.dm, self.x, self.y, 10, 170, 303, 25, 25)]
                main_state.Enemybullet += [bullet(self.bulletimg, 23, [-self.r, -4], main_state.player, self.dm, self.x, self.y, 10, 170, 303, 25, 25)]

                p.threat+=self.dm
                self.fireframe+=1
            elif self.curState=='Attack2':
                main_state.Enemybullet += [
                    bullet(self.bulletimg, 2, p, main_state.player, self.dm, self.x, self.y, 10, 170, 303, 25, 25, 3)]
                main_state.Enemybullet += [
                    bullet(self.bulletimg, 1, p, main_state.player, self.dm, self.x, self.y, 10, 170, 303, 25, 25, 3)]
                main_state.Enemybullet += [
                    bullet(self.bulletimg, 3, [0, -4], main_state.player, self.dm, self.x, self.y, 10, 170, 303, 25,
                           25)]
                main_state.Enemybullet += [
                    bullet(self.bulletimg, 23, [self.r, -4], main_state.player, self.dm, self.x, self.y, 10, 170, 303,
                           25, 25)]
                main_state.Enemybullet += [
                    bullet(self.bulletimg, 23, [-self.r, -4], main_state.player, self.dm, self.x, self.y, 10, 170, 303,
                           25, 25)]

                main_state.Enemybullet += [
                    bullet(self.bulletimg, 10, [-2,-2], main_state.player, self.dm, self.x, self.y, 10, 170, 303, 25, 25)]
                main_state.Enemybullet += [
                    bullet(self.bulletimg, 10, [2,-2], main_state.player, self.dm, self.x, self.y, 10, 170, 303, 25, 25)]

                main_state.Enemybullet += [bullet(self.bulletimg, 15, p, main_state.player, self.dm, self.x, self.y, 10, 170, 303, 25, 25)]
                p.threat += self.dm
                self.fireframe += 1
        elif self.fireframe <self.fs:
            self.fireframe+=1
        else:
            self.fireframe=0

    def AI(self):

        if len(main_state.player)>0:
            self.Attack(main_state.player[0])
        if self.hp<3000 and self.phase==0:
            self.phase=1
        if self.phase==1:
            self.image = load_image('boss2_2.png')
            main_state.Enemy += [Enemy1(i+1) for i in range(20)]
            main_state.Enemy += [Enemy2(i+1) for i in range(5)]
            self.phase=2
            self.curState=self.STATE[1]




class Pilot:
    Left=0
    Right=1
    pattern1=0
    pattern2=0
    image=None
    bulletimg=None
    bulletimg2=None
    bulletimg3=None
    threat=0
    hp=150+(store_state.Upgrade3*(50))#체력
    maxhp=hp
    hpbar=None
    df=1+(store_state.Upgrade2*(3))#방어력
    dm=25+(store_state.Upgrade1*(1000))#공격력
    sp=6#속도
    fs=10#발사속도
    BoundR=17
    fireframe=0
    delobj=False
    frame=550
    dir=0
    sound1=None
    dodge=False
    dTick=0
    bomb=None
    sound2=None
    def __init__(self):
        self.hp = 150 + (store_state.Upgrade3 * (40))  # 체력
        self.df = 1 + (store_state.Upgrade2 * (3))  # 방어력
        self.dm = 25 + (store_state.Upgrade1 * (10))  # 공격력
        self.sp = 6  # 속도
        self.fs = 10  # 발사속도
        self.BoundR = 17
        self.maxhp=self.hp
        self.aframe=0;
        self.dframe=-1
        self.x=800
        self.y=0
        self.pattern1=store_state.pUpgrade1
        self.pattern2=store_state.pUpgrade2
        self.pattern3=store_state.pUpgrade3
        dTick=0
        dodge = False
        if Pilot.image==None:
            Pilot.image =load_image('Pilot.png')
            Pilot.bulletimg=load_image('EnemyBullet.png')
            Pilot.bomb = load_image('bomb.png')
            Pilot.bulletimg2=load_image('EnemyBullet2.png')
            Pilot.bulletimg3=load_image('bullet3.png')
            Pilot.sound1=load_wav('laser2.wav')

            Pilot.sound1.set_volume(65)
            Pilot.sound2=load_wav('laser3.wav')
            Pilot.sound2.set_volume(65)
            Pilot.hpbar=load_image('hpbar.png')

    def Draw(self):
        self.hpbar.draw(self.x-3, self.y + 75, 30 * self.hp / self.maxhp, 30)
        if self.hp>0:
            self.image.clip_draw(self.frame,0,48,52,self.x,self.y+40)

        else:
            self.bomb.clip_draw(self.dframe*95,0,95,70,self.x,self.y)


    def Dodge(self):
        if self.dir == self.Left:
            if self.frame>0:
                self.frame-=50
                self.BoundR=0
                self.x-=10
            else:
                self.frame=550
                self.dodge=False
                self.BoundR=30
        elif self.dir == self.Right:
            if self.frame<1100:
                self.frame+=50
                self.BoundR=0
                self.x+=10
            else:
                self.frame=550
                self.dodge=False
                self.BoundR=30


    def Update(self):

        if self.dodge==False:
            if len(main_state.xKey)!=0:
                if main_state.xKey[0]==0:
                    if self.x>10:
                        self.x -= self.sp
                    else:
                        self.x=10
                else:
                    if self.x<1580:
                        self.x += self.sp
                    else:
                        self.x=1580

        if len(main_state.yKey)!=0:
            if main_state.yKey[0]==0:
                self.y += self.sp
            else:
                if self.y>5:
                    self.y -= self.sp
                else:
                    self.y=5

        if self.hp>0:
            self.Attack(0)

        if self.hp<0 and self.dframe<0:
            self.dframe=0
        if self.dframe>=7:
            self.delobj=True
            main_state.End=True
        else:
            if self.hp<=0:
                self.dframe+=1

        if self.aframe>=3:
            self.aframe=0
        else:
            self.aframe+=1



        if self.dodge==True:
            if self.dTick==1:
                self.Dodge()
                self.dTick=0
            self.dTick+=1
        else:
            self.dTick = 0

    def Attack(self,p):
        if self.fireframe==0:
            self.sound1.play(1)

            main_state.playerbullet+=[bullet(self.bulletimg,16,p,main_state.Enemy,self.dm,self.x,self.y,10,85, 303, 25,25)]
            if self.pattern1>0:

                if len(main_state.Enemy)>0:
                    main_state.playerbullet += [bullet(self.bulletimg2, 16, main_state.Enemy[0], main_state.Enemy, self.dm/3, self.x, self.y, 10, 0, 0, 39,40,1)]
            if self.pattern2>0:
                self.sound1.play(1)
                if len(main_state.Enemy)>0:
                    main_state.playerbullet += [bullet(self.bulletimg, 13,[-1,4], main_state.Enemy, self.dm/5, self.x, self.y, 20,85, 303, 25,25,2)]
                    main_state.playerbullet += [bullet(self.bulletimg, 13,[1,4], main_state.Enemy, self.dm/5, self.x, self.y, 20,85, 303, 25,25,2)]
                    main_state.playerbullet += [bullet(self.bulletimg, 13,[2,3], main_state.Enemy, self.dm/5, self.x, self.y, 20,85, 303, 25,25,2)]
                    main_state.playerbullet += [bullet(self.bulletimg, 13,[-2,3], main_state.Enemy, self.dm/5, self.x, self.y, 20,85, 303, 25,25,2)]

            if self.pattern3>0:
                self.sound2.play(1)
                if len(main_state.Enemy)>0 and  random.randint(0,8)==2 :
                    main_state.playerbullet += [
                        bullet(self.bulletimg3, 25, p, main_state.Enemy, self.dm * 3, self.x, self.y, 50, 0, 0, 102,
                               156)]
            self.fireframe+=1
        elif self.fireframe <self.fs:
            self.fireframe+=1
        else:
            self.fireframe=0




##    def Dodge(self):
#        self.d+=1
#        if self.d<8:
#            self.x+=10
#           self.y-=3
#v       elif self.d>=8 and self.d<24:
#            self.x-=10
 #           self.y -= 3
  #      elif self.d>=24and self.d<32:
   #         self.x+=10
   #         self.y -= 3
   #     else:
   #         self.curState=self.STATE[0]
   #         self.threat=0
