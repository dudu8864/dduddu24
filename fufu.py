from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

import time

app = Ursina()

player = FirstPersonController(collider = 'box')

ball = Entity(
    parent=camera,
    model='sphere',
    color=color.red,
    scale=0.6,
    collider='sphere',
    position=(0.4, -0.3, 0.7)
)

ground = Entity(model='plane', scale=(50,1,50), color=color.white.tint(-0.2), collider='box')

mouse.locked = True
window.fullscreen = True
camera.fov = 90
blocks = []


def input(key):
    global blocks
    if ground.hovered:
        if key == 'left mouse down':
            block = Entity(model='cube',color=color.red.tint(0.4),texture='brick', scale=(2,2,2),world_position=mouse.world_point, collider = 'box' )
            blocks.append(block)
            print('wa sans!')
            
    for block in blocks:
            if block.hovered == True: 
                if key == 'left mouse down': 
                    block = Entity(model='cube',color=color.red.tint(.4), texture='brick',scale=(2,2,2),position=mouse.world_point,collider = 'box' )
                    blocks.append(block)
                if key == 'right mouse down':
                    blocks.remove(block)
                    destroy(block)

    if key == 'escape':
        application.quit()

    if key == 'control':
        mouse.locked = not mouse.locked

    if key == 'e':
        if ball.parent == camera:
            ball.parent = scene
            ball.position = player.world_position + player.forward * 1 + Vec3(0, 0.5, 0)
        else:
            ball.parent = camera
            ball.position = Vec3(0.5, -0.3, 0.8)

app.run()

