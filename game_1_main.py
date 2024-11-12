# this file was created by: Joaquin Duran
# this is where we import d libraries and modules
import pygame as pg
from game_1_settings import *
# from sprites import *
from game_1_sprites_side_scroller import *
from game_1_tilemap import *
from os import path
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
    self.map = Map(path.join(self.game_folder, 'game_1_level1.txt'))
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
          JumpBoost(self, col, row)
          
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
  def draw_text(self, surface, text, size, color, x, y):
    font_name = pg.font.match_font('arial')
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surface.blit(text_surface, text_rect)

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
  