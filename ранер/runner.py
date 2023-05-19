from pygame import *
from random import randint
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
coins = 0
jump_schetchik = 0
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
            collect_coin(1)
        if self.rect.x > -100:
            self.rect.x -= self.speed
        else:
            self.rect.x = 1000
        window.blit(self.image,(self.rect.x,self.rect.y))
class Payse(Sprites):
    def __init__(self,sprite,x,y,w,h):
        super().__init__(sprite,x,y,w,h)
        self.image = transform.scale(image.load(sprite),(self.w,self.h))
    def update(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
def collect_coin(takes_coins):
    global coins
    global coins_font
    coins += takes_coins
    coins_font = font.render(str(coins) ,True,(0,0,0))

# геймплей
bg_coin = transform.scale(image.load('coin.png'),(40,50))
bg = transform.scale(image.load('bg.png'),(800,600))

player = Player('player.png',100,500,200,100,50)
payse = Sprites('payse.png',730,10,50,50)
start_button = Payse('start.png',330,220,150,150)
stop_menu = Sprites('stop_menu.png',100,150,600,300)
rock_bg1 = Animate_bg('gora.png',0,286,820,164,1)   
rock_bg2 = Animate_bg('gora.png',820,286,820,164,1)
flour1 = Animate_bg('flour.png',0,450,300,150,3)
flour2 = Animate_bg('flour.png',300,450,300,150,3)
flour3 = Animate_bg('flour.png',600,450,300,150,3)
flour4 = Animate_bg('flour.png',900,450,300,150,3)
spike1 = Spikes('spike.png',800,460,3,100,90)
spikes.add(spike1)
coin = Coins('coin.png',1000,460,3,50,70)

# лобби
lobby_bg = Sprites('lobby_bg.png',0,0,800,600)
start_button2 = Sprites('start.png',350,250,120,120)
while game:
    for i in event.get():
        if i.type == QUIT:
            game = False
        if i.type == MOUSEBUTTONUP:
            if payse.rect.collidepoint(i.pos):
                final = False
                payse_window = True
            if start_button.rect.collidepoint(i.pos):
                final = True
                payse_window = False
            if start_button2.rect.collidepoint(i.pos):
                final = True
                lobby = False   
    if payse_window:
        stop_menu.update()
        start_button.update()
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
        coin.update()
        payse.update()
    clock.tick(fps)
    display.update()
