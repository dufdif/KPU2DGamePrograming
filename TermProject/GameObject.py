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

        if self.y<0:
            self.delobj=True

        if self.y>800:
            self.delobj=True

        if self.pattern ==0:
            pass
        elif self.pattern==1:

            tx=self.lockon.x - self.x
            ty=self.lockon.y - self.y
            self.mx=tx
            self.my=ty

            self.mx *= self.sp * 1 / math.sqrt((tx) * (tx) + (ty) * (ty))
            self.my *= self.sp * 1 / math.sqrt((tx) * (tx) + (ty) * (ty))
            if self.lockon.delobj==True:
                self.delobj=True


        for p in self.lockonlist:
            x = p.x - self.x
            y = p.y - self.y
            l = math.sqrt(x * x + y * y)

            if p.BoundR==0:
                pass
            else:
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
    rg=270#사거리
    fireframe=0
    BoundR=60
    delobj=False
    dframe=-1#피가 0일때 폭팔이미지
    bomb = None

    def __init__(self,i):
        self.dframe=-1
        self.wave=i
        self.x=800+random.randint(-450,450)
        self.y=600+random.randint(-50,55)+self.wave*400
        if Enemy1.image==None:
            Enemy1.image =load_image('Enemy12.png')
            Enemy1.bulletimg=load_image('EnemyBullet.png')
            Enemy1.bomb=load_image('bomb.png')



    def Draw(self):
        if self.hp>0:
            self.image.clip_draw(150,265,130,100,self.x,self.y)
        else:
            self.bomb.clip_draw(self.dframe*95,0,95,70,self.x,self.y)

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
    dframe=-1#피가 0일때 폭팔이미지
    bomb = None

    def __init__(self,i):
        self.wave=i
        self.x=800+random.randint(-450,450)
        self.y=600+random.randint(-50,55)+self.wave*400
        if Enemy2.image==None:
            Enemy2.image =load_image('Enemy2.png')
            Enemy2.bulletimg=load_image('EnemyBullet.png')
            Enemy2.bomb=load_image('bomb.png')

    def Draw(self):
        if self.hp>0:
            self.image.draw(self.x, self.y)
        else:
            self.bomb.clip_draw(self.dframe*95,0,95,70,self.x,self.y)


    def Update(self):
        if self.AI()==True:#아무행동도 안했으면
            self.y-=self.sp#움직이게함
        if self.hp<0 and self.dframe<0:
            self.dframe=0
        if self.dframe>=7:
            self.delobj=True
        else:
            if self.hp<=0:
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
    rg=300#사거리
    BoundR=60
    fireframe=0
    delobj=False
    dframe=-1#피가 0일때 폭팔이미지
    bomb = None

    def __init__(self,x,y):
        self.x=x
        self.y=y
        if Unit1.image==None:
            Unit1.image =load_image('Unit1.png')
            Unit1.bulletimg=load_image('EnemyBullet.png')
            Unit1.bomb=load_image('bomb.png')

    def Draw(self):
        if self.hp>0:
            self.image.draw(self.x, self.y + 40)
        else:
            self.bomb.clip_draw(self.dframe*95,0,95,70,self.x,self.y)

    def Update(self):
        if self.AI() == True:  # 아무행동도 안했으면
            self.y += self.sp  # 움직이게함
        if self.hp<0 and self.dframe<0:
            self.dframe=0
        if self.dframe>=7:
            self.delobj=True
        else:
            if self.hp<=0:
                self.dframe+=1

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
    hp=70+(store_state.Upgrade3*(25))#체력
    df=0+(store_state.Upgrade2*(1))#방어력
    dm=50+(store_state.Upgrade1*(30))#공격력
    sp=2#속도
    fs=200-(store_state.Upgrade4*(1))#발사속도
    rg=650#사거리
    BoundR=60
    fireframe=0
    delobj=False
    dframe=-1#피가 0일때 폭팔이미지
    bomb = None


    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.aframe=0
        if Unit2.image==None:
            Unit2.image =load_image('Unit2.png')
            Unit2.bulletimg=load_image('EnemyBullet.png')
            Unit2.bomb=load_image('bomb.png')

    def Draw(self):
        if self.hp>0:
            self.image.clip_draw(self.aframe*80,0,80,101,self.x, self.y + 40)
        else:
            self.bomb.clip_draw(self.dframe*95,0,95,70,self.x,self.y)

    def Update(self):
        if self.AI() == True:  # 아무행동도 안했으면
            self.y += self.sp  # 움직이게함
        if self. hp>0:
            self.aframe+=1
        if self.aframe>=3:
            self.aframe=0
        if self.hp<0 and self.dframe<0:
            self.dframe=0
        if self.dframe>=7:
            self.delobj=True
        else:
            if self.hp<=0:
                self.dframe+=1

    def Attack(self,p):
        if self.fireframe==0:
            main_state.playerbullet += [bullet(self.bulletimg, 8, p, main_state.Enemy, self.dm, self.x, self.y, 10, 400, 453, 25, 25,1)]
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
            self.y-=3
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
        if self.threat > 40:  # 만약 어느정도 위험하다 생각되면
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
    hp=500+(store_state.Upgrade3*(25))#체력
    df=3+(store_state.Upgrade2*(5))#방어력
    dm=1+(store_state.Upgrade1*(1))#공격력
    sp=3#속도
    fs=50-(store_state.Upgrade4*(5))#발사속도
    rg=250#사거리
    BoundR=130
    fireframe=0
    delobj=False
    dframe=-1#피가 0일때 폭팔이미지
    bomb = None

    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.tdf=self.df
        if Unit3.image==None:
            Unit3.image =load_image('Unit3.png')
            Unit3.bulletimg=load_image('EnemyBullet.png')
            Unit3.bomb=load_image('bomb.png')
            Unit3.image2=load_image('Unit3_s.png')

    def Draw(self):
        if self.hp>0:
            self.image.draw(self.x, self.y + 50)
            if self.curState==self.STATE[1]:
                self.image2.draw(self.x,self.y+50)
        else:
            self.bomb.clip_draw(self.dframe*95,0,95,70,self.x,self.y)

    def Update(self):
        if self.AI() == True:  # 아무행동도 안했으면
            self.y += self.sp  # 움직이게함
        if self.hp<0 and self.dframe<0:
            self.dframe=0
        if self.dframe>=7:
            self.delobj=True
        else:
            if self.hp<=0:
                self.dframe+=1

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
    hp=2000#체력
    df=0#방어력
    dm=10#공격력
    sp=2#속도
    fs=30#발사속도

    fireframe=0
    BoundR=60
    delobj=False
    def __init__(self):

        self.x=800
        self.y=1000
        if Boss1.image==None:
            Boss1.image =load_image('boss1_p1.png')
            Boss1.bulletimg=load_image('EnemyBullet.png')

    def Draw(self):
        self.image.draw(self.x,self.y)


    def Update(self):
        if self.y>600:
            self.y-=self.sp#움직이게함
        else:
            self.y=600
        if self.hp<0:
            self.delobj=True
            main_state.Enemy.clear()

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

