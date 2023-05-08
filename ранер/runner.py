from pygame import *
from random import randint
font.init()
mixer.init()
window = display.set_mode((800,600))
bg = transform.scale(image.load('bg.png'),(800,600))
bg_coin = transform.scale(image.load('coin.png'),(40,50))
display.set_caption('Ето ранир')
clock = time.Clock()
font = font.Font(None,50)
canjump = 'true'
final = True
j = 0
fps = 60
coins = 0
coins_font = font.render(str(coins) ,True,(0,0,0))
game = True
spikes = sprite.Group()
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
            global j
            self.j = j
        if canjump == 'false':
            self.jump()
    def jump(self):
        global canjump  
        if self.j <= self.jump_stranght*0.9:
            self.rect.y -= 5
            self.j += 1
        if self.j > self.jump_stranght*0.9 and self.j <= self.jump_stranght*1.1:
            self.j += 1
        if self.j > self.jump_stranght*1.1:
            self.rect.y += 5
            self.j += 1
        if self.j > self.jump_stranght*2.05:
            self.rect.y = self.first_y
            canjump = 'true'
            self.j = 0
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
            final = False
        if self.rect.x > -100:
            self.rect.x -= self.speed
        else:
            self.rect.x = 1000
        window.blit(self.image,(self.rect.x,self.rect.y))
class Coins(Sprites):
    def __init__(self,sprite,x,y,speed,w,h):
        super().__init__(sprite,x,y,w,h)
        self.image = transform.scale(image.load(sprite),(self.w,self.h))
        self.speed = speed
    def update(self):
        if sprite.collide_rect(self,player):
            self.rect.x = 1000
            collect_coin(100)
        if self.rect.x > -100:
            self.rect.x -= self.speed
        else:
            self.rect.x = 1000
        window.blit(self.image,(self.rect.x,self.rect.y))
def collect_coin(takes_coins):
    global coins
    global coins_font
    coins += takes_coins
    coins_font = font.render(str(coins) ,True,(0,0,0))
player = Player('player.png',100,500,50,100,50)
rock_bg1 = Animate_bg('gora.png',0,286,820,164,1)   
rock_bg2 = Animate_bg('gora.png',820,286,820,164,1)
flour1 = Animate_bg('flour.png',0,450,300,150,3)
flour2 = Animate_bg('flour.png',300,450,300,150,3)
flour3 = Animate_bg('flour.png',600,450,300,150,3)
flour4 = Animate_bg('flour.png',900,450,300,150,3)
spike1 = Spikes('spike.png',800,460,3,100,90)
spikes.add(spike1)
coin = Coins('coin.png',1000,460,3,50,70)
while game:
    for i in event.get():
        if i.type == QUIT:
            game = False
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
        coin.update()
        clock.tick(fps)
        display.update()