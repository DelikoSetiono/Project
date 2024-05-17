from pygame import *


class GameSprite(sprite.Sprite):
 def __init__(self, player_image, player_x, player_y, size_x, size_y):
     sprite.Sprite.__init__(self)
     self.image = transform.scale(image.load(player_image), (size_x, size_y))
     self.rect = self.image.get_rect()
     self.rect.x = player_x
     self.rect.y = player_y
 def reset(self):
     window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed, player_y_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed

        self.is_jumping = False
        self.jump_speed = -18
        self.gravity = 1
        self.y_velocity = -10

    def update(self):
        if packman.rect.x <= win_width - 130 and packman.x_speed > 0 or packman.rect.x >= 0 and packman.x_speed < 0:
            self.rect.x += self.x_speed
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)

        self.y_velocity += self.gravity
        self.rect.y += self.y_velocity

        if self.rect.y >= 460 - self.rect.height:
            self.rect.y = 460 - self.rect.height
            self.y_velocity = 0
            self.is_jumping = False

        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_velocity > 0:
            for p in platforms_touched:
                self.y_velocity = 10
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
        elif self.y_velocity < 0:
            for p in platforms_touched:
                self.y_velocity = 0
                self.rect.top = max(self.rect.top, p.rect.bottom)

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.y_velocity = self.jump_speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.right, self.rect.centery, 15, 20, 17)
        bullets.add(bullet)

class Enemy(GameSprite):
 side = "Left"
 def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
     GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
     self.speed = player_speed


 def update(self):
     if self.rect.x <= 500: 
         self.side = "right"
     if self.rect.x >= win_width - 120:
         self.side = "left"
     if self.side == "left":
         self.rect.x -= self.speed
     else:
         self.rect.x += self.speed

class Bullet(GameSprite):
 def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
     GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
     self.speed = player_speed

 def update(self):
     self.rect.x += self.speed

     if self.rect.x > win_width+10:
         self.kill()

win_width = 1100
win_height = 495
display.set_caption("Project")
window = display.set_mode((win_width, win_height))
back = image.load("back1.jpg")

barriers = sprite.Group()
bullets = sprite.Group()
monsters = sprite.Group()

w1 = GameSprite('wall_2.png', 300, 350, 119, 38)
w2 = GameSprite('wall1.png', 100, 344, 50, 110)
w3 = GameSprite('wall1.png', 259, 360, 60, 93)
w4 = GameSprite('wall_2.png', 90, 416, 119, 38)
w5 = GameSprite('wall_2.png', 500, 310, 119, 38)
w6 = GameSprite('wall_2.png', 603, 310, 119, 38)
w7 = GameSprite('wall_2.png', 703, 310, 119, 38)
w8 = GameSprite('wall_2.png', 803, 310, 119, 38)
w9 = GameSprite('wall_2.png', 903, 310, 119, 38)
w10 = GameSprite('wall_2.png', 269, 240, 160, 38)
w11 = GameSprite('wall_2.png', 190, 240, 160, 38)


barriers.add(w1)
barriers.add(w2)
barriers.add(w3)
barriers.add(w4)
barriers.add(w5)
barriers.add(w6)
barriers.add(w7)
barriers.add(w8)
barriers.add(w9)
barriers.add(w10)
barriers.add(w11)

packman = Player('hero.png', 3, win_height - 110, 44, 44, 0, 0)
final_sprite = GameSprite('pac-1.png', win_width - 100, win_height - 100, 50, 50)

monster1 = Enemy('cyborg.png', 660 - 20, 270, 45, 45, 5)
monster2 = Enemy('cyborg.png', 1029 - 60, 410, 45, 45, 5)
monster3 = Enemy('cyborg.png', 880 - 60, 410, 45, 45, 5)
monster4 = Enemy('cyborg.png', 800 - 60, 410, 45, 45, 5)

monsters.add(monster1)
monsters.add(monster2)
monsters.add(monster3)
monsters.add(monster4)

finish = False

run = True
while run:
    time.delay(60)
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_a:
                packman.x_speed = -7
            if e.key == K_d:
                packman.x_speed = 7
            if e.key == K_s:
                packman.y_speed = 5
            if e.key == K_SPACE:
                packman.jump()
            if e.key == K_f:
                packman.fire()
        elif e.type == KEYUP:
            if e.key == K_a:
                packman.x_speed = 0
            if e.key == K_d:
                packman.x_speed = 0
            if e.key == K_w:
                packman.y_speed = 0
            if e.key == K_s:
                packman.y_speed = 0

    if not finish:
        window.blit(transform.scale(back, (win_width, win_height)), (0, 0))
        packman.update()
        bullets.update()
        packman.reset()
        bullets.draw(window)
        barriers.draw(window)
        final_sprite.reset()

        sprite.groupcollide(monsters, bullets, True, True)
        monsters.update()
        monsters.draw(window)
        sprite.groupcollide(bullets, barriers, True, False)

        if sprite.spritecollide(packman, monsters, False):
            finish = True
            img = image.load('over1.png')
            d = img.get_width() // img.get_height()
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_height * d, win_height)), (315, 0))

        if sprite.collide_rect(packman, final_sprite):
            finish = True
            img = image.load('thanks.jpeg')
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_width, win_height)), (0, 0))

    display.update()

