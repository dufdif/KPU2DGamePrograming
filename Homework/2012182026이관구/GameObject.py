from pico2d import *
import random

#   ----    모든 게임 오브젝트를 여기서 설계  ----


class Grass:  # 풀은 간단하게 그리기 기능만 가지며 이미지를 가지고 있음
    def __init__(self):
        self.image = load_image('grass.png')

    def Draw(self):
        self.image.draw(400, 30)


class boy:  # 소년은 위치와 이미지, 프레임을 가진다.
    def __init__(self):
        self.x = random.randint(100, 700)
        self.y = random.randint(90, 200)
        self.frame = random.randint(0, 7)
        self.image = load_image('run_animation.png')

    def update(self):  # 업데이트 함수는 그리기와 매 프레임마다 처리해야할 행동(x축으로 2만큼 매프레임마다 이동)을 처리
        self.frame = (self.frame + 1) % 8
        self.x += 2
        if self.x >= 800:
            self.x = 0
    def Draw(self): # 그리기 함수
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)