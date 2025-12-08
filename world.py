import pygame
from mayhem import Mayhem
from buggies import Buggies
from settings import HEIGHT, WIDTH, ENEMY_SPEED, CHARACTER_SIZE, BULLET_SIZE, NAV_THICKNESS
from bullet import Bullet
from display import Display

class World: 
  def __init__(self, screen):
    self.screen = Screen
    self.player = pygame.sprite.GroupSingle()
    self.buggies = pygame.sprite.Group()
    self.display = Display(self.screen)
    self.game_over = False
    self.player_score = 0
    self.game_level = 1
    self.generate_world()

  def _generate_world(self):
    player_x, player_y = WIDTH //2, HEIGHT - CHARACTER_SIZE
    center_size = CHARACTER_SIZE // 2
    player_pos = (player_x -center_size, player_y)
    self.player.add(Mayhem(player_pos, CHARACTER_SIZE))
    self._generate_buggies()

  def add_additionals(self):
    nav = pygame.Rect(0, HEIGHT, WIDTH, NAV_THICKNESS)
    pygame.draw.rect(self.screen, pygame.Color("yellow"), nav)
    self.display.show_life(self.player.sprite.life)
    self.display.show_score(self.player_score)
    self.display.show_level(self.game_level)
