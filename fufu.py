from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

import time

app = Ursina()


class yee(FirstPersonController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.speed_normal = 5  
        self.speed_run = 10
        self.mouse_sensitivity_default = Vec2(40, 40)

    def update(self):
        super().update()

        if held_keys['shift']:
            self.speed = self.speed_run
        else:
            self.speed = self.speed_normal

        if mouse.locked:
            self.mouse_sensitivity = self.mouse_sensitivity_default
        else:
            self.mouse_sensitivity = Vec2(0, 0)


player = yee(position=(0, 0, 0), collider='capsule')

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
    if key == 'left mouse down':
        hit_info = raycast(camera.world_position, camera.forward, distance=100, ignore=[player])
        if hit_info.hit and hit_info.entity == ground:
            block = Entity(model='cube',
                           color=color.red.tint(0.4),
                           texture='brick',
                           scale=(2,2,2),
                           world_position=hit_info.world_point,
                           collider='box')
            blocks.append(block)
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

