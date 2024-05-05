import os
from pygame import *
from random import randint
from time import time as tm

def getRandomColor():
    return (randint(0, 255), randint(0, 255), randint(0, 255))
def get_window_size():
    return [1050, 750]

class GameSprite(sprite.Sprite):
    def __init__(self, image_, x, y, speed, width=80, height=80):
        super().__init__()
        self.image = transform.scale(image.load(image_), (width, height))
        self.rect = self.image.get_rect()        
        self.speed = speed
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def __init__(self, image, speed, playerNum=1, isAI=0):#
        super().__init__(image, 0, 0, speed, 30, 90)
        self.playerNum = playerNum
        self.isAI = isAI #
        self.goStart()    
    def update(self):
        keys = key.get_pressed()
        speedBonus = curTime // 15
        if self.isAI:
            if ball.rect.y < self.rect.y and self.rect.y > self.speed:
                self.rect.y -= self.speed + speedBonus
            if ball.rect.y > self.rect.y and self.rect.y < 750 - self.rect.height - self.speed:
                self.rect.y += self.speed + speedBonus 
        else:        
            if self.playerNum == 1:
                if keys[K_w] and self.rect.y > self.speed:
                    self.rect.y -= self.speed + speedBonus
                if keys[K_s] and self.rect.y < 750 - self.rect.height - self.speed:
                    self.rect.y += self.speed + speedBonus 
            else:
                if keys[K_UP] and self.rect.y > self.speed:
                    self.rect.y -= self.speed + speedBonus
                if keys[K_DOWN] and self.rect.y < 750 - self.rect.height - self.speed:
                    self.rect.y += self.speed + speedBonus             
    def goStart(self):
        if self.playerNum == 1:
            self.rect.x = 0
        else:
            self.rect.x = 1050 - self.rect.width
        self.rect.y = (750 - self.rect.height) // 2
class Ball(GameSprite):
    def __init__(self, image, width=30, height=30):
        wndWidth, wndHeight = get_window_size()
        x = (wndWidth - width) // 2
        y = (wndHeight - height) // 2
        speed = 5
        super().__init__(image, x, y, speed, width, height)
        self.getDirection()        
    def getDirection(self):
        lst = [-1, 1]
        self.speedX = self.speed * lst[randint(0, 1)]
        self.speedY = self.speed * lst[randint(0, 1)]
    def update(self):
        self.speedX = self.speedX / abs(self.speedX) * self.speed
        self.speedY = self.speedY / abs(self.speedY) * self.speed
        self.rect.y += self.speedY
        self.rect.x += self.speedX
        wndWidth, wndHeight = get_window_size()
        if self.rect.y >= (wndHeight - self.rect.height):
            self.rebound(1, -1)
        if self.rect.y <= 0:
            self.rebound(1, -1) 
        if self.rect.x >= (wndWidth - self.rect.width):
            global score1
            score1 += 1
            self.respawn()
        if self.rect.x <= 0:
            global score2
            score2 += 1   
            self.respawn()         
    def rebound(self, mX, mY):
        self.speedX *= mX
        self.speedY *= mY
    def respawn(self):
        wndWidth, wndHeight = get_window_size()
        self.rect.x = (wndWidth - self.rect.width) // 2
        self.rect.y = (wndHeight - self.rect.height) // 2
        self.getDirection()
#создай окно игры
os.environ['SDL_VIDEO_CENTERED'] = '1'
window = display.set_mode((1050, 750))
display.set_caption('Пинг-понг')
#задай фон сцены
background = transform.scale(image.load('cnjk.jpg'), (1050, 750))
#создай 2 спрайта и размести их на сцене
players = sprite.Group()
players.add(Player('ракетка1.png', 10, 1))
players.add(Player('ракетка2.png', 10, 2, 1))

ball = Ball('ball.png', 30, 30)
#работа со звуками
'''
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire = mixer.Sound('fire.ogg')
'''
#обработай событие «клик по кнопке "Закрыть окно"»
gameOver = False
finish = 3 #0-играем 1-выиграл левый 2-выиграл правый 3-меню
clock = time.Clock()
FPS = 60
font.init()
fnt = font.Font(None, 170)
fntMidle = font.Font(None, 70)
fntSmall = font.Font(None, 35)
win = fnt.render('PLAYER1 WON', True, (200, 0, 0))
lose = fnt.render('PLAYER2 WON', True, (0, 0, 200))
menu = fntMidle.render('1 - игра с ИИ  2 - игра вдвоём  3 - ИИ с ИИ', True, (0, 0, 0))
score1 = 0
score2 = 0
curTime = 0 
timeBegin = tm()# запоминаем время начала игры
while not gameOver:
    window.blit(background, (0, 0))
    events = event.get()
    for ev in events:
        if ev.type == QUIT:
            gameOver = True
    if not finish:
        players.update()
        players.draw(window)
        ball.update()
        ball.reset()
        collideList = sprite.spritecollide(ball, players, False)#####
        if len(collideList) > 0:
            if (ball.rect.x <= (30-ball.speed-1)) or (ball.rect.x >= 1050-(30-ball.speed-1)-ball.rect.width):
                ball.rebound(-1, -1)
            else:
                ball.rebound(-1, 1)
        if score1 >= 5:
            finish = 1
        if score2 >= 5:
            finish = 2
        curTime = round(tm() - timeBegin, 1)
        ball.speed = 5 + curTime // 10
    else:
        keys = key.get_pressed()
        if (finish == 3): #если меню
            if keys[K_1]:
                for player in players:
                    if player.playerNum == 2:
                        player.isAI = 1
                    else:
                        player.isAI = 0
                finish = 0
                timeBegin = tm()
            if keys[K_2]:
                for player in players:
                        player.isAI = 0
                finish = 0
                timeBegin = tm() 
            if keys[K_3]:
                for player in players:
                        player.isAI = 1
                finish = 0
                timeBegin = tm()                                  
        if (finish in (1, 2)) and keys[K_r]:
            for player in players:
                player.goStart()
            ball.speed = 5
            ball.respawn()
            finish = 3
            score1 = 0 ###
            score2 = 0 ###
            timeBegin = tm()
    if finish == 1:
        window.blit(win, (100, 300))
    elif finish == 2:
        window.blit(lose, (100, 300))
    elif finish == 3:
        window.blit(menu, ((1050 - menu.get_width())//2, (750 - menu.get_height())//2))
    scoreText = fntMidle.render(str(score1) + ':' + str(score2), True, (255, 255, 255))
    window.blit(scoreText, ((1050 - scoreText.get_width()) // 2, 0))
    timeText = fntSmall.render(str(curTime), True, (255, 255, 0))
    window.blit(timeText, ((1050 - timeText.get_width()) // 2, 40))
    display.update()
    clock.tick(FPS)