from pico2d import *
import game_framework
import title_state

name = "StartState"
image = None
logo_time = 0.0
def enter():
    global image
    p=open_canvas(1600,800)

    SDL_GetWindowTitle
    image = load_image('kpu_credit.png')

def exit():
    global image
    del(image)
    close_canvas()


def update():
    global logo_time
    if (logo_time > 1.0):
        logo_time = 0
        game_framework.push_state(title_state)
    delay(0.01)
    logo_time += 0.01
def draw():
    global image
    clear_canvas()
    image.draw(800, 400)
    update_canvas()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.running=False


def pause():
    pass
def resume():
    pass