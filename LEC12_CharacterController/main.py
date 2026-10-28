from pico2d import *
import random

from boy import Boy # boy : 모듈 이름, Boy : 클래스 이름
from grass import Grass # grass : 모듈 이름, Grass : 클래스 이름


# Game object class here



def handle_events():
    global running

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_a:
            boy.begin_autorun()
        elif event.type == SDL_KEYDOWN and event.key in (SDLK_LEFT, SDLK_RIGHT):
            direction = -1 if event.key == SDLK_LEFT else 1
            if direction not in pressed_directions:
                pressed_directions.append(direction)
        elif event.type == SDL_KEYUP and event.key in (SDLK_LEFT, SDLK_RIGHT):
            direction = -1 if event.key == SDLK_LEFT else 1
            if direction in pressed_directions:
                pressed_directions.remove(direction)

    boy.update_direction_keys(pressed_directions)


def reset_world():
    global world
    global boy
    global pressed_directions

    world = []
    pressed_directions = []

    grass = Grass()
    world.append(grass)

    boy = Boy()
    world.append(boy)



def update_world():
    for o in world:
        o.update()
    pass


def render_world():
    clear_canvas()
    for o in world:
        o.draw()
    update_canvas()


running = True

open_canvas()
reset_world()
# game loop
while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)
# finalization code
close_canvas()
