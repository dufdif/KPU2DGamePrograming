from pico2d import*
import game_framework
import main_state
import store_state
name = "TitleState"
image = None
bgm=None
def enter():
    global image
    global bgm
    image = load_image('background.jpg')
    bgm=load_music('bgm.mp3')
    bgm.set_volume(55)
    bgm.repeat_play()



def exit():
    global image
    del(image)


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            elif (event.type,event.key) == (SDL_KEYDOWN,SDLK_SPACE):
                game_framework.change_state(store_state)

def draw():
    global image
    clear_canvas()
    image.draw(770,450,1600,900)
    update_canvas()



def update():
    pass

def pause():
    pass
def resume():
    pass