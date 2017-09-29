from pico2d import *
import game_framework

import random




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
    def Draw(self):
        self.image.clip_draw(self.frame * 100, 0, 100, 100, self.x, self.y)

Boys = []
player =None  # 플레이어로 선택된 녀석을 이용해 움직인다.


def handle_events():  # 플레이어의 좌표를 넘겨주고 새로운 좌표를 얻어옴
    events = get_events()
    global player
    global Boys
    for event in events:
        if event.type == SDL_KEYDOWN:  # F1~11까지 버튼을 누르면 각 소년 오브젝트를 조종할수 있다.
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_F1:
                player = Boys[0]
            elif event.key == SDLK_F2:
                player = Boys[1]
            elif event.key == SDLK_F3:
                player = Boys[2]
            elif event.key == SDLK_F4:
                player = Boys[3]
            elif event.key == SDLK_F5:
                player = Boys[4]
            elif event.key == SDLK_F6:
                player = Boys[5]
            elif event.key == SDLK_F7:
                player = Boys[6]
            elif event.key == SDLK_F8:
                player = Boys[7]
            elif event.key == SDLK_F9:
                player = Boys[8]
            elif event.key == SDLK_F10:
                player = Boys[9]
            elif event.key == SDLK_F11:
                player = Boys[10]
        elif event.type == SDL_MOUSEMOTION:
            player.x, player.y = event.x, 600 - event.y



grass = None

def enter():
    global Boys
    global grass
    global player
    Boys=[boy() for i in range(11)]
    grass=Grass()
    player= Boys[0]
def exit():
    global Boys
    global grass
    del grass
    del Boys

def update():
    global Boys
    for b in Boys:
        b.update()
def draw():
    clear_canvas()
    global Boys
    global grass
    for b in Boys:
        b.Draw()
    grass.Draw()
    update_canvas()
    delay(0.025)
def pause(): pass
def resume(): pass