class Pilot:
    Left=0
    Right=1
    pattern1=0
    image=None
    bulletimg=None
    threat=0
    hp=150+(store_state.Upgrade3*(25))#체력
    df=1+(store_state.Upgrade2*(1))#방어력
    dm=25+(store_state.Upgrade1*(3))#공격력
    sp=6#속도
    fs=10#발사속도
    BoundR=30
    fireframe=0
    delobj=False
    frame=550
    dir=0
    dodge=False
    dTick=0

    def __init__(self):
        self.x=800
        self.y=0
        self.pattern1=store_state.pUpgrade1
        dTick=0
        dodge = False
        if Pilot.image==None:
            Pilot.image =load_image('Pilot.png')
            Pilot.bulletimg=load_image('EnemyBullet.png')

    def Draw(self):
        self.image.clip_draw(self.frame,0,48,52,self.x,self.y+40)

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
                    self.x -= self.sp
                else:
                    self.x += self.sp

        if len(main_state.yKey)!=0:
            if main_state.yKey[0]==0:
                self.y += self.sp
            else:
                self.y -= self.sp

        if self.hp<0:
            self.delobj=True
        else:
            self.Attack(0)

        if self.dodge==True:
            if self.dTick==1:
                self.Dodge()
                self.dTick=0
            self.dTick+=1
        else:
            self.dTick = 0

    def Attack(self,p):
        if self.fireframe==0:

            main_state.playerbullet+=[bullet(self.bulletimg,16,p,main_state.Enemy,self.dm,self.x,self.y,10,85, 303, 25,25)]
            if self.pattern1>0:
                if len(main_state.Enemy)>0:
                    main_state.playerbullet += [bullet(self.bulletimg, 16, main_state.Enemy[0], main_state.Enemy, self.dm/3, self.x, self.y, 10, 85, 303, 25, 25,1)]

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
