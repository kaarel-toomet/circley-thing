import pygame as pg
import random as r
import sys
pg.init()
pg.mixer.init()
pic = pg.image.load("trollface.png")
pg.font
screen = pg.display.set_mode((0,0), pg.RESIZABLE)
screenw = screen.get_width()
screenh = screen.get_height()
pg.display.set_caption("movepic")
do = True
dist = 8
up = True
down = True
left = True
right = True
mup = False
mdown = False
mleft = False
mright = False
timer = pg.time.Clock()
lifes = 5
pickiness = 42
font = pg.font.SysFont("Times", 24)
dfont = pg.font.SysFont("Times", 32)
pfont = pg.font.SysFont("Times", 50)
pause = False
gameover = False
player = pg.sprite.Group()
class Player(pg.sprite.Sprite):
    def __init__(self,x,y):
        pg.sprite.Sprite.__init__(self)
        self.image = pic
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self, mup, mdown, mleft, mright):
        if self.rect.y <= 0:
            up = False
        else:
            up = True
        if self.rect.y >= screenh-100:
            down = False
        else:
            down = True
        if self.rect.x <= 0:
            left = False
        else:
            left = True
        if self.rect.x >= screenw-124:
            right = False
        else:
            right = True
        if mup and up:
            self.rect.y -= dist 
        if mdown and down:
            self.rect.y += dist
        if mleft and left:
            self.rect.x -= dist
        if mright and right:
            self.rect.x += dist
class Disc(pg.sprite.GroupSingle):
    def __init__(self, x, y, xvel, yvel,r,g,b,wr,wg,wb,pickiness=pickiness):
        d = pg.sprite.Sprite()
        pg.sprite.GroupSingle.__init__(self, d)
        self.x = x
        self.y = y
        self.xvel = xvel
        self.yvel = yvel
        self.r = r
        self.g = g
        self.b = b
        self.wr = wr
        self.wg = wg
        self.wb = wb
        self.pickiness = pickiness
        self.sprite.rect = pg.rect.Rect(x,y,20,20)
    def update(self):
        if self.x + self.xvel <= screenw-90 and self.x + self.xvel >= 0:
            self.x += self.xvel
            self.x = int(self.x)
        else:
            self.xvel = -self.xvel
        if self.y + self.yvel <= screenh-90 and self.y + self.yvel >= 0:
            self.y += self.yvel
            self.y = int(self.y)
        else:
            self.yvel = -self.yvel
        self.sprite.rect = pg.rect.Rect(self.x,self.y,20,20)
    def drw(self):
        pg.draw.circle(screen,(self.r,self.g,self.b),(self.x,self.y),20)
def reset():
    lifes = 5
    #player.empty()
    hullmyts = Player(screenw/2,screenh/2)
    player.add(hullmyts)
#hullmyts = Player(screenw/2,screenh/2)
#player.add(hullmyts)

discs = [ Disc(r.randint(100,screenw-190),r.randint(100,screenh-190),
               r.randint(-10,10),r.randint(-10,10),
               r.randint(0,255),r.randint(0,255),r.randint(0,255),
               r.randint(0,255),r.randint(0,255),r.randint(0,255))
            for i in range(5)]

while do:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            do = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                mup = True
            elif event.key == pg.K_DOWN:
                mdown = True
            elif event.key == pg.K_LEFT:
                mleft = True
            elif event.key == pg.K_RIGHT:
                mright = True
            elif event.key == pg.K_p:
                pause = True
            elif event.key == pg.K_r:
                reset()
        elif event.type == pg.KEYUP:
            if event.key == pg.K_UP:
                mup = False
            elif event.key == pg.K_DOWN:
                mdown = False
            elif event.key == pg.K_LEFT:
                mleft = False
            elif event.key == pg.K_RIGHT:
                mright = False
    while pause:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pause = False
                do = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_p:
                    pause = False
        pd = "PAUSED"
        ptext = dfont.render(pd, True, (0,0,0))
        ptext_rect = ptext.get_rect()
        ptext_rect.centerx = screen.get_rect().centerx
        ptext_rect.y = 50
        screen.blit(ptext,ptext_rect)
        screen.blit(text,text_rect)
        pg.display.update()
    if lifes == 0:
        uded = "GAME OVER"
        dtext = dfont.render(uded, True, (255,0,0))
        dtext_rect = dtext.get_rect()
        dtext_rect.centerx = screen.get_rect().centerx
        dtext_rect.y = 30
        screen.blit(dtext,dtext_rect)
        screen.blit(text,text_rect)
        pg.display.update()
        gameover = True
    while gameover:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                gameover = False
                do = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    gameover = False
                    reset()
    for i1, disc1 in enumerate(discs):
        for i2, disc2 in enumerate(discs):
            if disc1 is disc2:
                #print("slef", i1, i2)
                continue
            col = pg.sprite.spritecollide(disc1.sprite,disc2,False)
            #print(disc1,disc2, i1, i2)
            #print(col)
            if len(col) > 0:
                print(disc1.x, disc2.x)
                #sys.exit(0)
    screen.fill((128,128,128))
    score = ("Lifes: " + str(lifes))
    text = font.render(score, True, (255,255,255))
    text_rect = text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.y = 10
    screen.blit(text,text_rect)
    for disc in discs:
        disc.update()
        disc.drw()
    player.update(mup, mdown, mleft, mright)
    player.draw(screen)
    pg.display.update()
    timer.tick(60)

pg.quit()
