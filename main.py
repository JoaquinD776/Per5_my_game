# this file was created by: Joaquin Duran
# this is where we import libraries and modules
import pygame as pg
from settings import *
# from sprites import *
from sprites_side_scroller import *
from tilemap import *
from os import path
import random
# we are editing this file after installing git

'''
Elevator pitch: I want to create a game about parkouring (like a platform game)

GOALS: to complete a parkour level and beat the boss
RULES: jump, move left and right, time jumps, if you fall off map, respawn at checkpoint
FEEDBACK: multiplayer?
FREEDOM: x and y movement with jump, platforming

Alpha goal: map moves with character (vertically)

'''


'''

sources:

'''
# create a game class that carries all the properties of the game and methods
class Game:
  # initializes all the things we need to run the game...includes the game clock which can set the FPS
  def __init__(self):
    pg.init()
    pg.mixer.init()
    self.clock = pg.time.Clock()
    self.screen = pg.display.set_mode((WIDTH, HEIGHT))
    # Determines screen dimensions from settings
    pg.display.set_caption("Joaquin's Game")
    self.playing = True
  def load_data(self):
    self.game_folder = path.dirname(__file__)
    self.snd_folder = path.join(self.game_folder, 'sounds' ) 
    self.map = Map(path.join(self.game_folder, 'game_1_level1.txt'))
    self.game_folder = path.dirname(__file__)
    self.img_folder = path.join(self.game_folder, 'images')
    self.jumpboost_img = pg.image.load(path.join(self.img_folder, 'Jumpboost.png'))
    self.coin_img = pg.image.load(path.join(self.img_folder, 'Coin.png'))
    self.wall_img = pg.image.load(path.join(self.img_folder, 'Wall.png'))
    self.platform_img = pg.image.load(path.join(self.img_folder, 'Platform.png'))
       # load sounds
    #self.jump_snd = pg.mixer.Sound(path.join(self.snd_folder, 'jump_07.wav'))
    pg.mixer.music.load(path.join(self.snd_folder, 'bckgrd.ogg'))
    pg.mixer.music.set_volume(0.4)
    pg.mixer.music.play(loops=-1)
  def new(self):
    self.load_data()
    print(self.map.data)
    # create the all sprites group to input sprites into the game
    self.all_sprites = pg.sprite.Group()
    self.all_walls = pg.sprite.Group()
    self.all_powerups = pg.sprite.Group()
    self.all_coins = pg.sprite.Group()
    self.all_slowpowerups = pg.sprite.Group()
    self.all_platforms = pg.sprite.Group()
    self.all_platformwalls = pg.sprite.Group()
    # Each sprite has a letter or number which is inputed into the level text
    for row, tiles in enumerate(self.map.data):
      print(row*TILESIZE)
      for col, tile in enumerate(tiles):
        print(col*TILESIZE)
        if tile == '1':
          Wall(self, col, row)
        if tile == 'M':
          Mob(self, col, row)
        if tile == 'P':
          self.player = Player(self, col, row)
        if tile == 'U':
          Powerup(self, col, row)
        if tile == 'C':
          Coin(self, col, row)
        if tile == 'Q':
          SlowPowerup(self, col, row)
        if tile == 'R':
          Platform(self, col, row)
        if tile == 'J':
          Jumpboost(self, col, row)
        if tile == 'p':
          Platformwall(self, col, row, 100, 20)
          
  # this is a method
  # the run method runs the game loop
  def run(self):
    while self.playing:
      self.dt = self.clock.tick(FPS) / 1000
      # input
      self.events()
      # process
      self.update()
      # output
      self.draw()

    pg.quit()
  # input
  def events(self):
    for event in pg.event.get():
        if event.type == pg.QUIT:
          self.playing = False
  # process
  # this is where the game updates the game state
  def update(self):
    # update all the sprites
    # text on screen including fps and coin count
    self.all_sprites.update()
    while len(self.all_platforms) < 15:
      width = random.randrange(50, 100)
      p = Platform(self, random.randrange(0, WIDTH//TILESIZE - width//TILESIZE), random.randrange(-5, 0), width, TILESIZE)
      if random.randint(0,9) > 4:
        c = Coin(self, p.rect.x//TILESIZE, p.rect.y//TILESIZE - 1)
        self.all_coins.add(c) #adds coin on platform
        self.all_sprites.add(c)
      self.all_platforms.add(p)
      self.all_sprites.add(p)

    if self.player.rect.top <= HEIGHT/4:
      print(str(len(self.all_platforms)))
      self.player.pos.y += abs(self.player.vel.y)
      for plat in self.all_platforms:
        plat.rect.y += abs(self.player.vel.y)
        if plat.rect.y >= HEIGHT:

          plat.kill() #destroys plats after they are off screen
          print(str(len(self.all_coins)))
      for coin in self.all_coins:
        coin.rect.y += abs(self.player.vel.y)
        if coin.rect.y >= HEIGHT:
          coin.kill()
          print(str(len(self.all_coins)))

  # output
  def draw(self):
    self.screen.fill(BLACK)
    self.all_sprites.draw(self.screen)
    self.draw_text(self.screen, str(self.dt*1000), 24, WHITE, WIDTH/30, HEIGHT/30)
    self.draw_text(self.screen, str(self.player.coin_count), 24, WHITE, WIDTH-100, 50)
    pg.display.flip()

if __name__ == "__main__":
  # instantiate
  print("main is running...")
  g = Game()
  print("main is running...")
  g.new()
  g.run()
