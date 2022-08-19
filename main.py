from pygame import *

init()

back = (200,255,255)
win_width=700
win_height=500
GREEN=(0,255,0)
window = display.set_mode((win_width,win_height))
window.fill(back)
display.set_caption('first')
picture = transform.scale(image.load('back.jpg'), (700,500))
winn = transform.scale(image.load('win.jpg'), (700,500))
lose = transform.scale(image.load('lose.jpg'), (700,500))
bullets = sprite.Group()
barriers = sprite.Group()

class GameSprite(sprite.Sprite):
    def __init__(self,filename, width, height, x, y):
        super().__init__()
        self.image = transform.scale(image.load(filename), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.rect = Rect(x, y, width, height)
        self.fill_color = color

    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Enemy(GameSprite):
    def __init__(self, filename, width, height, x,y, speed):
        super().__init__(filename, width, height, x, y)
        self.speed = speed

    def update(self):
        if self.rect.x<=300:
            self.direction = 'right'
        elif self.rect.x>=500:
            self.direction = 'left'
        if self.direction == 'right':
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed
        
class Player(GameSprite):
    def __init__(self, filename, width, height, x,y, x_speed, y_speed):
        super().__init__(filename, width, height, x, y)
        self.x_speed = x_speed
        self.y_speed = y_speed
    def update(self):
        if self.rect.x>0 or self.x_speed>0 and self.rect.x<700:
            self.rect.x += self.x_speed

        self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed>0:
            for p in platforms_touched:
                self.rect.right=min(self.rect.right, p.rect.left)
        elif self.x_speed<0:
            for p in platforms_touched:
                self.rect.left=max(self.rect.left, p.rect.right)

        self.rect.y += self.y_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed>0:
            for p in platforms_touched:
                self.rect.bottom=min(self.rect.bottom, p.rect.top)
        elif self.y_speed<0:
            for p in platforms_touched:
                self.rect.top=max(self.rect.top, p.rect.bottom)

    def fire(self):
        bullet = Bullet('fire.png', 50,50, self.rect.right,self.rect.centery-15, 50)
        bullets.add(bullet)
class Bullet(GameSprite):
    def __init__(self, filename, width, height, x, y, speed):
        super().__init__(filename, width, height, x, y)
        self.speed = speed
    def update(self):
        self.rect.x +=self.speed
        if self.rect.x>500:
            self.kill()

player = Player('mario.png', 70, 70, 100,250, 0, 0)
wall1 = GameSprite('wall.png', 60, 400, 400, 50)
wall2 = GameSprite('wall.png', 400, 60, 200, 170)
wall3 = GameSprite('wall.png', 60, 350, 200, 350)
win = GameSprite('key.png', 48, 48, 500, 300)
mush = Enemy('mushroom.png', 60, 60, 500, 350, 5)


barriers = sprite.Group()
barriers.add(wall1)
barriers.add(wall2)
barriers.add(wall3)

enemies = sprite.Group()
enemies.add(mush)

run = True
finish = False
while run:
    
    time.delay(50)
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_RIGHT:
                player.x_speed=8
            if e.key == K_LEFT:
                player.x_speed=-8
            if e.key == K_UP:
                player.y_speed=-10
            if e.key == K_DOWN:
                player.y_speed=10
            if e.key == K_SPACE:
                player.fire()
        if e.type == KEYUP:
            if e.key == K_RIGHT:
                player.x_speed=0
            if e.key == K_LEFT:
                player.x_speed=0
            if e.key == K_UP:
                player.y_speed=0
            if e.key == K_DOWN:
                player.y_speed=0
    window.blit(picture,(0,0))

    if sprite.collide_rect(player, win):
        win.reset()
        finish = True
        window.blit(winn,(0,0))
    if sprite.collide_rect(player, mush):
        mush.reset()
        finish = True
        window.blit(lose,(0,0))

    



    if not(finish):
        sprite.groupcollide(bullets, barriers, True, False)
        sprite.groupcollide(bullets,barriers, True, True)
        win.reset()
        enemies.draw(window)
        enemies.update()
        barriers.draw(window)
        bullets.draw(window)
        player.update()
        player.reset()
    
        wall1.reset()
        wall2.reset()
        wall3.reset()
        bullets.update()

           
        
 
    display.update()
