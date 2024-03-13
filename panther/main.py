import pygame
from random import randint
pygame.init()


WIDTH, HEIGHT = 1280, 760
FPS = 60
TILE = 50

DIRECTS = [[0, -1], [1, 0], [0, 1], [-1, 0]]

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
fontUI = pygame.font.Font(None, 30)
img_block = pygame.image.load('panther/images/block_brick.png')
img_tanks = [pygame.image.load('panther/images/tank1.png'),
             pygame.image.load('panther/images/tank2.png'),
             pygame.image.load('panther/images/tank3.png'),
             pygame.image.load('panther/images/tank4.png'),
             pygame.image.load('panther/images/tank5.png'),
             pygame.image.load('panther/images/tank6.png'),
             pygame.image.load('panther/images/tank7.png'),
             pygame.image.load('panther/images/tank8.png')
             ]
img_bang = [pygame.image.load('panther/images/bang1.png'),
            pygame.image.load('panther/images/bang2.png'),
            pygame.image.load('panther/images/bang3.png')]

img_bonus = [pygame.image.load('panther/images/bonus_bomb.png'),
             pygame.image.load('panther/images/bonus_helmet.png'),
             pygame.image.load('panther/images/bonus_shovel.png'),
             pygame.image.load('panther/images/bonus_star.png'),
             pygame.image.load('panther/images/bonus_tank.png'),
             pygame.image.load('panther/images/bonus_time.png')]


class User_interfeis:
    def __init__(self) -> None:
        pass

    def update(self):
        pass

    def draw(self):
        i = 0
        for obj in objects:
            if obj.type == 'tank':
                pygame.draw.rect(window, obj.color, (5+i*70, 5, 22, 22))
                
                text = fontUI.render(str(obj.helfpoint), 1, obj.color)
                rect = text.get_rect(center = (5 + i*70 +32, 5+11))
                window.blit(text, rect)
                i +=1




class Tank:
    def __init__(self, color, px, py, direct, key_list):
        objects.append(self)
        self.type = 'tank'
        self.color = color
        self.rect = pygame.Rect(px, py, TILE, TILE)
        self.direct = direct
        self.move_speed = 2 
        self.bullet_damage = 1
        self.bullet_speed = 5
        self.shot_timer = 0
        self.shot_dalay = 60
        self.helfpoint = 3 
        self.level_tank = 0
        self.image = pygame.transform.rotate(img_tanks[self.level_tank], self.direct * 90)
        self.rect = self.image.get_rect(center = self.rect.center)

        self.key_left = key_list[0]
        self.key_right = key_list[1]
        self.key_up = key_list[2]
        self.key_down = key_list[3]
        self.key_shot = key_list[4]

    def update(self):
        self.image = pygame.transform.rotate(img_tanks[self.level_tank], -self.direct * 90)
        self.image = pygame.transform.scale(self.image, (self.image.get_width()+10, self.image.get_height()+10))
        self.rect = self.image.get_rect(center = self.rect.center)
        oldX, oldY = self.rect.topleft
        if keys[self.key_left]:
            self.rect.x -= self.move_speed
            self.direct = 3
        elif keys[self.key_right]:
            self.rect.x += self.move_speed
            self.direct = 1
        elif keys[self.key_up]:
            self.rect.y -= self.move_speed
            self.direct = 0
        elif keys[self.key_down]:
            self.rect.y += self.move_speed
            self.direct = 2

        for obj in objects:
             if obj != self and obj.type == 'block' and self.rect.colliderect(obj.rect):
                self.rect.topleft = oldX, oldY 
        
        if keys[self.key_shot] and self.shot_timer == 0:
            dx = DIRECTS[self.direct][0] * self.bullet_speed   
            dy = DIRECTS[self.direct][1] * self.bullet_speed     
            Bullet(self, self.rect.centerx+1, self.rect.centery+1, dx, dy, self.bullet_damage)
            self.shot_timer = self.shot_dalay
        if self.shot_timer > 0:
            self.shot_timer -= 1
        #исправление выезда танка за границы
        if self.rect[0] < 1 or self.rect[0] > WIDTH-TILE-1 or self.rect[1] < 1 or self.rect[1] > HEIGHT-TILE-1:
            self.rect.topleft = oldX, oldY

    def draw(self):
        window.blit(self.image, self.rect)
         
    def damage(self, value):    
        self.helfpoint -= value
        if self.helfpoint <= 0:
            objects.remove(self)
            print(self.color, 'dead')

