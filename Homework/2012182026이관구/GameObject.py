from pico2d import *
import random

#   ----    모든 게임 오브젝트를 여기서 설계  ----

class Grass:  # 풀은 간단하게 그리기 기능만 가지며 이미지를 가지고 있음
    image=None
    def __init__(self):
        if Grass.image==None:
            Grass.image =load_image('grass.png')

    def Draw(self):
        self.image.draw(400, 30)


class boy:  # 소년은 위치와 이미지, 프레임을 가진다.
    image=None
    num=None
    LeftRun=0
    RightRun=1
    LeftStand=2
    RightStand=3
    def __init__(self,i):
        self.x = random.randint(100, 700)
        self.y = random.randint(90, 200)
        self.frame = random.randint(0, 7)
        self.dir=1  #방향
        self.state=random.randint(0,3)
        self.num=i
        self.runframe=0
        self.standframe=0
        if boy.image==None:
            boy.image = load_image('animation_sheet.png')
    def handleLeftRun(self):
        self.x-=5
        self.runframe+=1
        if self.x<0:
            self.x=0
            self.state=self.RightRun
        if self.runframe==100:
            self.state=self.LeftStand
            self.standframe=0
    def handleLeftStand(self):
        self.standframe+=1
        if self.standframe==50:
            self.runframe=0
            self.state=self.LeftRun

    def handleRightRun(self):
        self.x += 5
        self.runframe += 1
        if self.x > 800:
            self.x = 800
            self.state = self.LeftRun
        if self.runframe == 100:
            self.state = self.RightStand
            self.standframe = 0

    def handleRightStand(self):
        self.standframe += 1
        if self.standframe == 50:
            self.runframe = 0
            self.state = self.RightRun

    handlestate={LeftRun:handleLeftRun,RightRun:handleRightRun,LeftStand:handleLeftStand,RightStand:handleRightStand}

    def update(self):  # 업데이트 함수는 그리기와 매 프레임마다 처리해야할 행동(x축으로 2만큼 매프레임마다 이동)을 처리
        self.frame = (self.frame + 1) % 8
        self.handlestate[self.state](self)


    def Draw(self): # 그리기 함수
        self.image.clip_draw(self.frame * 100, self.state*100, 100, 100, self.x, self.y)

