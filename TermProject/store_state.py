from pico2d import*
import main_state
import GameObject
import game_framework

name = "StoreState"
image = None
font = None
gold = 0

Upgrade1=0
Upgrade2=0
Upgrade3=0
Upgrade4=0


def enter():
    show_cursor()
    global image
    global font
    image = load_image('storebg.png')
    font = load_font('NANUMBARUNGOTHICBOLD.TTF',40)
    global gold
    gold += 500 + main_state.stage*1000

def exit():
    global image
    global font

    del(image)
    del font


def handle_events():
    global gold
    global Upgrade1
    global Upgrade2
    global Upgrade3
    global Upgrade4

    events = get_events()
    for event in events:
        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
            game_framework.change_state(main_state)
        elif event.type == SDL_MOUSEBUTTONDOWN:
            if event.x>=60 and event.x<350 and event.y >= 225 and event.y<310:#  유닛1 생성
                if gold>=100:
                    main_state.numUnit1+=1
                    gold-=100


            elif event.x>=435 and event.x<620 and event.y >= 225 and event.y<310:#  업그레이드 1
                if gold>=500*(Upgrade1+1):
                    gold-=500*(Upgrade1+1)
                    Upgrade1+=1
            elif event.x>=435 and event.x<620 and event.y >= 365 and event.y<450:#  업그레이드 2
                if gold>=500*(Upgrade2+1):
                    gold-=500*(Upgrade2+1)
                    Upgrade2+=1
            elif event.x>=435 and event.x<620 and event.y >= 405 and event.y<590:#  업그레이드 3
                if gold>=500*(Upgrade3+1):
                    gold-=500*(Upgrade3+1)
                    Upgrade3+=1
            elif event.x>=435 and event.x<620 and event.y >= 445 and event.y<730:#  업그레이드 4
                if gold>=500*(Upgrade4+1):
                    gold-=500*(Upgrade4+1)
                    Upgrade4+=1



def draw():
    global image
    global font
    global gold
    global Upgrade1
    global Upgrade2
    global Upgrade3
    global Upgrade4

    clear_canvas()
    image.draw(750,400)
    font.draw(1100,740,str(gold))#골드
    font.draw(250,500,str(main_state.numUnit1))#유닛 1 갯수


    font.draw(600,565,str((Upgrade1+1)*500))#업그레이드1 비용
    font.draw(600, 510, str(Upgrade1))#업그레이드1 횟수

    font.draw(600,425,str((Upgrade2+1)*500))#업그레이드2 비용
    font.draw(600, 370, str(Upgrade2))#업그레이드2 횟수

    font.draw(600,285,str((Upgrade3+1)*500))#업그레이드3 비용
    font.draw(600, 230, str(Upgrade3))#업그레이드3 횟수

    font.draw(630,145,str((Upgrade4+1)*500))#업그레이드4 비용
    font.draw(630, 90, str(Upgrade4))#업그레이드4 횟수

    font.draw(1350,530,str(main_state.stageEnemy1[main_state.stage]))
    font.draw(1350, 430, str(main_state.stageEnemy2[main_state.stage]))
    update_canvas()



def update():
    pass

def pause():
    pass
def resume():
    pass