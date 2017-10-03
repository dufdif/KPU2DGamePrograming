from pico2d import *
import game_framework

from GameObject import *

# --- 설계된 모든 오브젝트를 직접 생성해서 사용하며 게임진행을 한다. ---





Font = None
player =None
Enemy = None
playerbullet=None
Enemybullet=None
Bg=None
stageClear=False
stage = 1
stageEnemy1={1:22,2:30,3:40}#스테이지별 적1 의 갯수
stageEnemy2={1:0,2:5,3:10}#스테이지별 적2의 갯수

type=None
# 유닛별로 재고가 있음. 이 재고를 다떨어지면 생성불가.
numUnit1=0
numUnit2=0

def handle_events():  # F1~5까지 누르면 유닛선택
    events = get_events()
    global player
    global type
    global numUnit1
    global numUnit2

    for event in events:
        if event.type == SDL_KEYDOWN:  # F1~11까지 버튼을 누르면 각 소년 오브젝트를 조종할수 있다.
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key==SDLK_F1:
                if type != 1:
                    type=1
                else:
                    type=None
      #  elif event.type==SDLK_F2:
      #      type=2

        elif event.type == SDL_MOUSEBUTTONDOWN:#누르면 그곳에 생성 단 Y는 한계선을 둠.
            if type == 1:
                if numUnit1>0:
                    maxY=800 - event.y
                    if maxY >= 200:
                        maxY=200
                    player+=[Unit1(event.x,maxY)]
                    numUnit1-=1


#여기서 하는일 1. 아군유닛과 적군유닛을 먼저 제거. 2. 스테이지에 맞게 적군 유닛을 생성해둠
def CreateStage():
    global Enemy
    global stage
    global player
    global Enemybullet
    global playerbullet

    Enemy.clear()
    player.clear()
    Enemybullet.clear()
    playerbullet.clear()

    if stage == 1:
        Enemy+=[Enemy1(1) for i in range(11)]
        Enemy += [Enemy1(2) for i in range(11)]
    elif stage == 2:
        Enemy += [Enemy1(1) for i in range(10)]
        Enemy += [Enemy1(2) for i in range(10)]
        Enemy += [Enemy2(2) for i in range(5)]

        Enemy += [Enemy1(3) for i in range(10)]


def enter():
    global player
    global Font
    global Enemy
    global stageClear
    global playerbullet
    global Enemybullet
    global type
    global Bg
    #Bg=load_image()
    type=None
    player = []
    Enemy = []
    playerbullet = []
    Enemybullet = []
    stageClear=False
    CreateStage()
    Font=load_font('NANUMBARUNGOTHICBOLD.TTF',15)

def exit():
    global Enemy
    del Enemy
    global player
    del player
    global Enemybullet
    del Enemybullet
    global playerbullet
    del playerbullet
    global Bg
    del Bg
def DelObject():#지워야 할 오브젝트를 지우는 녀석.
    global Enemy
    global player
    global Enemybullet
    global playerbullet

    n=0
    for eb in Enemybullet:
        if eb.delobj==True:
            Enemybullet.pop(n)
            del eb
            n-=1
        n+=1

    n = 0
    for pb in playerbullet:
        if pb.delobj == True:
            playerbullet.pop(n)
            del pb
            n -= 1
        n += 1

    n = 0
    for e in Enemy:
        if e.delobj == True:
            Enemy.pop(n)
            del e
            n -= 1
        n += 1

    n = 0
    for p in player:
        if p.delobj == True:
            player.pop(n)
            del p
            n -= 1
        n += 1


def update():
    global Enemy
    global player
    global Enemybullet
    global playerbullet
    global stageClear
    global stage
    DelObject()

    for e in Enemy:
        e.Update()
    for p in player:
        p.Update()

    for eb in Enemybullet:
        eb.Update()
    for pb in playerbullet:
        pb.Update()

    if len(Enemy)==0 and stageClear==False:
        stageClear=True
        stage+=1
        game_framework.change_state(store_state)


def draw():#여기서 모든 객체를 그리고 모든 폰트를 그린다. 매우 중요한 상태의 드로우함수!
    clear_canvas()
    global player
    global Enemy
    global Enemybullet
    global playerbullet

    for e in Enemy:
        e.Draw()

    for p in player:
        p.Draw()

    for eb in Enemybullet:
        eb.Draw()

    for pb in playerbullet:
        pb.Draw()

    update_canvas()
    delay(0.025)



def pause(): pass
def resume(): pass