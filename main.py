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

Chris Cozort

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
    self.key_pressed = False
    self.key_start = 0
    self.key_elapsed = 0
    self.score = 0
  def load_data(self):
    self.game_folder = path.dirname(__file__)
    # with open(path.join(self.game_folder, HS_FILE), 'w') as f:
    #   f.write(str(0))
    try:
      with open(path.join(self.game_folder, HS_FILE), 'r') as f:
        self.highscore = int(f.read())
    except:
      with open(path.join(self.game_folder, HS_FILE), 'w') as f:
        f.write(str(0))


    self.snd_folder = path.join(self.game_folder, 'sounds' ) 
      # load map
    self.map = Map(path.join(self.game_folder, 'game_1_level1.txt'))
    self.game_folder = path.dirname(__file__)
    # load images
    self.img_folder = path.join(self.game_folder, 'images')
    self.jumpboost_img = pg.image.load(path.join(self.img_folder, 'Jumpboost.png'))
    self.coin_img = pg.image.load(path.join(self.img_folder, 'Coin.png'))
    self.wall_img = pg.image.load(path.join(self.img_folder, 'Wall.png'))
    self.platform_img = pg.image.load(path.join(self.img_folder, 'Platform.png'))
    self.player_img = pg.image.load(path.join(self.img_folder, 'Player.png'))
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
          Platformwall(self, col, row, 100, TILESIZE)
          
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
          if self.playing:
            self.playing = False
          self.running = False
        
        if event.type == pg.KEYDOWN:
          if event.key == pg.K_SPACE:
            if not self.key_pressed:
              self.player.jump()
              self.key_start = pg.time.get_ticks()
              self.key_pressed = True
        
        if event.type == pg.KEYUP:
          if event.key == pg.K_s:
            self.key_pressed = False
            if self.key_elapsed < 300:
              self.player.vel.y += GRAVITY
            
            print("Spacebar held for", self.key_elapsed, "milliseconds")
  # process
  # this is where the game updates the game state
  def update(self):
    # update all the sprites
    # text on screen including fps and coin count
  
    self.all_sprites.update()
    while len(self.all_platformwalls) < 15:
      width = (random.randrange(50, 100))
      p = Platformwall(self, random.randrange(0, WIDTH//TILESIZE - width//TILESIZE), random.randrange(-5, 0), width, TILESIZE)
      if random.randint(0,9) > 4:
        Q = Coin(self, p.rect.x//TILESIZE, p.rect.y//TILESIZE - 1)
        self.all_coins.add(Q)
        self.all_sprites.add(Q)
      self.all_platformwalls.add(p)
      self.all_sprites.add(p)
      
    if self.player.rect.top <= HEIGHT/4:
      print(str(len(self.all_platformwalls)))
      self.player.pos.y += abs(self.player.vel.y)
      for plat in self.all_platformwalls:
        plat.rect.y += abs(self.player.vel.y)
        if plat.rect.y >= HEIGHT:
          
          plat.kill()
          print(str(len(self.all_coins)))
      for coin in self.all_coins:
        coin.rect.y += abs(self.player.vel.y)
        if coin.rect.y >= HEIGHT:
          coin.kill()
          print(str(len(self.score)))

  def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        surface.blit(text_surface, text_rect)
  def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.draw_text(self.screen, str(pg.time.get_ticks()), 24, WHITE, WIDTH/30, HEIGHT/30)
        self.draw_text(self.screen, "High Score: " + str(self.highscore), 24, BLACK, WIDTH/2, HEIGHT/12)
        self.draw_text(self.screen, "Current Score: " + str(self.score), 24, BLACK, WIDTH/2, HEIGHT/24)
        pg.display.flip()

if __name__ == "__main__":
  # instantiate
  print("main is running...")
  g = Game()
  print("main is running...")
  g.new()
  g.run()
