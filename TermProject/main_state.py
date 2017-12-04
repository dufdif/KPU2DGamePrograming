from pico2d import *
import game_framework

from GameObject import *

# --- 설계된 모든 오브젝트를 직접 생성해서 사용하며 게임진행을 한다. ---

import end_state


End=False

End_time=0

Font = None
player =None
Enemy = None
playerbullet=None
Enemybullet=None
Bg=None
Bg2=None

ui1 =None
ui2 =None
ui3 =None

bgy=0
bgy2=0

stageClear=False
stage = 1
stageEnemy1={1:15,2:25,3:35,4:40}#스테이지별 적1 의 갯수
stageEnemy2={1:7,2:15,3:10,4:20}#스테이지별 적2의 갯수
stageEnemy3={1:3,2:3,3:8,4:5}#스테이지별 적2의 갯수

type=None
# 유닛별로 재고가 있음. 이 재고를 다떨어지면 생성불가.
numUnit1=0
numUnit2=0
numUnit3=0

xKey=[]
yKey=[]

mousex=0
mousey=0

def handle_events():  # F1~5까지 누르면 유닛선택
    events = get_events()
    global player
    global stage
    global type
    global numUnit1
    global numUnit2
    global numUnit3
    global xKey
    global yKey
    global mousex
    global mousey
    if stage%2 == 1:
        for event in events:

            if event.type == SDL_KEYDOWN:
                if event.key == SDLK_ESCAPE:
                    game_framework.quit()
                elif event.key==SDLK_F1:
                    if type != 1:
                        type=1

                    else:
                        type=None
                elif event.key==SDLK_F2:
                    if type != 2:
                        type=2
                    else:
                        type=None
                elif event.key == SDLK_F3:
                    if type != 3:
                        type = 3
                    else:
                        type = None

            elif event.type == SDL_MOUSEMOTION:
                mousex = event.x
                mousey = 800 - event.y



            elif event.type == SDL_MOUSEBUTTONDOWN:#누르면 그곳에 생성 단 Y는 한계선을 둠.
                if type == 1:
                    if numUnit1>0:
                        maxY=800 - event.y
                        if maxY >= 200:
                            maxY=200
                        player+=[Unit1(event.x,maxY)]
                        numUnit1-=1
                elif type == 2:
                    if numUnit2>0:
                        maxY=800 - event.y
                        if maxY >= 200:
                            maxY=200
                        player+=[Unit2(event.x,maxY)]
                        numUnit2-=1
                elif type == 3:
                    if numUnit3>0:
                        maxY=800 - event.y
                        if maxY >= 200:
                            maxY=200
                        player+=[Unit3(event.x,maxY)]
                        numUnit3-=1


    else:
        hide_cursor()
        if len(player)>0:
            for event in events:
                if event.type == SDL_KEYDOWN:
                    if event.key == SDLK_ESCAPE:
                        game_framework.quit()
                    elif event.key==SDLK_LEFT:
                        xKey+=[0]
                    elif event.key==SDLK_RIGHT:
                        xKey+=[1]

                    elif event.key == SDLK_UP:
                        yKey += [0]
                    elif event.key == SDLK_DOWN:
                        yKey+=[1]
                    elif event.key == SDLK_z:
                        player[0].dir = player[0].Left
                        player[0].dodge=True
                    elif event.key == SDLK_x:
                        player[0].dir = player[0].Right
                        player[0].dodge = True
                elif event.type == SDL_KEYUP:
                    if event.key == SDLK_LEFT:
                        if len(xKey)>0:
                            xKey.remove(0)
                    elif event.key == SDLK_RIGHT:
                        if len(xKey) > 0:
                            xKey.remove(1)
                    elif event.key == SDLK_UP:
                        if len(yKey) > 0:
                            yKey.remove(0)
                    elif event.key == SDLK_DOWN:
                        if len(yKey) > 0:
                            yKey.remove(1)


                    #elif event.type==SDL_MOUSEMOTION:
                #player[0].x,player[0].y=event.x,800-event.y
            #elif event.type == SDL_MOUSEBUTTONDOWN:
            #    if event.button == SDL_BUTTON_LEFT:
            #        player[0].dir=player[0].Left
            #        player[0].dodge=True
            #    else:
            #        player[0].dir = player[0].Right
            #        player[0].dodge = True


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
        Enemy+=[Enemy1(1) for i in range(3)]
        Enemy += [Enemy1(2) for i in range(5)]
        Enemy += [Enemy2(2) for i in range(2)]



        Enemy += [Enemy1(5) for i in range(2)]
        Enemy += [Enemy2(4) for i in range(2)]
        Enemy += [Enemy2(5) for i in range(1)]

        Enemy += [Enemy3(1) for i in range(3)]

    elif stage ==2:
        player+=[Pilot()]
        Enemy+=[Boss1()]
    elif stage == 3:
        Enemy += [Enemy1(1) for i in range(15)]
        Enemy += [Enemy3(2) for i in range(3)]

        Enemy += [Enemy1(4) for i in range(7)]
        Enemy += [Enemy2(4) for i in range(10)]

        Enemy += [Enemy1(8) for i in range(15)]
        Enemy += [Enemy3(8) for i in range(5)]
    elif stage ==4:
        player+=[Pilot()]
        Enemy+=[Boss2()]


