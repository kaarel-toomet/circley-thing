import pygame as pg
import random as r
import sys
pg.init()
pg.mixer.init()
pop = pg.mixer.Sound("pop.wav")
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
pickiness = 192
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
    def __init__(self, x, y, xvel, yvel, r, g, b, wr, wg, wb, umtick = 0):
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
        self.umtick = umtick
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
        if self.umtick > 0:
            self.umtick -= 1
    def drw(self):
        pg.draw.circle(screen,(round(self.r),round(self.g),round(self.b)),(self.x,self.y),20)
    def getumt(self):
        return self.umtick
    def addumt(self,addedticks):
        self.umtick += addedticks
    def gclrwclr(self):
        return [self.r,self.g,self.b,self.wr,self.wg,self.wb]
    def aclrwclr(self,m8clrs):
        self.r = (self.r+m8clrs[0])/2
        self.g = (self.g+m8clrs[1])/2
        self.b = (self.b+m8clrs[2])/2
        self.wr = (self.wr+m8clrs[3])/2
        self.wg = (self.wg+m8clrs[4])/2
        self.wb = (self.wb+m8clrs[5])/2
    def mutate(self,amount):
        self.r += round(r.normalvariate(0,amount))
        self.g += round(r.normalvariate(0,amount))
        self.b += round(r.normalvariate(0,amount))
        self.wr += round(r.normalvariate(0,amount))
        self.wg += round(r.normalvariate(0,amount))
        self.wb += round(r.normalvariate(0,amount))
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
            for i in range(42)]

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
            if i2 <= i1:
                continue
            col = pg.sprite.spritecollide(disc1.sprite,disc2,False)
            if len(col) > 0:# and disc1.getumt() == 0 and disc2.getumt() == 0:
                disc1.addumt(60)
                disc2.addumt(60)
                d1c = disc1.gclrwclr()
                d2c = disc2.gclrwclr()
                m81r = False
                m81g = False
                m81b = False
                m82r = False
                m82g = False
                m82b = False
                for ir1 in range(round(d1c[0]-pickiness),round(d1c[0]+pickiness)):
                    if ir1 == d2c[3]:
                        m82r = True
                        break
                for ig1 in range(round(d1c[1]-pickiness),round(d1c[1]+pickiness)):
                    if ig1 == d2c[4]:
                        m82g = True
                        break
                for ib1 in range(round(d1c[2]-pickiness),round(d1c[2]+pickiness)):
                    if ib1 == d2c[5]:
                        m82b = True
                        break
                for ir2 in range(round(d2c[0]-pickiness),round(d2c[0]+pickiness)):
                    if ir2 == d1c[3]:
                        m81r = True
                        break
                for ig2 in range(round(d2c[1]-pickiness),round(d2c[1]+pickiness)):
                    if ig2 == d1c[4]:
                        m81g = True
                        break
                for ib2 in range(round(d2c[2]-pickiness),round(d2c[2]+pickiness)):
                    if ib2 == d1c[5]:
                        m81b = True
                        break
                if m81r and m81g and m81b and m82r and m82g and m82b:
                    disc1.aclrwclr(d2c)
                    disc2.aclrwclr(d1c)
                    disc1.mutate(10)
                    disc2.mutate(10)
                    pop.play()
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
    #timer.tick(60)

pg.quit()
