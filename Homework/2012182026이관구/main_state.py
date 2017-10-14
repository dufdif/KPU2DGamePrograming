from pico2d import *
import game_framework

from GameObject import *

# --- 설계된 모든 오브젝트를 직접 생성해서 사용하며 게임진행을 한다. ---





Boys = []
Font = None
player =None  # 플레이어로 선택된 녀석을 이용해 움직인다.


def handle_events():  # 플레이어의 좌표를 넘겨주고 새로운 좌표를 얻어옴
    events = get_events()
    global player
    global Boys
    for event in events:
        if event.type == SDL_KEYDOWN:  # F1~11까지 버튼을 누르면 각 소년 오브젝트를 조종할수 있다.
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_LEFT:#왼쪽 버튼을 누르면 1씩 감소
                n=player.num-1
                if n < 0:
                    n=0
                player = Boys[n]
            elif event.key == SDLK_RIGHT:#오른쪽 버튼을 누르면 1씩 증가
                n=player.num+1
                if n>999:
                    n=999
                player = Boys[n]
            elif event.key == SDLK_UP:#위쪽 버튼을 누르면 50씩 증가
                n=player.num+50
                if n>999:
                    n=999
                player = Boys[n]
            elif event.key == SDLK_DOWN:#아래쪽 버튼을 누르면 50씩 감소
                n=player.num-50
                if n<0:
                    n=0
                player = Boys[n]

        elif event.type == SDL_MOUSEMOTION:
            player.x, player.y = event.x, 600 - event.y



grass = None

def enter():
    global Boys
    global grass
    global player
    global Font
    Boys=[boy(i) for i in range(1000)]
    grass=Grass()
    player= Boys[0]
    Font=load_font('NANUMBARUNGOTHICBOLD.TTF',15)

def exit():
    global Boys
    global grass
    del grass
    del Boys

def update():
    global Boys
    for b in Boys:
        b.update()
def draw():#여기서 모든 객체를 그리고 모든 폰트를 그린다. 매우 중요한 상태의 드로우함수!
    clear_canvas()
    global Boys
    global grass
    global player
    for b in Boys:
        b.Draw()
    grass.Draw()
    Font.draw(0,580,'Character Number  :' + str(player.num+1))
    update_canvas()
    delay(0.025)
def pause(): pass
def resume(): pass