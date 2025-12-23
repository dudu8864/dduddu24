
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
import time

app = Ursina()

#EditorCamera()
player = FirstPersonController( 
    model = 'cube',
    scale = 1, 
    color = (0,0,0,0)
    )

ball = Entity(
    parent=camera,
    model='sphere',
    color=color.red,
    scale=0.3,
    collider='sphere',
    position=(0.5, -0.3, 0.8)
)
ball.undestroyable = True

ground = Entity(
    model='plane',
    collider='box',
    scale=300,
    position=(0,0,0),
    texture='grass'
)
ground.undestroyable = True

#debug_text = Text(text='', position=(-0.85, 0.45), scale=1, color=color.yellow)
mouse.locked = True
window.fullscreen = True
camera.fov = 90
gravity = 0.98

state = 0 # 쏘기전
ball.direction = Vec3(0,0,0)

winner_stack = 0
win_text = Text(text='win!', position=(-.07,.04), scale=3, color=color.yellow)
win_text.enabled = False
voxel_count_text = Text(text='', position=(0, -0.1),origin=(0, 0), scale=1.5, color=color.lime)
voxel_count_text.enabled = False

def update():
    global state, winner_stack

    if held_keys['control']:
        player.speed = 2
    elif held_keys['shift']:
        player.speed = 15
    else:                   
        player.speed = 7

    voxels = [e for e in scene.entities if isinstance(e, Voxel)]
    current_voxel_count = len(voxels) - 900
    voxel_count_text.text = f'Installed Blocks: {current_voxel_count}'

    if state == 1:
        speed = 25
        move_step = ball.direction * speed * time.dt
        ball.direction.y -= 0.5 * time.dt
        hit_info = raycast(ball.world_position, ball.direction, distance=move_step.length(), ignore=(ball, player))

        if hit_info.hit:
            state = 0 
            if isinstance(hit_info.entity, Board):
                if hit_info.entity.color != color.green:
                    hit_info.entity.color = color.green
                    winner_stack +=1
                    total_boards = len([e for e in scene.entities if isinstance(e, Board)])
                    if winner_stack >= total_boards:
                        win_text.enabled = True
                        voxel_count_text.enabled = True
                        player.cursor.enabled = False
        else:
            ball.position += move_step
              
            ball.direction.y -= gravity * time.dt
        

class Board(Entity):
    def __init__(self, position=(0,0,0), color = color.azure):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=.10,
            texture='white_cube',
            color=color,
            collider='box'
        )
for i in range(5):
    Board(
        position=(
            random.uniform(1, 28), 
            random.uniform(7, 20),
            random.uniform(1, 28)  
        ),
        color=color.red)
    Board.undestroyable = True

class Voxel(Button):
    def __init__(self, position=(0,0,0)):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=.10,
            texture='white_cube',
            color=color.hsv(0, 0, random.uniform(.9, 1.0)),
            highlight_color=color.green)


def input(key):
    global state
    if key == 'left mouse down':
        hit_info = raycast(camera.world_position, camera.forward, distance=50)
        if hit_info.hit:
            if not isinstance(hit_info.entity, (Wall, Board)):
                Voxel(position=hit_info.entity.position + hit_info.normal)
    if key == 'right mouse down':
        e = mouse.hovered_entity
        if e and not getattr(e, 'undestroyable', False):
            destroy(e)
    '''
    if key == 'q':
        hit_info = raycast(camera.world_position, camera.forward, distance=20, ignore=(player,))
        
        if hit_info.hit:
            # 정보를 텍스트에 표시
            debug_text.text = (
                f"Hit Entity: {hit_info.entity}\n"
                f"Hit Point: {hit_info.world_point}\n"
                f"Distance: {round(hit_info.distance, 2)}"
            )
            invoke(setattr, debug_text, 'text', '', delay=5)
        else:
            debug_text.text = "No hit"
            invoke(setattr, debug_text, 'text', '', delay=5)
    '''

    if key == 'escape':
        application.quit()

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

for z in range(30):
    for x in range(30):
        voxel = Voxel(position=(x,0,z))

class Wall (Entity):
    def __init__(self, position=(0,0,0), rotation=(0,0,0)):
        super().__init__(
            model='quad', 
            color=color.gray, 
            scale=30, 
            double_sided=True, 
            position=position,
            rotation=rotation,
            collider='box'
        )
        Wall.undestroyable = True

Wall(position=(14.5,15,-0.5))
Wall(position=(14.5,15,29.5))
Wall(position=(29.5,15,14.5), rotation=(0,90,0))
Wall(position=(-0.5,15,14.5), rotation=(0,90,0))

app.run()

