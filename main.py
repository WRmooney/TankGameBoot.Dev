import sys
sys.modules['pygame.sndarray'] = None

import pygame.display
import pygame.image
import pygame.mixer
import pygame.time
import pygame.event
import pygame.key
import pygame.mouse
import pygame.sprite
import pygame.rect
import pygame.font
import random
import math
import os

from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement
from PIL import Image
import numpy as np



def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and PyInstaller """
    try:
        base_path = sys._MEIPASS  # PyInstaller sets this at runtime
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def loadify(imgname):
    """ For Loading Sprites more Efficiently """
    return pygame.image.load(resource_path(imgname)).convert_alpha()

#colors
floor=(196,164,132)
wall=(181,101,29)
darkwall=(90,50,15)

pygame.font.init()

mainfontbig = pygame.font.Font(resource_path("Assets/Fonts/NoContinue.ttf"), 75)
mainfontmed = pygame.font.Font(resource_path("Assets/Fonts/NoContinue.ttf"), 50)
mainfontsm = pygame.font.Font(resource_path("Assets/Fonts/NoContinue.ttf"), 35)
bossfont1 = pygame.font.Font(resource_path("Assets/Fonts/Horror.otf"), 100)
joshfont = pygame.font.Font(resource_path("Assets/Fonts/Boss2.ttf"), 125)
titlefont = pygame.font.Font(resource_path("Assets/Fonts/Title.ttf"), 150)


pygame.init()
pygame.mixer.init()




screen_width = 1300
screen_height = 900



screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Tank Game")
pygame.display.set_icon(loadify("Assets/Sprites/logo.png"))
timer = pygame.time.Clock()


gamestate="mainmenu"

score = 0
running = True

levelgrid=[
  [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
  [1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1],
  [1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
  [1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
  [1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
  [1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
  [1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
  [1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1],
  [1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]


# define classes
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.pos = pygame.Vector2(x, y)
        self.image = pygame.Surface((20, 20))
        self.image.fill((49, 125, 255))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 3
        self.color = (49, 125, 255)
        self.og_cannon = loadify('Assets\Sprites\BlueTank.png')
        self.cannon = self.og_cannon
        self.cannon_ang=0
        self.cannon_rect = self.cannon.get_rect(center=self.rect.center)
        self.bulletgroup = pygame.sprite.Group()
        self.maxbullets = 5
        self.location = findcoordinate(x,y)
        self.bulletspeed = 5
        tanks.add(self)
        self.canhitself = True
        self.start_lives = lives

    def move(self, dx, dy):
        # Move along X axis
        self.pos.x += dx/5
        self.rect.x = int(self.pos.x)
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0:
                    self.rect.right = wall.rect.left
                    self.pos.x = self.rect.x
                elif dx < 0:
                    self.rect.left = wall.rect.right
                    self.pos.x = self.rect.x
        for tank in tanks:
            if self.rect.colliderect(tank.rect) and tank is not self:
                if dx > 0:
                    self.rect.right = tank.rect.left
                    self.pos.x = self.rect.x
                elif dx < 0:
                    self.rect.left = tank.rect.right
                    self.pos.x = self.rect.x
        # Move along Y axis
        self.pos.y += dy/5
        self.rect.y = int(self.pos.y)
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dy > 0:
                    self.rect.bottom = wall.rect.top
                    self.pos.y = self.rect.y
                elif dy < 0:
                    self.rect.top = wall.rect.bottom
                    self.pos.y = self.rect.y
        for tank in tanks:
            if self.rect.colliderect(tank.rect) and tank is not self:
                if dy > 0:
                    self.rect.bottom = tank.rect.top
                    self.pos.y = self.rect.y
                elif dy < 0:
                    self.rect.top = tank.rect.bottom
                    self.pos.y = self.rect.y

    def update(self):
        for i in range(5):
            self.move(dx,dy)
        self.mousepos = pygame.mouse.get_pos()
        self.diffx = self.mousepos[0] - self.pos.x
        self.diffy = -(self.mousepos[1] - self.pos.y)
        self.mouseangle = math.atan2(self.diffy, self.diffx)
        self.cannon_ang = math.degrees(self.mouseangle)-90
        self.cannon = pygame.transform.rotate(self.og_cannon, self.cannon_ang)
        self.cannon_rect = self.cannon.get_rect(center=self.rect.center)
        self.location = findcoordinate(self.pos.x,self.pos.y)
        self.draw(screen)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        screen.blit(self.cannon, (self.cannon_rect.x, self.cannon_rect.y))

    def primaryfire(self):
        if len(self.bulletgroup)<self.maxbullets:
            self.bullet = Bullet(self.rect.center[0] + math.cos(self.mouseangle)*20, self.rect.center[1]-math.sin(self.mouseangle)*20, self.mouseangle, self.bulletspeed, 1)
            self.bulletgroup.add(self.bullet)
            bulletgroup.add(self.bullet)

    def got_hit(self):
        global gamestate
        global deathx
        global deathy
        global tick
        tick=0
        gamestate = "died"
        deathx = self.pos.x
        deathy = self.pos.y

class Explosion(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.x, self.y = x-25,y-25
        self.f1 = loadify("Assets/Sprites/frame1.png")
        self.f2 = loadify("Assets/Sprites/frame2.png")
        self.f3 = loadify("Assets/Sprites/frame3.png")
        self.frametick = 0
        self.image = self.f1
        self.sound = pygame.mixer.Sound(resource_path("Assets/Audio/SFX/explode.wav"))
        self.sound.set_volume(0.5)
        pygame.mixer.Sound.play(self.sound)

    def update(self):

        if self.frametick == 3:
            self.image = self.f2
        elif self.frametick == 6:
            self.image = self.f3
        elif self.frametick == 9:
            self.image = self.f2
        elif self.frametick == 12:
            self.image = self.f1
        elif self.frametick == 15:
            self.kill()
        self.frametick += 1
        self.draw()


    def draw(self):
        screen.blit(self.image, (self.x, self.y))

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((25,25))
        self.rect = self.image.get_rect(topleft=(x,y))

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y,ang,speed, bounces, collideself=True):
        super().__init__()
        self.size = 8
        self.image = pygame.Surface((self.size,self.size))
        self.rect = self.image.get_rect(center=(x,y))
        self.angle = ang
        self.pos = pygame.Vector2(x, y)
        self.speed=speed
        self.bounces = bounces
        self.dx = math.cos(self.angle) * self.speed
        self.dy = -math.sin(self.angle)*self.speed
        self.invincible = True
        self.invincibility_tick = 0
        self.has_hit = False
        self.invincibility_time = 1
        self.collideself = collideself
        self.shootsound = pygame.mixer.Sound(resource_path("Assets/Audio/SFX/shoot.wav"))
        self.shootsound.set_volume(0.5)
        pygame.mixer.Sound.play(self.shootsound)

    def update(self):
        if self.invincible:
            self.invincibility_tick += 1
        if self.invincibility_tick > self.invincibility_time:
            self.invincible = False
        for i in range(self.speed*2):
            self.move()
            if not self.has_hit:
                self.checkcollision()
        self.draw(screen)

    def move(self):
        self.pos.x += self.dx*(1/(2*self.speed))
        self.pos.y += self.dy*(1/(2*self.speed))
        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y

    def draw(self, surface):

        pygame.draw.circle(surface,(0,0,0),(self.pos.x,self.pos.y),self.size/2)
        #pygame.draw.rect(surface, (255,255,255), self.rect)

    def checkcollision(self):
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.bounces -= 1
                self.bounce(wall)
        if self.bounces < 0:
            self.eradicate()
        for bullet in bulletgroup:
            if self.rect.colliderect(bullet.rect) and bullet!=self:
                if self.collideself or bullet in player.bulletgroup:
                    if not isinstance(bullet, BigBullet):
                        bulletgroup.remove(bullet)
                        bullet.eradicate()
                    if not isinstance(self, BigBullet):
                        bulletgroup.remove(self)
                        self.eradicate()
        for tank in tanks:
            if self.rect.colliderect(tank.rect): # if the bullet collides with the tank
                if self in tank.bulletgroup: # if the tank shot the bullet
                    if not tank.canhitself: # and the tank isnt allowed to hit itself, then nothing happens
                        continue
                self.has_hit = True # bullet was not fired by self, and if it was, it is allowed to hit itself
                tank.got_hit()
                self.eradicate()
                break

    def eradicate(self):
        self.kill()

    def bounce(self,wall):

        # Store previous position before collision
        prev_rect = self.rect.copy()
        prev_rect.x -= self.dx
        prev_rect.y -= self.dy

        # Calculate overlaps in X and Y
        dx_overlap = min(self.rect.right, wall.rect.right) - max(self.rect.left, wall.rect.left)
        dy_overlap = min(self.rect.bottom, wall.rect.bottom) - max(self.rect.top, wall.rect.top)

        # Determine which axis has smaller overlap
        if dx_overlap < dy_overlap:
            # Hit from left/right
            self.dx *= -1
            if self.dx > 0:
                self.rect.left = wall.rect.right
            else:
                self.rect.right = wall.rect.left
        else:
            # Hit from top/bottom
            self.dy *= -1
            if self.dy > 0:
                self.rect.top = wall.rect.bottom
            else:
                self.rect.bottom = wall.rect.top

        self.bouncesound = pygame.mixer.Sound(resource_path("Assets/Audio/SFX/bounce.mp3"))
        self.bouncesound.set_volume(0.5)
        pygame.mixer.Sound.play(self.bouncesound)

class BigBullet(Bullet):
    def __init__(self, x, y, angle, speed, bounces):
        super().__init__(x,y,angle,speed,bounces)
        self.size = 20
        self.image = pygame.Surface((self.size, self.size))
        self.rect = self.image.get_rect(center=(x, y))
        self.invincibility_time = 5

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.pos = pygame.Vector2(x, y)
        self.image = pygame.Surface((20, 20))
        self.image.fill((0,0,0))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 2
        self.turnspeed = 4
        self.color = (150,0,0)
        self.location = findcoordinate(x,y)
        self.start = None
        self.end = None
        self.dx = 0
        self.dy = 0
        self.next_x = self.pos.x
        self.next_y = self.pos.y
        self.og_cannon = loadify('Assets/Sprites/BlackTank.png')
        self.cannon = self.og_cannon
        self.cannon_ang = 0
        self.cannon_rect = self.cannon.get_rect(center=self.rect.center)
        tanks.add(self)
        self.path = None
        self.rotate_tick = 0
        self.rotate_time = 0
        self.rotate_direction = 0
        self.accuracy = 50
        self.maxbullets = 3
        self.firerate = 30
        self.shoottick = 0
        self.firechance = 3
        self.bulletspeed = 5
        self.bullettype = 0
        self.bulletgroup = pygame.sprite.Group()
        self.bounces = 0
        self.maxhealth = 1
        self.health = self.maxhealth
        self.boss = False
        self.name = None
        self.patroltick = 0
        self.patroltime = 60
        self.patrol = True
        self.aggressiveness = 1.25
        self.canhitself = False

    def update(self):


        self.start = grid.node(self.location[0], self.location[1])
        self.end = grid.node(player.location[0], player.location[1])
        finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
        self.path, self.runs = finder.find_path(self.start, self.end, grid)


        self.cannon = pygame.transform.rotate(self.og_cannon, self.cannon_ang-90)
        self.cannon_rect = self.cannon.get_rect(center=self.rect.center)

        # Fire tick
        self.shoottick += 1
        if self.shoottick > self.firerate:
            self.shoottick = 0

        self.ai()

        self.draw()

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.cannon, (self.cannon_rect.x, self.cannon_rect.y))

        if self.maxhealth > 1:
            # change healthbar color depending on health percentage
            if self.health > self.maxhealth / 2:
                hbcolor = (100, 255, 100)
            elif self.health > self.maxhealth / 4:
                hbcolor = (255, 255, 50)
            else:
                hbcolor = (255, 50, 50)

            # draw healthbar
            if self.boss:
                pygame.draw.rect(screen, hbcolor, [315, 145, 690 * (self.health / self.maxhealth), 75])
                bosstxt = joshfont.render(self.name, True, (0,0,0))
                bossrect = bosstxt.get_rect(center=(650,70))
                screen.blit(bosstxt, bossrect)
            else:
                pygame.draw.rect(screen, hbcolor, [self.pos.x - 5, self.pos.y + 25, 30 * (self.health / self.maxhealth), 5])

    def pathtoplayer(self):
        if len(self.path) < 2:
            return
        if self.path and len(self.path) >= 2:
            self.next_x, self.next_y = self.path[1]  # [0] is current pos
            self.next_x, self.next_y = coord_to_pixel(self.next_x, self.next_y)
            self.move_toward(self.next_x, self.next_y)

            # Pathfinding debugging, displays the AI path
            """
            for i in range(len(self.path)-1):
                x, y = self.path[i]
                x2, y2 = self.path[i+1]
                x,y = coord_to_pixel(x,y)
                x2,y2 = coord_to_pixel(x2,y2)
                pygame.draw.line(screen, (0,0,0),(x+13,y+13),(x2+13,y2+13))
            """

        while len(self.path) >= 1:
            dir_vector = pygame.Vector2(self.next_x - self.rect.centerx, self.next_y - self.rect.centery)
            distance = dir_vector.length()

            if distance < 50:  # Close enough to tile
                self.path.pop(0)  # Move to next tile in path
            else:
                break

        self.move_toward(self.pos.x, self.pos.y)


        # prevent diagonal being faster
        if self.dy != 0 and self.dx != 0:
            self.dy *= 0.7
            self.dx *= 0.7

    def move(self):

        for i in range(5):
            # Move along X axis
            self.pos.x += self.dx/5
            self.rect.x = int(self.pos.x)
            for wall in walls:
                if self.rect.colliderect(wall.rect):
                    if self.dx > 0:
                        self.rect.right = wall.rect.left
                        self.pos.x = self.rect.x
                    elif self.dx < 0:
                        self.rect.left = wall.rect.right
                        self.pos.x = self.rect.x
            for tank in tanks:
                if self.rect.colliderect(tank.rect) and tank is not self:
                    if self.dx > 0:
                        self.rect.right = tank.rect.left
                        self.pos.x = self.rect.x
                    elif self.dx < 0:
                        self.rect.left = tank.rect.right
                        self.pos.x = self.rect.x
            # Move along Y axis
            self.pos.y += self.dy/5
            self.rect.y = int(self.pos.y)
            for wall in walls:
                if self.rect.colliderect(wall.rect):
                    if self.dy > 0:
                        self.rect.bottom = wall.rect.top
                        self.pos.y = self.rect.y
                    elif self.dy < 0:
                        self.rect.top = wall.rect.bottom
                        self.pos.y = self.rect.y
            for tank in tanks:
                if self.rect.colliderect(tank.rect) and tank is not self:
                    if self.dy > 0:
                        self.rect.bottom = tank.rect.top
                        self.pos.y = self.rect.y
                    elif self.dy < 0:
                        self.rect.top = tank.rect.bottom
                        self.pos.y = self.rect.y

    def check_LOS(self):
        for wall in walls:
            if wall.rect.clipline(self.pos, player.pos):
                return False
        for enemy in enemies:
            if enemy.rect.clipline(self.pos, player.pos) and enemy is not self:
                return False
        return True

    def aim_at_player(self):


        # Rotate towards player using math
        self.x_diff = player.pos.x - self.pos.x
        self.y_diff = player.pos.y - self.pos.y
        self.goal_angle = -math.degrees(math.atan2(self.y_diff, self.x_diff))+360

        # chooses which direction is closer to turn, adjusts angle accordingly
        if self.cannon_ang > self.goal_angle:
            if self.cannon_ang - self.goal_angle > 180:
                self.goal_angle += 360
        elif self.cannon_ang < self.goal_angle:
            if self.goal_angle - self.cannon_ang > 180:
                self.goal_angle -= 360


        # Prevent crazy angle numbers
        if self.cannon_ang > 360:
            self.cannon_ang -= 360
        elif self.cannon_ang < 0:
            self.cannon_ang += 360

        # Turn towards the player, mutliple times to prevent overcorrection
        for i in range(4):
            if self.cannon_ang < self.goal_angle:
                self.cannon_ang += 0.25*self.turnspeed
            elif self.cannon_ang > self.goal_angle:
                self.cannon_ang -= 0.25*self.turnspeed

    def ai(self):
        self.patroltick += 1
        #print(pygame.Vector2(player.rect.centerx - self.rect.centerx, player.rect.centery - self.rect.centery).length())
        if not self.patrol and pygame.Vector2(player.rect.centerx - self.rect.centerx, player.rect.centery - self.rect.centery).length() < 350:
            self.pathtoplayer()

            if self.patroltick == self.patroltime:
                self.patrol = True
                self.patroltick = 0
                self.patroltime = random.randint(round(30/self.aggressiveness),round(120/self.aggressiveness))

        else:
            if self.patroltick == self.patroltime:
                self.patrol = False
                self.patroltick = 0
                self.patroltime = random.randint(round(30 * self.aggressiveness), round(120 * self.aggressiveness))
                self.dx = random.randint(-1,1)*self.speed
                self.dy = random.randint(-1,1)*self.speed

        self.move()

        if self.check_LOS():
            self.aim_at_player()
            self.check_aim(self.goal_angle, self.cannon_ang)
        else:
            self.idle_rotate()

    def check_aim(self, goal, angle):
        if abs(goal-angle) < 3 and \
                self.shoottick >= self.firerate and \
                random.randint(1,self.firechance) == 1 and \
                len(self.bulletgroup) < self.maxbullets:
            self.primaryfire(self.rect.center[0] + math.cos(math.radians(self.cannon_ang))*20,
                             self.rect.center[1]-math.sin(math.radians(self.cannon_ang))*20,
                             self.bullettype,
                             self.cannon_ang, self.bulletspeed, self.bounces)

    def idle_rotate(self):
        self.rotate_tick += 1

        if self.rotate_tick < self.rotate_time:
            # direction 1 is left, 2 is right, 0 is none
            if self.rotate_direction == 1:
                self.cannon_ang += self.turnspeed/2
            elif self.rotate_direction == 2:
                self.cannon_ang -= self.turnspeed/2


        else:
            self.rotate_tick = 0
            # choose between 1-4 seconds to rotate
            self.rotate_time = random.randint(30,120)
            # Change direction to rotate
            self.rotate_direction = random.randint(0,2)

    def move_toward(self,x,y):
        # Change dx towards player
        if self.pos.x < x and abs(self.pos.x-x)>3:
            self.dx = self.speed
        elif self.pos.x > x and abs(self.pos.x-x)>3:
            self.dx = -self.speed

        # change dy towards player
        if self.pos.y < y and abs(self.pos.y-y)>3:
            self.dy = self.speed
        elif self.pos.y > y and abs(self.pos.y-y)>3:
            self.dy = -self.speed

    def primaryfire(self, x, y, type, angle, speed, bounces, collideself=True):
        angle_deviation = random.randint(-self.accuracy,self.accuracy)/10
        rad_ang = math.radians(angle + angle_deviation)
        if type == 0:
            bullet = Bullet(x,y,rad_ang,speed,bounces,collideself)
        elif type == 1:
            bullet = BigBullet(x,y,rad_ang,speed,bounces)
        self.bulletgroup.add(bullet)
        bulletgroup.add(bullet)

    def got_hit(self):
        self.health -= 1
        if self.health <= 0:
            global score
            score += 1
            explosions.add(Explosion(self.pos.x, self.pos.y))
            self.kill()

class josh(Enemy):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.maxhealth = 20 + level
        self.health = self.maxhealth
        self.color = (50,50,50)
        self.accuracy = 500
        self.bulletspeed = 10
        self.firerate = 5
        self.firechance = 1
        self.turnspeed = 5
        self.speed = 2
        self.maxbullets = 100
        self.boss = True
        self.name = "The Josh"
        self.playedintro = False
        self.introtick = 0
        self.aggressiveness = 2

    def ai(self):
        super().ai()
        if not self.playedintro:
            self.playintro()
            self.playedintro = True

    def playintro(self):
        self.intro = pygame.mixer.Sound(resource_path("Assets/Audio/Josh/Intro/Intro" + str(random.randint(1, 9)) + ".mp3"))
        self.intro.set_volume(0.7)
        pygame.mixer.Sound.play(self.intro)

    def got_hit(self):
        self.health-=1
        if self.health <= 0:
            self.intro = pygame.mixer.Sound(resource_path("Assets/Audio/Josh/Outro/Outro" + str(random.randint(1, 9)) + ".mp3"))
            self.intro.set_volume(0.7)
            pygame.mixer.Sound.play(self.intro)
            global score
            score += 1
            self.kill()

class BuckShot(Enemy):
    def __init__(self, x,y):
        super().__init__(x,y)
        self.maxhealth = 20 + level
        self.health = self.maxhealth
        self.color = (50,50,50)
        self.accuracy = 1
        self.bulletspeed = 5
        self.speed = 2
        self.maxbullets = 100
        self.firerate = 15
        self.boss = True
        self.name = "BuckShot"
        self.aggressiveness = 10
        self.playedintro = False
        self.introtick = 0

    def ai(self):
        super().ai()
        if not self.playedintro:
            self.playintro()
            self.playedintro = True

    def playintro(self):
        self.intro = pygame.mixer.Sound(resource_path("Assets/Audio/BuckShot/Intro/Intro" + str(random.randint(1, 5)) + ".mp3"))
        self.intro.set_volume(3.0)
        pygame.mixer.Sound.play(self.intro)

    def check_aim(self, goal, angle):
        if abs(goal-angle) < 3 and \
                self.shoottick >= self.firerate and \
                random.randint(1,self.firechance) == 1 and \
                len(self.bulletgroup) < self.maxbullets:
            for i in range(11):
                self.primaryfire(self.rect.center[0] + math.cos(math.radians(self.cannon_ang-25+i*5))*20,
                             self.rect.center[1]-math.sin(math.radians(self.cannon_ang-25+i*5))*20,
                             self.bullettype,
                             self.cannon_ang-25+i*5, self.bulletspeed, self.bounces, False)

    def got_hit(self):
        self.health-=1
        if self.health <= 0:
            self.intro = pygame.mixer.Sound(resource_path("Assets/Audio/BuckShot/Outro/Outro" + str(random.randint(1, 1)) + ".mp3"))
            self.intro.set_volume(0.7)
            pygame.mixer.Sound.play(self.intro)
            global score
            score += 1
            self.kill()

class KaBoom(Enemy):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.maxbullets = 0
        self.speed = 5
        self.boss = True
        self.name = "KaBoom"
        self.aggressiveness=0.1
        self.shoottick = 0
        self.firerate = 30
        self.maxhealth = 10
        self.health = self.maxhealth
        self.playedintro = False
        self.introtick = 0

    def ai(self):
        if not self.playedintro:
            self.playintro()
            self.playedintro = True
        self.patroltick += 1
        if self.patroltick == self.patroltime:
            self.patroltick = 0
            self.patroltime = random.randint(round(30 * self.aggressiveness), round(120 * self.aggressiveness))
            self.dx = random.randint(-1, 1) * self.speed
            self.dy = random.randint(-1, 1) * self.speed
        self.shoottick+=1
        if self.shoottick > self.firerate:
            self.primaryfire()
        self.move()
        self.idle_rotate()

    def primaryfire(self):
        minegroup.add(Mine(player.pos.x+10,player.pos.y+10,5))

    def playintro(self):
        self.intro = pygame.mixer.Sound(resource_path("Assets/Audio/KaBoom/Intro/Intro" + str(random.randint(1, 4)) + ".mp3"))
        self.intro.set_volume(1.0)
        pygame.mixer.Sound.play(self.intro)

    def got_hit(self):
        self.health-=1
        if self.health <= 0:
            self.outro = pygame.mixer.Sound(resource_path("Assets/Audio/KaBoom/Outro/Outro" + str(random.randint(1, 2)) + ".mp3"))
            self.outro.set_volume(0.7)
            pygame.mixer.Sound.play(self.outro)
            global score
            score += 1
            self.kill()

class Mine(pygame.sprite.Sprite):
    def __init__(self,x,y,timer):
        super().__init__()
        self.pos = pygame.Vector2(x,y)
        self.timer = timer
        self.tick = 0
        self.active = False
        self.f1 = loadify("Assets/Sprites/bigframe1.png")
        self.f2 = loadify("Assets/Sprites/bigframe2.png")
        self.f3 = loadify("Assets/Sprites/bigframe3.png")
        self.f4 = loadify("Assets/Sprites/bigframe4.png")
        self.f5 = loadify("Assets/Sprites/bigframe5.png")
        self.f6 = loadify("Assets/Sprites/bigframe6.png")
        self.color = (255,255,0)
        self.image = pygame.draw.circle(screen,self.color,(self.pos.x,self.pos.y), 10)
        self.x, self.y = self.pos.x-125,self.pos.y-125

        self.shade = 255

    def update(self):
        if not self.active:
            self.shade -= (255/(30*self.timer))
            if self.shade <= 0:
                self.active = True
                self.sound = pygame.mixer.Sound(resource_path("Assets/Audio/SFX/explode.wav"))
                self.sound.set_volume(0.5)
                pygame.mixer.Sound.play(self.sound)
                self.image = self.f1
                self.rect=self.image.get_rect(center=(self.pos.x,self.pos.y))
                self.shade = 0
            self.color = (255,self.shade,0)

        elif self.active:
            self.mask = pygame.mask.from_surface(self.image)
            self.rect=self.image.get_rect(center=(self.pos.x,self.pos.y))
            hitplayer = pygame.sprite.spritecollide(self, playergroup, False)
            if hitplayer and self.image == self.f6:
                player.got_hit()
            self.tick+=1


        self.draw()

    def draw(self):
        if not self.active:
            pygame.draw.circle(screen,self.color,(self.pos.x, self.pos.y),10)
        else:
            if self.tick <= 2:
                self.image = self.f1
                screen.blit(self.image, (self.x,self.y))
            elif self.tick <= 4:
                self.image = self.f2
                screen.blit(self.image, (self.x,self.y))
            elif self.tick <= 6:
                self.image = self.f3
                screen.blit(self.image, (self.x,self.y))
            elif self.tick <= 8:
                self.image = self.f4
                screen.blit(self.image, (self.x,self.y))
            elif self.tick <= 10:
                self.image = self.f5
                screen.blit(self.image, (self.x,self.y))
            elif self.tick <= 12:
                self.image = self.f6
                screen.blit(self.image, (self.x,self.y))
            elif self.tick <= 14:
                self.image = self.f5
                screen.blit(self.image, (self.x,self.y))
            elif self.tick <= 16:
                self.image = self.f4
                screen.blit(self.image, (self.x,self.y))
            elif self.tick <= 18:
                self.image = self.f3
                screen.blit(self.image, (self.x,self.y))
            elif self.tick <= 20:
                self.image = self.f2
                screen.blit(self.image, (self.x,self.y))
            elif self.tick <= 22:
                self.image = self.f1
                screen.blit(self.image, (self.x,self.y))
            else:
                self.kill()

class BrownTank(Enemy):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.speed=0
        self.turnspeed=1
        self.maxbullets = 1
        self.accuracy = 100
        self.color = (100,70,30)
        self.og_cannon=loadify("Assets/Sprites/BrownTank.png")

class GrayTank(Enemy):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.speed = 2
        self.turnspeed = 2
        self.maxbullets = 3
        self.accuracy = 80
        self.color = (120,120,120)
        self.og_cannon=loadify("Assets/Sprites/GrayTank.png")
        self.aggressiveness = 0.5

class TealTank(Enemy):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.speed = 2
        self.turnspeed = 3
        self.maxbullets = 1
        self.accuracy = 30
        self.firechance = 1
        self.color = (80, 200,200)
        self.og_cannon = loadify("Assets/Sprites/TealTank.png")
        self.aggressiveness = 1.1
        self.bullettype = 1
        self.bulletspeed = 5
        self.canhitself = False

    def check_aim(self, goal, angle):
        if abs(goal-angle) < 3 and \
                self.shoottick >= self.firerate and \
                random.randint(1,self.firechance) == 1 and \
                len(self.bulletgroup) < self.maxbullets:
            self.primaryfire(self.rect.center[0] + math.cos(math.radians(self.cannon_ang))*30,
                             self.rect.center[1]-math.sin(math.radians(self.cannon_ang))*30,
                             self.bullettype,
                             self.cannon_ang, self.bulletspeed, self.bounces)

class LimeTank(Enemy):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.speed = 0.5
        self.accuracy = 1
        self.turnspeed = 3
        self.aggressiveness = 1.2
        self.bulletspeed = 15
        self.maxbullets = 1
        self.firechance = 1
        self.color = (56, 255, 25)
        self.og_cannon = loadify("Assets/Sprites/LimeTank.png")
        self.maxhealth = 3
        self.health = 3

class PinkTank(Enemy):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.speed = 3
        self.turnspeed = 5
        self.firerate = 10
        self.firechance = 1
        self.maxbullets = 10
        self.accuracy = 20
        self.aggressiveness = 2.5
        self.color = (209, 31, 174)
        self.og_cannon = loadify("Assets/Sprites/PinkTank.png")
        self.bulletspeed = 6
        self.maxhealth = 3
        self.health = 3

class RedTank(Enemy):
    def __init__(self,x,y):
        super().__init__(x,y)
        self.speed = 1.5
        self.turnspeed = 2
        self.maxbullets = 20
        self.accuracy = 80
        self.firerate = 5
        self.firechance = 2
        self.color = (140,0,0)
        self.og_cannon = loadify("Assets/Sprites/RedTank.png")
        self.aggressiveness = 0.8
        self.bulletspeed = 3
        self.maxhealth = 5
        self.health = 5

def findcoordinate(x,y):
    gridx = round((x-25)/25,0)
    gridy = round((y-250)/25,0)
    return (int(gridx),int(gridy))

def coord_to_pixel(x,y):
    return 25+3+x*25,250+3+y*25

def draw_grid(grid):
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                tilecolor=wall
            else:
                tilecolor=floor




            pygame.draw.rect(screen,tilecolor,[25+j*25,250+i*25,25,25])

    #draw outline of grid
    for i in range(52):
        pygame.draw.rect(screen,wall,[0+i*25,225, 25,25])
        pygame.draw.rect(screen,wall,[0+i*25,875,25,25])
    for i in range(25):
        pygame.draw.rect(screen,wall,[0,250+i*25,25,25])
        pygame.draw.rect(screen,wall,[1275,250+i*25,25,25])

def update_all():
    for bullet in bulletgroup:
        bullet.update()
    player.update()
    for enemy in enemies:
        enemy.update()
    for explosion in explosions:
        explosion.update()
    for mine in minegroup:
        mine.update()

def update_pathfinding():
    player.location = findcoordinate(player.pos.x,player.pos.y)
    for enemy in enemies:
        enemy.location = findcoordinate(enemy.pos.x, enemy.pos.y)

def map_to_array(number):
    img = Image.open(resource_path("Assets/Maps/map"+str(number)+".png")).convert("RGB")
    arr = np.array(img)
    new_arr = [[0 for _ in range(50)] for _ in range(25)]


    for i in range(25):
        for j in range(50):
            tile = arr[i][j]
            if tile[0] == tile[1] == tile[2]: # grayscale; black, gray, or white
                if tile[0] == 0:#black pixel; wall
                    new_arr[i][j] = 0
                elif tile[0] == 255: #white pixel; floor
                    new_arr[i][j] = 1
                else: # gray pixel
                    new_arr[i][j] = 2
            else:
                if tile[0] == 255: # red pixel; enemies cant spawn here
                    new_arr[i][j] = -2
                elif tile[2] == 255: # blue pixel; player spawn
                    new_arr[i][j] = -1


    return new_arr

def show_crosshair(cross, pos):
    screen.blit(cross, (pos[0] - 17, pos[1] - 17))

def spawn_walls(grid):
    # load outline walls
    for i in range(52):
        walls.add(Wall(0 + i * 25, 225))
        walls.add(Wall(0 + i * 25, 875))
    for i in range(25):
        walls.add(Wall(0, 250 + i * 25))
        walls.add(Wall(1275, 250 + i * 25))
    # load non-outline walls
    for i in range(25):
        for j in range(50):
            if grid[i][j] == 0:
                walls.add(Wall(25 + j * 25, 250 + i * 25))

def draw_level_ui():
    pygame.draw.rect(screen,wall,[5,5,300,105])
    pausetxt = mainfontmed.render("PAUSE [esc]",True,(0,0,0))
    pauserect = pausetxt.get_rect(center=(150,55))
    screen.blit(pausetxt,pauserect)
    pygame.draw.rect(screen,wall,[5,115,300,105])
    lvltxt = mainfontmed.render("Level: " + str(level), True, (0,0,0))
    lvlrect = lvltxt.get_rect(center=(150,170))
    screen.blit(lvltxt,lvlrect)
    pygame.draw.rect(screen,wall,[1010,5,285,105])
    enemytxt = mainfontsm.render("Enemies Left: " + str(len(enemies)), True, (0,0,0))
    enemyrect = enemytxt.get_rect(center=(1150,55))
    screen.blit(enemytxt, enemyrect)
    pygame.draw.rect(screen, wall,[1010,115,285,105])
    killcounttxt = mainfontsm.render("Tanks Killed: " + str(score), True, (0,0,0))
    killcountrect = killcounttxt.get_rect(center=(1150,170))
    screen.blit(killcounttxt,killcountrect)

def spawn_level(grid,level):
    open_spawns = []
    player_spawns = []
    red_spots = []

    for i in range(25):
        for j in range(50):
            if grid[i][j] == 1: # find all tiles available for spawns
                open_spawns.append((i,j))
            elif grid[i][j] == -1:
                player_spawns.append((i,j))
            elif grid[i][j] == -2:
                red_spots.append((i,j))

    randomcoord = random.randint(0,len(player_spawns)-1)
    playercoords = player_spawns[randomcoord]
    playerlocation = coord_to_pixel(playercoords[1], playercoords[0])
    play = Player(playerlocation[0],playerlocation[1])

    playergroup.add(play) #add player
    tanks.add(play)
    for i in range(len(player_spawns)):
        grid[player_spawns[i][0]][player_spawns[i][1]] = 1 #turn blue tiles into floor
    num_spawns, strongest_spawn = findmaxspawn(level), findhighesttank(level)
    for i in range(num_spawns):
        location = open_spawns[random.randint(0,len(open_spawns)-1)]
        tanktype = random.randint(1,strongest_spawn)
        if level%10!=0:
            enemies.add(get_tank(tanktype, location))
        else:
            enemies.add(get_boss(location))
        open_spawns.remove((location[0],location[1]))
    for i in range(len(red_spots)):
        grid[red_spots[i][0]][red_spots[i][1]] = 1

    if level > 40:
        for enemy in enemies:
            addhealth = math.floor((level-40)/5)
            enemy.health += addhealth
            enemy.maxhealth += addhealth

def findmaxspawn(level):
    if level%10 == 0:
        return 1
    else:
        return min(math.ceil(level/2.5),15)

def findhighesttank(level):
    if level <=5:
        return 1
    elif level <= 10:
        return 2
    elif level <= 15:
        return 3
    elif level <= 20:
        return 4
    elif level <= 25:
        return 5
    elif level <= 30:
        return 6
    else:
        return 6

def get_tank(type, coord):

    location = coord_to_pixel(coord[1],coord[0])

    if type == 1:
        return BrownTank(location[0],location[1])
    elif type == 2:
        return GrayTank(location[0], location[1])
    elif type == 3:
        return TealTank(location[0], location[1])
    elif type == 4:
        return LimeTank(location[0], location[1])
    elif type == 5:
        return PinkTank(location[0], location[1])
    elif type == 6:
        return RedTank(location[0], location[1])

def get_boss(coord):
    location = coord_to_pixel(coord[1], coord[0])
    bossnum = random.randint(1,3)

    if bossnum == 1:
        return josh(location[0], location[1])
    elif bossnum == 2:
        return BuckShot(location[0], location[1])
    elif bossnum == 3:
        return KaBoom(location[0], location[1])

def loading_ui(level):
    screen.fill(floor)

    if level%10 == 0:
        screen.fill((80,0,0))
        for i in range(18):
            for j in range(13):
                pygame.draw.rect(screen, (100,0,0), [0 + (50 * (i % 2)) + 100 * j, i * 50, 50, 50])
    elif level%2 == 0:
        for i in range(9):
            pygame.draw.rect(screen,wall,[0,i*100,1300,50])
    elif level%2 == 1:
        for i in range(13):
            pygame.draw.rect(screen,wall,[i*100,0,50,900])

    loadingtxt = mainfontbig.render("LEVEL " + str(level), True, (0,0,0))
    loadingrect = loadingtxt.get_rect(center=(650,450))
    screen.blit(loadingtxt,loadingrect)

    livestxt = mainfontbig.render("Lives: " + str(lives), True, (0, 0, 0))
    livesrect = livestxt.get_rect(center=(650, 550))
    screen.blit(livestxt, livesrect)

    if level % 10 == 0:
        bosstxt = bossfont1.render("BOSS", True, (0, 0, 0))
        bossrect = bosstxt.get_rect(center=(650, 350))
        screen.blit(bosstxt, bossrect)

    if level % 5 == 1 and level != 1 and not died:


        extralifetxt = mainfontbig.render("+1 Life", True, (0, 0, 0))
        extraliferect = extralifetxt.get_rect(center=(650, 350))
        screen.blit(extralifetxt, extraliferect)

    if level == 1:
        screen.blit(wbutton, (42,826))
        screen.blit(abutton, (5,863))
        screen.blit(sbutton,(42,863))
        screen.blit(dbutton,(79,863))
        screen.blit(leftclick,(116,831))

def empty_all():
    enemies.empty()
    playergroup.empty()
    bulletgroup.empty()
    tanks.empty()
    walls.empty()
    minegroup.empty()





playergroup = pygame.sprite.Group()
bulletgroup = pygame.sprite.Group()
walls = pygame.sprite.Group()
enemies = pygame.sprite.Group()
tanks = pygame.sprite.Group()
explosions = pygame.sprite.Group()
minegroup = pygame.sprite.Group()


crosshair=loadify('Assets/Sprites/Crosshair.png')
leftclick = loadify("Assets/Sprites/lmb.png")
abutton=loadify("Assets/Sprites/a.png")
wbutton = loadify("Assets/Sprites/w.png")
sbutton = loadify("Assets/Sprites/s.png")
dbutton = loadify("Assets/Sprites/d.png")


deathx, deathy = None, None
dx,dy=0,0
tick = 0
ldown = False
rdown = False
level = 10
score = 0
lives = 3
died = False

pygame.mixer.music.load(resource_path('Assets/Audio/Music/LevelTheme1.mp3'))
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.6)

while running:
    # Framerate of 30
    timer.tick(30)

    # Quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    mousepos = pygame.mouse.get_pos()
    mousestate = pygame.mouse.get_pressed()
    lmb = mousestate[0]
    rmb = mousestate[2]

    if gamestate=="mainmenu":
        screen.fill(floor)
        for i in range(18):
            for j in range(13):
                pygame.draw.rect(screen,wall,[0+(50*(i%2))+100*j,i*50,50,50])

        titletxt = titlefont.render("TANK GAME", True, (0,0,0))
        titlerect = titletxt.get_rect(center=(650,300))
        screen.blit(titletxt,titlerect)
        startbutton = pygame.rect.Rect(505,450,290,140)
        pygame.draw.rect(screen,darkwall,[505,450,290,140])
        starttxt = mainfontbig.render("PLAY", True, (0,0,0))
        startrect = starttxt.get_rect(center=(650,520))
        screen.blit(starttxt,startrect)
        creditbutton = pygame.rect.Rect(505, 600, 290, 140)
        pygame.draw.rect(screen, darkwall, [505, 600, 290, 140])
        credittxt = mainfontbig.render("Credits", True, (0, 0, 0))
        creditrect = credittxt.get_rect(center=(650, 670))
        screen.blit(credittxt, creditrect)


        if ldown and not lmb:
            ldown = False

        if lmb and startbutton.collidepoint(mousepos) and not ldown:
            level = 1
            score = 0
            lives=3
            ldown = True
            gamestate = "loadlevel"

        if lmb and creditbutton.collidepoint(mousepos)and not ldown:
            gamestate = "credits"
            ldown = True

        pygame.display.flip()

    elif gamestate == "credits":
        screen.fill(floor)
        for i in range(18):
            for j in range(13):
                pygame.draw.rect(screen, wall, [50 - (50 * (i % 2)) + 100 * j, i * 50, 50, 50])

        creditbigtxt = titlefont.render("Credits", True, (0, 0, 0))
        creditbigrect = creditbigtxt.get_rect(center=(650, 100))
        screen.blit(creditbigtxt, creditbigrect)

        credittxt = mainfontmed.render("Voices:", True, (0, 0, 0))
        creditrect = credittxt.get_rect(center=(650, 250))
        screen.blit(credittxt, creditrect)

        credittxt = mainfontmed.render("The Josh - @Azero.iz", True, (0, 0, 0))
        creditrect = credittxt.get_rect(center=(650, 300))
        screen.blit(credittxt, creditrect)

        credittxt = mainfontmed.render("BuckShot - @Fourteensouls", True, (0, 0, 0))
        creditrect = credittxt.get_rect(center=(650, 350))
        screen.blit(credittxt, creditrect)

        credittxt = mainfontmed.render("KaBoom - @TheyrThem", True, (0, 0, 0))
        creditrect = credittxt.get_rect(center=(650, 400))
        screen.blit(credittxt, creditrect)

        credittxt = mainfontmed.render("Music:", True, (0, 0, 0))
        creditrect = credittxt.get_rect(center=(650, 500))
        screen.blit(credittxt, creditrect)

        credittxt = mainfontmed.render("JoshBuster - @Azero.iz", True, (0, 0, 0))
        creditrect = credittxt.get_rect(center=(650, 550))
        screen.blit(credittxt, creditrect)

        backbutton = pygame.rect.Rect(5, 5, 290, 140)
        pygame.draw.rect(screen, darkwall, [5, 5, 290, 140])
        backtxt = mainfontbig.render("Back", True, (0, 0, 0))
        backrect = backtxt.get_rect(center=(150, 75))
        screen.blit(backtxt, backrect)


        if ldown and not lmb:
            ldown = False

        if lmb and backbutton.collidepoint(mousepos) and not ldown:
            gamestate = "mainmenu"
            ldown = True



        pygame.display.flip()

    elif gamestate=="loadlevel":
        screen.fill(floor)
        pygame.mouse.set_visible(0)
        show_crosshair(crosshair, mousepos)

        if tick == 0: # load the level once
            if level % 5 == 1 and level != 1 and not died:
                lives += 1
            mapnum = random.randint(1,15)
            levelgrid = map_to_array(mapnum)

            spawn_level(levelgrid, level)
            spawn_walls(levelgrid)
            player = playergroup.sprites()[0]
            grid = Grid(matrix=levelgrid)


        loading_ui(level)
        show_crosshair(crosshair, mousepos)

        tick += 1
        if tick >= 120:
            tick=0
            levelcompletetick = 0

            gamestate="inlevel"


        pygame.display.flip()

    elif gamestate=="inlevel":

        # Do everything it should do in the level
        screen.fill(floor)
        draw_grid(levelgrid)
        draw_level_ui()
        dx, dy = 0, 0

        #player movement
        if keys[pygame.K_w]:
            dy=-player.speed
        if keys[pygame.K_s]:
            dy=player.speed
        if keys[pygame.K_a]:
            dx=-player.speed
        if keys[pygame.K_d]:
            dx=player.speed

        pausebuttonrect = pygame.rect.Rect(5,5,300,105)
        if keys[pygame.K_ESCAPE] or (lmb and pausebuttonrect.collidepoint(mousepos) and not ldown):
            gamestate = "paused"
            pygame.mouse.set_visible(1)
            if lmb:
                ldown = True
            continue


        #Prevent diagonal movement being faster
        if dx!=0 and dy!=0:
            dx*=0.7
            dy*=0.7
        update_all()

        # Fire when clicked

        if lmb and not ldown:
            ldown = True
            player.primaryfire()
        elif ldown and not lmb:
            ldown = False

        # update enemy pathfinding 6 times per second
        if tick%5 == 0:
            update_pathfinding()

        # display the crosshair
        show_crosshair(crosshair, mousepos)


        tick += 1

        # check if all enemies are dead
        if len(enemies) == 0:
            bulletgroup.empty()
            levelcompletetick += 1
            if levelcompletetick == 120:
                empty_all()
                gamestate = "loadlevel"
                level += 1
                tick=0
                died = False

            ui_offset = levelcompletetick*10
            if ui_offset > 600:
                ui_offset = 600

            pygame.draw.rect(screen,darkwall,[300,-300+ui_offset,700,300],)
            levelcompletetext = mainfontbig.render("Level Complete!", True, (0,0,0))
            levelcompleterect = levelcompletetext.get_rect(center=(650,-150+ui_offset))
            screen.blit(levelcompletetext,levelcompleterect)

        pygame.display.flip()

    elif gamestate == "paused":
        pygame.draw.rect(screen, darkwall, [500, 300, 300, 400], )
        pausedtext = mainfontbig.render("Paused", True, (0, 0, 0))
        pausedrect = pausedtext.get_rect(center=(650, 350))
        screen.blit(pausedtext, pausedrect)
        resumebutton = pygame.rect.Rect(505,400,290,140)
        pygame.draw.rect(screen,wall,[505,400,290,140])
        resumetext = mainfontbig.render("Resume", True, (0,0,0))
        resumerect = resumetext.get_rect(center=(650,470))
        screen.blit(resumetext, resumerect)
        quitbutton = pygame.rect.Rect(505,550,290,140)
        pygame.draw.rect(screen,wall,[505,550,290,140])
        quittext = mainfontbig.render("Quit", True, (0,0,0))
        quitrect = quittext.get_rect(center=(650,620))
        screen.blit(quittext,quitrect)



        if ldown and not lmb:
            ldown = False


        if (lmb and resumebutton.collidepoint(mousepos)) and not ldown:
            gamestate = "inlevel"
            pygame.mouse.set_visible(0)
            ldown=True
        if lmb and quitbutton.collidepoint(mousepos) and not ldown:
            gamestate = "mainmenu"
            empty_all()
            ldown = True
            died = True
            tick=0

        pygame.display.flip()

    elif (gamestate == "died" and lives>1) or gamestate == "dead1":
        died = True
        screen.fill(floor)
        draw_grid(levelgrid)
        draw_level_ui()
        if tick == 1:
            explosions.add(Explosion(deathx, deathy))
            lives-=1
            gamestate = "dead1"
        tick += 1

        for explosion in explosions:
            explosion.update()
        opacity=3*tick-60
        if opacity < 0:
            opacity = 0
        elif opacity > 255:
            opacity = 255
        transparent_surface = pygame.Surface((1300, 900), pygame.SRCALPHA)
        pygame.draw.rect(transparent_surface, (darkwall[0],darkwall[1],darkwall[2],opacity), [0,200,1300,500])

        diedtext = mainfontbig.render("You Died", True, (0, 0, 0))
        diedrect = diedtext.get_rect(center=(650, 450))
        transparent_surface.set_alpha(opacity)
        transparent_surface.blit(diedtext, diedrect)
        screen.blit(transparent_surface,(0,0))
        show_crosshair(crosshair, mousepos)
        pygame.display.flip()

        if tick >= 210:
            gamestate = "loadlevel"
            empty_all()
            tick=0

    elif gamestate == "died" and lives <=1:

        screen.fill(floor)
        draw_grid(levelgrid)
        draw_level_ui()
        if tick == 1:
            explosions.add(Explosion(deathx, deathy))
            lives -= 1
        tick += 1
        for explosion in explosions:
            explosion.update()
        opacity = 5 * tick
        if opacity < 0:
            opacity = 0
        elif opacity > 255:
            opacity = 255



        transparent_surface = pygame.Surface((1300, 900), pygame.SRCALPHA)
        pygame.draw.rect(transparent_surface, (darkwall[0],darkwall[1],darkwall[2], opacity), [0, 200, 1300, 500])
        diedtext = mainfontbig.render("Out Of Lives!", True, (0, 0, 0))
        diedrect = diedtext.get_rect(center=(650, 300))
        transparent_surface.set_alpha(opacity)
        transparent_surface.blit(diedtext, diedrect)
        screen.blit(transparent_surface, (0, 0))



        opacity2 = 5 * tick - 60
        if opacity2 < 0:
            opacity2 = 0
        elif opacity2 > 255:
            opacity2 = 255
        transparent_surface2 = pygame.Surface((1300, 900), pygame.SRCALPHA)
        restartbutton = pygame.rect.Rect(505, 400, 290, 140)
        pygame.draw.rect(transparent_surface2, (wall[0],wall[1],wall[2],opacity2), [505, 400, 290, 140])
        restarttext = mainfontbig.render("Restart", True, (0, 0, 0))
        restartrect = restarttext.get_rect(center=(650, 475))
        transparent_surface2.set_alpha(opacity2)
        transparent_surface2.blit(restarttext,restartrect)
        screen.blit(transparent_surface2, (0,0))



        opacity3 = 5 * tick - 120
        if opacity3 < 0:
            opacity3 = 0
        elif opacity3 > 255:
            opacity3 = 255
        transparent_surface3 = pygame.Surface((1300, 900), pygame.SRCALPHA)
        quitbutton = pygame.rect.Rect(505, 550, 290, 140)
        pygame.draw.rect(transparent_surface3, (wall[0], wall[1], wall[2], opacity3), [505, 550, 290, 140])
        quittext = mainfontbig.render("Quit", True, (0, 0, 0))
        quitrect = quittext.get_rect(center=(650, 620))
        transparent_surface3.set_alpha(opacity3)
        transparent_surface3.blit(quittext, quitrect)
        screen.blit(transparent_surface3, (0, 0))



        if (lmb and restartbutton.collidepoint(mousepos)) and not ldown and tick > 30:
            gamestate = "loadlevel"
            level = 1
            score = 0
            lives = 3
            tick=0
            empty_all()
            pygame.mouse.set_visible(0)
            ldown=True

        if (lmb and quitbutton.collidepoint(mousepos)) and not ldown and tick > 30:
            gamestate = "mainmenu"
            ldown = True
            pygame.mouse.set_visible(1)
            tick=0
            empty_all()



        show_crosshair(crosshair, mousepos)



        pygame.display.flip()








pygame.quit()