class Explogen:
    def __init__(self, px, py):
        self.px = px
        self.py = py
        objects.append(self)
        self.type = 'bang'
        self.frame = 0

    def update(self):
        self.frame += 0.2
        if self.frame >= 3:
            objects.remove(self)

    def draw(self):
        img = img_bang[int(self.frame)]
        img = pygame.transform.scale(img, (img.get_width()+10, img.get_height()+10))
        rect = img.get_rect(center = (self.px, self.py))
        window.blit(img, rect)


class Bonus:
    def __init__(self, px, py, size):
        self.px = px
        self.py = py
        self.type = 'bonus'
        self.life_time = 599
        self.image = pygame.transform.scale(img_bonus[randint(0, len(img_bonus)-1)], (size, size))
        objects.append(self)
        self.rect = pygame.Rect(px, py, size, size)


    def update(self):
        self.life_time -= 1
        for obj in objects:
            if obj.type == 'tank' and obj != self and self.rect.colliderect(obj.rect):
                if obj.level_tank < 7:
                    obj.level_tank +=1
                    obj.move_speed += 0.2
                    obj.helfpoint += 1
                objects.remove(self)

    def draw(self):
        if self.life_time % 30 != 0 and self.life_time + 1 % 30 != 0 and  self.life_time + 2 % 30 != 0:
            window.blit(self.image, self.rect )



class Bullet:
    def __init__(self, parent, px, py, dx, dy, damage) -> None:
        bullets.append(self)
        self.px, self.py = px, py
        self.parent = parent
        self.dx, self.dy = dx, dy
        self.damage = damage

    def update(self):
        self.px += self.dx
        self.py += self.dy
        if self.px < 0 or self.px > WIDTH or self.py < 0 or self.py > HEIGHT:
            bullets.remove(self)
        else:
            for obj in objects:
                if obj != self.parent and obj.type != ('bang') and obj.type != ('bonus') and obj.rect.collidepoint(self.px, self.py):
                    obj.damage(self.damage)
                    bullets.remove(self)
                    Explogen(self.px, self.py)
                    break                     

    def draw(self):
        pygame.draw.circle(window, 'yellow', (self.px, self.py), 2)


class Block:
        def __init__(self, px, py, size):
            objects.append(self)
            self.type = 'block'
            self.rect = pygame.Rect(px, py, size, size)
            self.helfpoint = 1

        def update(self):
            pass

        def draw(self):
            self.image = pygame.transform.scale(img_block, (img_block.get_width()+18, img_block.get_height()+18))
            window.blit(self.image, self.rect)
            

        def damage(self, value):
            self.helfpoint -= value
            if self.helfpoint <= 0:
                objects.remove(self)

        
bullets = []
objects = []
Tank('blue', 100, 275, 0, (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_SPACE ))
Tank('red', 650, 275, 0, (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_KP_ENTER ))
ui = User_interfeis()
for _ in range(WIDTH * HEIGHT// 1024 // 10):
    while True:
        x = randint(0, WIDTH//TILE - 1) * TILE
        y = randint(0, HEIGHT//TILE - 1) * TILE
        rect = pygame.Rect(x, y, TILE, TILE)
        fined = False
        for obj in objects:
            if rect.colliderect(obj.rect):
                fined = True
        if not fined:
             break
            
    Block(x, y, TILE)


play = True
while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
    if randint(0, 1800) < 1:
        bon = Bonus( randint(0, WIDTH//TILE - 1) * TILE,  randint(0, WIDTH//TILE - 1) * TILE, TILE)

    keys = pygame.key.get_pressed()
                
    for bullet in bullets:
        bullet.update()

    for obj in objects:
        obj.update()

    ui.update()
    
    window.fill('black')

    for bullet in bullets:
        bullet.draw()
    
    for obj in objects:
        obj.draw()

    ui.draw()


    pygame.display.update()
    clock.tick(FPS)

pygame.quit()