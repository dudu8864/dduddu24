
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

import time

app = Ursina()

#EditorCamera()
player = FirstPersonController( 
    model = 'sphere',
    scale = 1, 
    color = (0,0,0,0),
    speed = 15)


ball = Entity(
    parent=camera,
    model='sphere',
    color=color.red,
    scale=0.4,
    collider='sphere',
    position=(-10,0,0) 
)
ball.undestroyable = True

ground = Entity(
    model='plane',
    collider='box',
    scale=64,
    texture='grass',
    texture_scale=(4,4)
)
ground.undestroyable = True

mouse.locked = True
window.fullscreen = True
camera.fov = 90
blocks = []
jump_cooltime = 0
jump_delay = 0.8  # 0.3초마다 점프
gravity = 0.98
state = 0 # 쏘기전
ball.direction = Vec3(0,0,0)

def update():
    global state
    #print(f'플레이어포워드값 {player.forward}')
    #print(f'플레이어 위치 {player.world_position}')
    global jump_cooltime

    if jump_cooltime > 0:
        jump_cooltime -= time.dt

    if held_keys['space'] and jump_cooltime <= 0 and player.grounded:
        player.jump()
        jump_cooltime = jump_delay

        player.camera_pivot.rotation_y = clamp(player.camera_pivot.rotation_y,-80,80)

    if state == 1:
        speed = 40
        move_step = ball.direction * speed * time.dt
        ball.direction.y -= 0.5 * time.dt
        hit_info = raycast(ball.world_position, ball.direction, distance=move_step.length(), ignore=(ball, player))

        if hit_info.hit:
            ball.position = hit_info.world_point
            #ball.position += hit_info.normal * (ball.scale.x / 2)
            state = 0 
        else:
            ball.position += move_step
            
            ball.direction.y -= gravity * time.dt


class Voxel(Button):
    def __init__(self, position=(0,0,0)):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=.10,
            texture='white_cube',
            color=color.hsv(0, 0, random.uniform(.9, 1.0)),
            highlight_color=color.lime,
        )


def input(key):
    global state
    if key == 'left mouse down':
        hit_info = raycast(camera.world_position, camera.forward, distance=5)
        if hit_info.hit:
            Voxel(position=hit_info.entity.position + hit_info.normal)
    if key == 'right mouse down':
        e = mouse.hovered_entity
        if e and not getattr(e, 'undestroyable', False):
            destroy(e)


    if key == 'escape':
        application.quit()

    if key == 'control':
        mouse.locked = not mouse.locked

    if key == 'e':
        if ball.parent == camera:
            state = 1
            ball.parent = scene
            ball.scale = 1
            ball.position = camera.world_position + camera.forward
            ball.direction = camera.forward
        else:
            state = 0
            ball.parent = camera
            ball.position = Vec3(0.5, -0.3, 0.8)
            ball.scale = 0.3

for z in range(10):
    for x in range(10):
        voxel = Voxel(position=(x+5,1,z))

app.run()

