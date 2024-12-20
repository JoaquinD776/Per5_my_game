# This file was created by: Joaquin Duran

# Imports setting for color, dimensions
import pygame as pg
from pygame.sprite import Sprite
from settings import *
from os import path
import random

vec = pg.math.Vector2

class Player(Sprite):
    #Contains properties of the player such as color, collisions, speed, keys
    # other elements in the game...
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = self.game.player_img
        self.image.set_colorkey(BLACK)
        # dimensions
        self.image.fill((128, 0, 128))
        # color (purple)
        self.rect = self.image.get_rect()
        self.pos = vec(x*TILESIZE, y*TILESIZE)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        #speed of player
        self.speed = 2
        self.coin_count = 0
        self.original_jump_power = 20      # Default jump power
        self.jump_power = self.original_jump_power  # Initial jump power
        self.jumping = False
        # keys to move player
    def get_keys(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.vel.x -= self.speed
        if keys[pg.K_d]:
            self.vel.x += self.speed
        if keys[pg.K_SPACE]:
            print("works")
            self.jump()
        if keys[pg.K_r]:
            self.pos = (WIDTH/2, HEIGHT/2)
            print("respawn")
            self.jump_power = 22

    def jump(self):
        # print("im trying to jump")
        
        print(self.vel.y)
        self.rect.y += 2
        whits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        phits = pg.sprite.spritecollide(self, self.game.all_platformwalls, False)
        self.rect.y -= 2
        if whits or phits and not self.jumping:
            self.jumping = True
            self.vel.y = -self.jump_power
            # print('still trying to jump...')
            
    # collides with walls on x axis        
    def collide_with_platformwalls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.all_platformwalls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - TILESIZE
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
            #     print("Collided on x axis")
            # else:
            #     print("not working...for hits")
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.all_platformwalls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - TILESIZE
                    self.vel.y = 0
                # if self.vel.y < 0:
                #     self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y
                self.jumping = False


    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - TILESIZE
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
            #     print("Collided on x axis")
            # else:
            #     print("not working...for hits")
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - TILESIZE
                    self.vel.y = 0
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y
                self.jumping = False
    # collisions with coins/powerups
    # "kill" refers to the sprite disappearing when collided with
    def collide_with_stuff(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Powerup":
                self.speed += 3
                print("I've gotten a powerup!")
            if str(hits[0].__class__.__name__) == "Coin":
                print("I got a coin!!!")
                self.coin_count += 1
            if str(hits[0].__class__.__name__) == "SlowPowerup":
                print("I got slower")
                self.speed -= 2  
                # Slow powerup decreases speed
                if self.speed < 1:  
                # Prevent speed from going below 1
                    self.speed = 1
            if str(hits[0].__class__.__name__) == "Jumpboost":
                print("Jumpboost collected!")
                self.jump_power = 40  # Increase jump power
                self.jump_boost_start_time = pg.time.get_ticks()  # Record start time of boost
                if self.jump_boost_start_time > 2000:
                    self.original_jump_power

    def update(self):
        # gravity and friction inputed from settings
        # keeps player on the map
        self.acc = vec(0, GRAVITY)
        self.get_keys()
        self.acc.x += self.vel.x * FRICTION
        self.vel += self.acc

        
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0

        self.pos += self.vel + 0.5 * self.acc

        self.rect.x = self.pos.x
        # collisions on x axis
        self.collide_with_walls('x')
        self.collide_with_platformwalls('x')
        # self.collide_with_platformwalls('x')

        self.rect.y = self.pos.y
        # collisions on y axis
        self.collide_with_walls('y')
        self.collide_with_platformwalls('y')
        # collisions with coins, powerups
        self.collide_with_stuff(self.game.all_powerups, True)
        self.collide_with_stuff(self.game.all_coins, True)

# other classes follow same baseline as player in terms of properties
class Mob(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((32, 32))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.speed = 25

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > WIDTH or self.rect.x < 0:
            self.speed *= -1
            self.rect.y += 32
        if self.rect.y > HEIGHT:
            self.rect.y = 0
        # bounces off of player by going opposite way
        if self.rect.colliderect(self.game.player):
            self.speed *= -1

class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = self.game.wall_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Platform(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_platforms
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((96, 32))
        self.image = self.game.platform_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.speed = 10
    def update(self):
        self.rect.x += self.speed
        if self.rect.right > WIDTH or self.rect.left < 0:
            self.speed *= -1
        hits = pg.sprite.spritecollide(self, self.game.all_walls, False)
        if hits:
            self.speed *= -1


class Powerup(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_powerups
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(PINK)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Jumpboost(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_powerups
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = self.game.jumpboost_img
        self.image.set_colorkey(BLACK)        
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Coin(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_coins
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = self.game.coin_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class SlowPowerup(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_powerups
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class Platformwall(Sprite):
     def __init__(self, game, x, y, w, h):
        self.game = game
        self.groups = game.all_sprites, game.all_platformwalls
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        print("i have created a platform...")
            
  


