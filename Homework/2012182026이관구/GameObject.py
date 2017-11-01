from pico2d import *
import random
import main_state
import game_framework
#   ----    모든 게임 오브젝트를 여기서 설계  ----

class Grass:  # 풀은 간단하게 그리기 기능만 가지며 이미지를 가지고 있음
    image=None
    def __init__(self):
        if Grass.image==None:
            Grass.image =load_image('grass.png')

    def get_bb(self):
        return 400 - 400, 30 - 25, 400 + 400, 30 + 25

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def Draw(self):
        self.image.draw(400, 30)
        self.draw_bb()


class boy:  # 소년은 위치와 이미지, 프레임을 가진다.
    image=None
    num=None
    totaltime=0

    LeftRun=0
    RightRun=1
    LeftStand=2
    RightStand=3
    duration=2

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

    def get_bb(self):
        return self.x - 20, self.y - 40, self.x + 20, self.y +40

    def draw_bb(self):
        draw_rectangle(*self.get_bb())

    def handleLeftRun(self):
        self.x-=100*game_framework.deltatime
        self.runframe+=game_framework.deltatime
        if self.x<0:
            self.x=0
            self.state=self.RightRun
        if self.runframe>=self.duration:
            self.duration=random.randint(1,5)
            self.state=self.LeftStand
            self.standframe=0
    def handleLeftStand(self):
        self.standframe+=game_framework.deltatime
        if self.standframe>=2:
            self.runframe=0
            self.state=self.LeftRun


    def handleRightRun(self):
        self.x += 100*game_framework.deltatime
        self.runframe += game_framework.deltatime
        if self.x > 800:
            self.x = 800
            self.state = self.LeftRun
        if self.runframe >= self.duration:
            self.duration = random.randint(1, 5)
            self.state = self.RightStand
            self.standframe = 0

    def handleRightStand(self):
        self.standframe += game_framework.deltatime
        if self.standframe >= 2:
            self.runframe = 0
            self.state = self.RightRun

    handlestate={LeftRun:handleLeftRun,RightRun:handleRightRun,LeftStand:handleLeftStand,RightStand:handleRightStand}

    def update(self):  # 업데이트 함수는 그리기와 매 프레임마다 처리해야할 행동(x축으로 2만큼 매프레임마다 이동)을 처리
        self.totaltime+=game_framework.deltatime
        if self.totaltime >= 0.05:
            self.frame = (self.frame + 1) % 8
            self.totaltime=0

        if self != main_state.player:
            self.handlestate[self.state](self)


    def Draw(self): # 그리기 함수
        self.image.clip_draw(self.frame * 100, self.state*100, 100, 100, self.x, self.y)
        self.draw_bb()




class ball:
    image=None
    speed=50

    def __init__(self,i):
        self.x = random.randint(100, 700)
        self.y = random.randint(400, 700)


        if ball.image==None:
            ball.image = load_image('ball21x21.png')


    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def draw_bb(self):
        draw_rectangle(*self.get_bb())


    def update(self):  # 업데이트 함수는 그리기와 매 프레임마다 처리해야할 행동(x축으로 2만큼 매프레임마다 이동)을 처리
        self.y-=game_framework.deltatime*self.speed
        self.speed+=40.8*game_framework.deltatime
        if self.speed>600:
            self.speed=600

    def Draw(self): # 그리기 함수

        self.image.draw(self.x,self.y)
        self.draw_bb()

