from pygame import *
from random import randint
#load functions for working with fonts seperately

font.init()
font1 = font.Font(None,80)
win = font1.render('You win!' ,True, (0,255,0))
lose = font1.render('You lose!', True, (255,0,0))

font2 = font.Font(None,36)

#sfx
mixer.init()
fire_sound = mixer.Sound('shoot.mp3')

#we need these pictures:
img_back = 'background.png'
img_hero = 'rocket.png' 
img_enemy = 'enemy.webp'
img_bullet = 'bullet.png'

score = 0    #ships hit
goal = 50 #ships need to be hit in order to win
lost = 0 #ships missed
max_lost = 3        # lose if this mant missed

#parent class for sprites
class GameSprite(sprite.Sprite):
    #class constuctor
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        #every sprite must store the image property
        self.image = transform.scale(image.load(player_image), (65,65))
        self.speed = player_speed
        #every sprite must have the rect property - the rectangle is fitted in
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x,self.rect.y))

#child class for the player sprite (controlled by arrows)
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    #the "fire" method (use the player's place to create a bullet there)
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx-30, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

#enemy sprite class
class Enemy(GameSprite):
    #enemy movement
    def update(self):
        self.rect.y += (self.speed)
        global lost
        #dissapears if reaches edge of the screen
        if self.rect.y > win_height:
            self.rect.x = randint(80,win_width - 80)
            self.rect.y = 0
            lost += 1

#bullet sprite class
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed 
        #disappears
        if self.rect.y < 0:
            self.kill()


#Game scene
win_width = 700
win_height = 500
window = display.set_mode((win_width,win_height))
display.set_caption("Galaga by Tan")
background = transform.scale(image.load(img_back), (win_width, win_height))

#create sprites
ship = Player(img_hero, 350, win_height - 100, 80, 100, 4)


#creating a group of enemy sprites
monsters = sprite.Group()
for i in range (1,6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40,80,50,randint(1,3))

    monsters.add(monster)

bullets = sprite.Group()


finish = False
run = True

while run:
    #press close button
    for e in event.get():
        if e.type == QUIT:
            run = False
        #press on the space bar - the sprite fires
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play
                ship.fire()

    
    if not finish:
        #refresh background
        window.blit(background,(0,0))

        #writing text on the screen
        text = font2.render("Score: " + str(score),1,(255,255,255))
        window.blit(text, (10,20))

        text_lose = font2.render("Missed: " + str(lost), 1, (255,255,255))
        window.blit(text_lose, (10,50))

        #producing sprite movements
        ship.update()
        monsters.update()
        bullets.update()

        #updating them at a location on each iteration of the loop
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)

        #bullet-monster collision check
        collides = sprite.groupcollide(monsters, bullets, True,True)
        for c in collides:
            #this loop will be repeated as many times as monsters are killed
            score += 1
            monster = Enemy(img_enemy, randint(80, win_width- 80), -50,80,50,randint(1,3))
            monsters.add(monster)

        #possible loss: missed too many/ character collided
        if sprite.spritecollide(ship,monsters,False) or lost >= max_lost:
            finish = True
            window.blit(lose,(200,200))

        #win check: points scored
        if score >= goal:
            finish = True
            window.blit(win,(200,200))

        display.update()
    #the loop runs every 0.05 seconds
    time.delay(10)
