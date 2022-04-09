from pygame import *
from random import randint 
from time import time as timer
#музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

#шрифты и надписи
font.init()
font1 = font.SysFont('Arial', 80)
win = font1.render('умничка<3', True, (255, 255, 255))
lose = font1.render('не сдавайся', True, (180, 255, 0))
font2 =font.SysFont('Arial', 36)


img_back = 'galaxy.jpg'
img_hero = 'rocket.png'
img_enemy = "ufo.png"
img_bullet = 'bullet.png'
img_enemy2 = 'rufs.png'
img_ast = "asteroid.png"


score = 0
goal = 50 
lost = 0
max_lost = 3
life = 3

#класс родитель для спрайтов
class GameSprite(sprite.Sprite):
    #конструктор класа
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):

        sprite.Sprite.__init__(self)

        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image),(size_x, size_y))
        self.speed = player_speed

        # каждый спрайт должен хранить свойство rect прямоугольник в котопрый он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# класс наслденик для спрайта игрока (управляется стрелочками)
class Player(GameSprite):

    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

#враг
class Enemy(GameSprite):
    #движение врага
    def update(self):
        self.rect.y += self.speed
        global lost
        #исчезает если дойдет до края экрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Enemy2(GameSprite):
    #движение 
    side = 'left'
    def update(self):
        if self.rect.x <= 10:
            self.side = 'right'
        if self.rect.x >= win_width - 85:
            self.side = 'left'
        if self.side == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

#пули
class Bullet(GameSprite):
    #движение врага
    def update(self):
        self.rect.y += self.speed
        #исчезает если дойдет до конца экрана
        if self.rect.y < 0:
            self.kill()
        
        
win_width = 700
win_height = 500
display.set_caption('Shooter')
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)

monsters2 = sprite.Group()
for i in range(1, 3):
    monster2 = Enemy2(img_enemy2, randint(10, 150), randint(10, 200), 100, 100, randint(10, 25))
    monsters2.add(monster2)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 7))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1, 3):
    asteroid = Enemy(img_ast, randint(80, win_width - 30), -40, 80, 50, randint(2, 7))
    asteroids.add(asteroid)


bullets = sprite.Group()
#
finish = False
#
run = True

rel_time = False

num_fire = 0

while run:
    
    for e in  event.get():
        if e.type == QUIT:
            run = False
        #
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                #fire_sound.play()
                ship.fire()

            if num_fire < 5 and rel_time == False:
                num_fire = num_fire + 1
                fire_sound.play()
                ship.fire()

            if num_fire >= 5 and rel_time == False:
                last_time = timer()
                rel_time = True
                

    if not finish:
        #ОБНОВЛЯЕМ ФОН
        window.blit(background,(0,0))

        #пишем текст на экране
        text = font2.render('Cчет:' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render('Пропущено:' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        #производим движение спрайтов
        ship.update()
        monsters.update()
        monsters2.update()
        bullets.update()
        asteroids.update()

        #обновляем их  в новом местоположении при каждой итерации цикла
        ship.reset()
        monsters2.draw(window)
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        #
        if rel_time == True:
            now_time = timer()

            if now_time - last_time <3:
                reload = font2.render('Wait, reload...', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        #проверка стоолкновений пули и монстров
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            #
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

        collides2 = sprite.groupcollide(monsters2, bullets, True, True)
        for c in collides2:
            #
            score = score + 2 
            monster2 = Enemy2(img_enemy2, randint(10, 150), randint(100, 200), 100, 100, randint(10, 25))
            monsters2.add(monster2)

        #
        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True)
            sprite.spritecollide(ship, asteroids, True)
            life = life - 1


        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 0, 0)
        if life == 1:
            life_color = (0, 0, 150)

        text_life = font1.render(str(life),1 , life_color)
        window.blit(text_life, (650, 10))

        display.update()

        #
        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        #
        if score >= goal:
            finish = True 
            window.blit(win, (200, 200)) 

        #
        text = font2.render('Счет:' + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))

        text_lose = font2.render('Пропущено:' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        display.update()

    else:
        finish = False
        score = 0
        lost = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for v in monsters2:
            v.kill()

            # цикл срабатывает каждую 0.05 сек
        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)

    time.delay(50)