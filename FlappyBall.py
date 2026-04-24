from ursina import *
import random

app = Ursina()

Sky()
camera.orthographic = True
camera.fov = 20

oyun_basladi = False
skor = 0
boru_zamanlayici = 0 

bird = Entity(model='quad', texture='circle', color=color.blue, scale=(1,1,1), collider='box')
bird.gravity = 0.5
bird.velocity = 0
skor_metni = Text(text=f'Skor: {skor}', position=(-0.1, 0.4), scale=2, color=color.black)
bilgi_metni = Text(text='Baslamak icin SPACE tusuna bas', origin=(0, -8), color=color.black)

pipes = []
pipe_speed = 5

def create_pipe():
    random_y = random.uniform(-3, 3)
    top = Entity(model='quad', color=color.green, scale=(2, 15, 1), 
                 position=(20, random_y + 10, 0), collider='box', passed=False)
    bottom = Entity(model='quad', color=color.green, scale=(2, 15, 1), 
                    position=(20, random_y - 10, 0), collider='box', passed=False)
    pipes.append(top)
    pipes.append(bottom)

def update():
    global oyun_basladi, skor, boru_zamanlayici
    if held_keys['space'] and not oyun_basladi:
        oyun_basladi = True
        bilgi_metni.enabled = False
        boru_zamanlayici = 2 

    if oyun_basladi:
        bird.velocity -= bird.gravity * time.dt
        bird.y += bird.velocity
        if held_keys['space']:
            bird.velocity = 0.08
            
        boru_zamanlayici += time.dt
        if boru_zamanlayici >= 2:
            create_pipe()
            boru_zamanlayici = 0

        for p in pipes:
            p.x -= pipe_speed * time.dt
            
            if not p.passed and p.x < bird.x:
                p.passed = True
                if pipes.index(p) % 2 == 0:
                    skor += 1
                    skor_metni.text = f'Skor: {skor}'

            if bird.intersects(p).hit or bird.y < -10 or bird.y > 10:
                reset_game()
                return

def reset_game():
    global oyun_basladi, skor, boru_zamanlayici
    oyun_basladi = False
    skor = 0
    boru_zamanlayici = 0
    skor_metni.text = f'Skor: {skor}'
    bilgi_metni.enabled = True
    bird.y = 0
    bird.velocity = 0
    for p in pipes:
        destroy(p)
    pipes.clear()
app.run()




