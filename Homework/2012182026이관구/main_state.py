from pico2d import *
import game_framework

from GameObject import *

# --- 설계된 모든 오브젝트를 직접 생성해서 사용하며 게임진행을 한다. ---

Maxnum=1

team='{	"0" : {"state":"LeftStand","x":100,"y":200} ,"1":{"state":"RightRun","x":400,"y":200} , "2":{"state":"LeftRun","x":100,"y":500},"3":{"state":"RightStand","x":100,"y":300},"4":{"state":"LeftRun","x":600,"y":200} }'

Boys = []
balls=[]

player =None


xKey=[]

yKey=[]


def collide(a,b):
	la,ba,ra,ta=a.get_bb()
	lb,bb,rb,tb=b.get_bb()
	if la>rb:return False
	if ra<lb: return False
	if ta<bb: return False
	if ba>tb: return False
	return True

def handle_events():  # F1~5까지 누르면 유닛선택

    events = get_events()

    global player
    global type
    global xKey
    global yKey
    global Boys




    for event in events:

        if event.type == SDL_KEYDOWN:

            if event.key == SDLK_ESCAPE:

                game_framework.quit()
    #        elif event.key == SDLK_F1:
     #           player=Boys[0]
      #      elif event.key == SDLK_F2:
       #         player=Boys[1]
        #    elif event.key == SDLK_F3:
         #       player = Boys[2]
          #  elif event.key == SDLK_F4:
           #     player = Boys[3]
            #elif event.key == SDLK_F5:
             #   player = Boys[4]


            elif event.key==SDLK_LEFT:

                xKey+=[0]

            elif event.key==SDLK_RIGHT:

                xKey+=[1]



            elif event.key == SDLK_UP:

                yKey += [0]

            elif event.key == SDLK_DOWN:

                yKey+=[1]



        elif event.type == SDL_KEYUP:

            if event.key == SDLK_LEFT:
                player.state = player.LeftStand
                if len(xKey)>0:

                    xKey.remove(0)

            elif event.key == SDLK_RIGHT:
                player.state = player.RightStand
                if len(xKey) > 0:

                    xKey.remove(1)

            elif event.key == SDLK_UP:

                if len(yKey) > 0:

                    yKey.remove(0)

            elif event.key == SDLK_DOWN:

                if len(yKey) > 0:

                    yKey.remove(1)







grass = None
state_table={'LeftRun':0,    'RightRun':1,    'LeftStand':2,    'RightStand':3}
def enter():
    global Boys
    global grass
    global player
    global Font
    global balls
    global state_table
    import json
    global team

    tdata=json.loads(team)

    Boys=[boy(i) for i in range(Maxnum)]
    balls=[ball(i) for i in range(10)]

    for i in range(Maxnum):
        strnum=str(Boys[i].num)
        Boys[i].x=tdata[strnum]['x']
        Boys[i].y = tdata[strnum]['y']
        Boys[i].state = state_table[tdata[strnum]['state']]

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
    global player
    global xKey
    global yKey
    for b in Boys:
        b.update()
    if collide(grass, Boys[0]):
        Boys[0].y = 95

    for b in balls:
        b.update()

    if len(xKey) != 0:

        if xKey[0] == 0:
            player.state=player.LeftRun
            if player.x>0:
                player.x -= 100*game_framework.deltatime

        else:
            player.state=player.RightRun
            if player.x<800:
                player.x += 100*game_framework.deltatime
    if len(yKey) != 0:

        if yKey[0] == 0:

            player.y += 100*game_framework.deltatime

        else:

            player.y -= 100*game_framework.deltatime




    for b in balls:
        if collide(Boys[0],b):
            balls.remove(b)
            Boys[0].eat()
        if collide(grass,b):
            b.y=65




def draw():#여기서 모든 객체를 그리고 모든 폰트를 그린다. 매우 중요한 상태의 드로우함수!
    clear_canvas()
    global Boys
    global grass
    global player
    global balls
    for b in Boys:
        b.Draw()
    for b in balls:
        b.Draw()

    grass.Draw()
    Font.draw(0,580,'Character Number  :' + str(player.num+1))


    update_canvas()

def pause(): pass
def resume(): pass