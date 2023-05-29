from pygame import *
from random import randint
import json
font.init()
mixer.init()
window = display.set_mode((800,600))
display.set_caption('Ето ранир')
clock = time.Clock()
font = font.Font(None,50)
canjump = 'true'
final = False
payse_window = False
lobby = True
fps = 60
variant_x = 0
with open('stata.json','r',encoding='utf-8') as file:
    data = json.load(file)
    coins_int = data['coins']
jump_schetchik = 0
coins_font = font.render(str(coins_int) ,True,(0,0,0))
game = True
spikes = sprite.Group()
coins = sprite.Group()

class Sprites(sprite.Sprite):
    def __init__(self,sprite,x,y,w,h):
        super().__init__()
        self.w = w
        self.h = h
        self.image = transform.scale(image.load(sprite),(self.w,self.h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y 
    def update(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(Sprites):
    def __init__(self,sprite,x,y,jump_stranght,w,h):
        super().__init__(sprite,x,y,w,h)
        self.image = transform.scale(image.load(sprite),(self.w,self.h))
        self.jump_stranght = jump_stranght
    def move(self):
        global canjump
        keys = key.get_pressed()
        if keys[K_SPACE] and canjump == 'true':
            canjump = 'false'
            self.first_y = self.rect.y
            self.jymp = True
            self.jjump = False
        if canjump == 'false':
            self.jump()
    def jump(self):
        global canjump 
        global jump_schetchik 
        if self.first_y-self.jump_stranght <= self.rect.y and self.jymp:
            self.rect.y -= 5
        if self.first_y-self.jump_stranght >= self.rect.y or self.jjump:
            self.jymp = False
            self.jjump = True
            jump_schetchik += 1
            if jump_schetchik >= 20 and self.first_y != self.rect.y:
                self.rect.y += 5
        if self.first_y == self.rect.y:
            canjump = 'true'
            jump_schetchik = 0

class Animate_bg(Sprites):
    def __init__(self,sprite,x,y,w,h,speed):
        super().__init__(sprite,x,y,w,h)
        self.image = transform.scale(image.load(sprite),(self.w,self.h))
        self.speed = speed
        self.weight = w
    def moving(self):
        self.rect.x -= self.speed
        if self.rect.x <= -self.weight:
            self.rect.x = 800
        window.blit(self.image,(self.rect.x,self.rect.y))

class Spikes(Sprites):
    def __init__(self,sprite,x,y,speed,w,h):
        super().__init__(sprite,x,y,w,h)
        self.image = transform.scale(image.load(sprite),(self.w,self.h))
        self.speed = speed
    def update(self):
        if sprite.spritecollide(player,spikes,False,collided=sprite.collide_rect_ratio(.78)):
            global final
            global payse_window
            final = False
            payse_window = True
        if self.rect.x > -100:
            self.rect.x -= self.speed
        else:
            self.kill()
        window.blit(self.image,(self.rect.x,self.rect.y))

class Coins(Sprites):
    def __init__(self,sprite,x,y,speed,w,h):
        super().__init__(sprite,x,y,w,h)
        self.image = transform.scale(image.load(sprite),(self.w,self.h))
        self.speed = speed
    def update(self):
        if sprite.collide_rect(self,player):
            self.kill()
            collect_coin(1)
        if self.rect.x > -100:
            self.rect.x -= self.speed
        else:
            self.kill()
        window.blit(self.image,(self.rect.x,self.rect.y))

class Payse(Sprites):
    def __init__(self,sprite,x,y,w,h):
        super().__init__(sprite,x,y,w,h)
        self.image = transform.scale(image.load(sprite),(self.w,self.h))
    def update(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
def collect_coin(takes_coins):
    global coins_int
    global coins_font
    coins_int += takes_coins
    coins_font = font.render(str(coins_int) ,True,(0,0,0))
def make_variant(variant,variant_x):
    for a in range(len(variant)):
        for i in range(len(variant[a])):
            if variant[a][i] == variant[a][0]:
                x = 1000
            if variant[a][i] == variant[a][1]:
                x = 1100
            if variant[a][i] == variant[a][2]:
                x = 1200
            if variant[a][i] == variant[a][3]:
                x = 1300  
            if variant[a][i] == variant[a][4]:
                x = 1400
            if variant[a] == variant[0]:
                y = 60
            if variant[a] == variant[1]:
                y = 160
            if variant[a] == variant[2]:
                y = 260
            if variant[a] == variant[3]:
                y = 360
            if variant[a] == variant[4]:
                y = 460
            if variant[a][i] == 'coin':
                coin = Coins('coin.png',x+variant_x,y,3,50,70)
                coins.add(coin)
            if variant[a][i] == 'coin2':
                coin = Coins('coin.png',x+variant_x,y,3,50,70)
                coins.add(coin)
            if variant[a][i] == 'coin3':
                coin = Coins('coin.png',x+variant_x,y,3,50,70)
                coins.add(coin)
            if variant[a][i] == 'spike':
                x-=25
                spike = Spikes('spike.png',x+variant_x,y,3,100,90)
                spikes.add(spike)

# геймплей
bg_coin = transform.scale(image.load('coin.png'),(40,50))
bg = transform.scale(image.load('bg.png'),(800,600))

player = Player('player.png',100,500,200,100,50)

payse = Sprites('payse.png',730,10,50,50)
start_button = Payse('start.png',340,220,150,150)
stop_menu = Sprites('stop_menu.png',100,150,600,300)
go_home = Sprites('go_home.png',140,220,150,150)

rock_bg1 = Animate_bg('gora.png',0,286,820,164,1)   
rock_bg2 = Animate_bg('gora.png',820,286,820,164,1)
flour1 = Animate_bg('flour.png',0,450,300,150,3)
flour2 = Animate_bg('flour.png',300,450,300,150,3)
flour3 = Animate_bg('flour.png',600,450,300,150,3)
flour4 = Animate_bg('flour.png',900,450,300,150,3)

#               лобби
lobby_bg = Sprites('lobby_bg.png',0,0,800,600)
start_button2 = Sprites('start.png',350,250,120,120)

while game:
    for i in event.get():
        if i.type == QUIT:
            game = False
            del data['coins']
            data['coins'] = coins_int
            data = {'coins':coins_int,'variants':
                                            [[[None,None,None,None,None],
                                            [None,None,None,None,None],
                                            [None,None,'coin',None,None],
                                            [None,'coin',None,'coin2',None],
                                            ['coin',None,'spike',None,'coin2']]
                                        ,
                                            [[None,None,None,None,None],
                                            [None,None,None,None,None],
                                            [None,None,None,None,None],
                                            [None,None,None,None,None],
                                            ['coin','coin2','coin3','spike',None]]
                                        ,
                                            [[None,None,None,None,None],
                                            [None,None,None,None,None],
                                            [None,None,None,None,None],
                                            [None,'coin',None,None,None],
                                            ['coin','spike','coin2',None,None]]
                                            ]}
            with open('stata.json','w',encoding='utf-8') as file:
                json.dump(data,file)
        if i.type == MOUSEBUTTONUP:
            if payse.rect.collidepoint(i.pos):
                final = False
                payse_window = True
            if start_button.rect.collidepoint(i.pos):
                spikes.empty()
                coins.empty()
                final = True
                payse_window = False
                #       отрисовка
                for e in range(0,3):
                    e = randint(0,2)
                    make_variant(data['variants'][e],variant_x)
                    variant_x += 500
                variant_x = 0
            if start_button2.rect.collidepoint(i.pos):
                final = True
                lobby = False   
            if go_home.rect.collidepoint(i.pos):
                payse_window = False
                final = False
                lobby = True
    if payse_window:
        stop_menu.update()
        start_button.update()
        go_home.update()
    if lobby:
        lobby_bg.update()
        start_button2.update()
    if final:
        window.blit(bg,(0,0))
        window.blit(coins_font,(80,30))
        window.blit(bg_coin,(20,20))
        rock_bg1.moving()
        rock_bg2.moving()
        flour1.moving()
        flour2.moving()
        flour3.moving()
        flour4.moving()
        player.update()
        player.move()
        spikes.update()
        spikes.draw(window)
        coins.update()
        coins.draw(window)
        payse.update()
    clock.tick(fps)
    display.update()