def enter():
    global End_time
    global xKey
    global yKey
    global player
    global Font
    global Enemy
    global stageClear
    global playerbullet
    global Enemybullet
    global type
    global Bg
    global Bg2
    global bgy
    global ui1
    global ui2
    global ui3

    ui1=load_image('Unit1.png')
    ui2=load_image('Unit2.png')
    ui3=load_image('Unit3.png')
    bgy=0

    Bg=load_image('bg.jpg')
    Bg2=load_image('bg2.jpg')
    type=None
    xKey = []
    yKey = []

    player = []
    Enemy = []
    playerbullet = []
    Enemybullet = []
    stageClear=False
    CreateStage()
    Font=load_font('NANUMBARUNGOTHICBOLD.TTF',15)

    End_time = 0

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
    global Bg2
    del Bg
    del Bg2


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
    global End_time
    global End
    global numUnit1
    global numUnit2
    global numUnit3
    global bgy
    DelObject()

    if bgy>-7220:
        bgy-=10
    else:
        bgy=0

    if len(Enemy)>0 and (len(player)==0 and numUnit1<=0 and numUnit2<=0 and numUnit3<=0 ): #유닛도없고 적들만 있으면
        End=True

    if stage%2==1:
        for e in Enemy:
            if e.y<-100 :
                End=True

    if stage==5:
        End=True

    if End==True:
        if End_time > 1.5:
            game_framework.change_state(end_state)
            End_time = 0

        else:
            End_time += 0.025

    else:
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
        if stageClear==True:
            if End_time>2:
                game_framework.change_state(store_state)
                End_time=0
            else:
                End_time+=0.025




def draw():#여기서 모든 객체를 그리고 모든 폰트를 그린다. 매우 중요한 상태의 드로우함수!
    clear_canvas()
    global player
    global Enemy
    global Enemybullet
    global playerbullet
    global Bg
    global Bg2
    global bgy
    global ui1
    global ui2
    global ui3
    global Font
    global mousex
    global mousey
    global type

    Bg.draw(800,400+bgy)
    Bg2.draw(800,6820+bgy)

    for e in Enemy:
        e.Draw()

    for p in player:
        p.Draw()

    for eb in Enemybullet:
        eb.Draw()

    for pb in playerbullet:
        pb.Draw()


    if stage%2==1:

        if type==1:
            ui1.draw(mousex,mousey,20,20)
        elif type==2:
            ui2.clip_draw(0,0,80,101,mousex,mousey,20,20)
        elif type==3:
            ui3.draw(mousex,mousey,20,20)


        ui1.draw(50,100,40,40)

        Font.draw(50,50,str(numUnit1),color=[255,255,255])
        ui2.clip_draw(0,0,80,101,90,100,40,40)
        Font.draw(90, 50, str(numUnit2), color=[255, 255, 255])
        ui3.draw(130, 100, 40, 40)
        Font.draw(130, 50, str(numUnit3), color=[255, 255, 255])

    update_canvas()
    delay(0.025)



def pause(): pass
def resume(): pass