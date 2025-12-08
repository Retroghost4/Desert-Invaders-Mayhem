import pygame
from mayhem import Mayhem
from buggies import Buggies
from settings import HEIGHT, WIDTH, ENEMY_SPEED, CHARACTER_SIZE, BULLET_SIZE, NAV_THICKNESS
from bullets import Bullet
from display import Display

class World: 
  def __init__(self, screen):
    self.screen = screen
    self.player = pygame.sprite.GroupSingle()
    self.buggies = pygame.sprite.Group()
    self.display = Display(self.screen)
    self.game_over = False
    self.player_score = 0
    self.game_level = 1
    self._generate_world()

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

  def player_move(self, attack = False):
   keys = pygame.key.get_pressed()
   if keys[pygame.K_a] and not self.game_over or keys[pygame.KLEFT] and not self.game_over:
    if self.player.sprite.rect.left > 0:
      self.player.sprite.move_left()
   if keys[pygame.K_d] and not self.game_over or keys[pygame.K_RIGHT] and not self.game_over:
    if self.player.sprite.rect.right < WIDTH:
      self.player.sprite.move_right()
   if keys[pygame.K_w] and not self.game_over or keys[pygame.K_UP] and not self.game_over:
    if self.player.sprite.rect.top > 0:
      self.player.sprite.move_up()
   if keys[pygame.K_s] and not self.game_over or keys[pygame.K_DOWN] and not self.game_over:
    if self.player.sprite.rect.bottom < HEIGHT:
      self.player.sprite.move_bottom()
   if keys[pygame.K_r]:
    self.game_over = False
    self.player_score = 0
    self.game_level = 1
    for buggie in self.buggies.sprites():
      buggie.kill()
    self._generate_world()
   if attack and not self.game_over:
    self.player.sprite._shoot()

  def _detect_collisions(self):
   player_attack_collision = pygame.sprite.groupcollide(self.buggies, self.player.sprite.player_bullets, True, True)
   if player_attack_collision:
    self.player_score += 10
   for buggie in self.buggies.sprites():
    buggie_attack_collision = pygame.sprite.groupcollide(buggie.bullets, self.player, True, False)
    if buggie_attack_collision:
      self.player.sprite.life -= 1
      break
   buggie_to_player_collision = pygame.sprite.groupcollide(self.buggies, self.player, True, False)
   if buggie_to_player_collision:
      self.player.sprite.life -= 1

  def _buggies_movement(self):
   move_sideward = False
   move_forward = False

   for buggie in self.buggies.sprites():
    if buggie.to_direction == "right" and buggie.rect.right < WIDTH or buggie.to_direction == "left" and buggie.rect.left > 0:
      move_sideward = True
      move_forward = False
    else:
      move_sideward = False
      move_forward = True
      buggie.to_direction = "left" if buggie.to_direction == "right" else "right"
      break

  def _buggie_shoot(self):
   for buggie in self.buggies.sprites():
     if (WIDTH - buggie.rect.x) // CHARACTER_SIZE == (WIDTH - self.player.sprite.rect.x) // CHARACTER_SIZE:
      buggie._shoot()
      break

  def _check_game_state(self):
   if self.player.sprite.life <= 0:
    self.game_over = True
    self.display.game_overmessage()
   for buggie in self.buggies.sprites():
    self.game_over = True
    self.display.game_over_message()
    break
  
   if len(self.buggies) == 0 and self.player.sprite.life > 0:
    self.game_level += 1
    self.generate_buggies()
    for buggie in self.buggies.sprites():
      buggie.move_speed += self.game_level -1

  def update(self):
    self.detect_collisions()
    self.buggie_movement()
    self._buggie.shoot()

    self.player.sprite.player_bullets.update()
    self.player.sprite.player_bullets.draw(self.screen)

    [buggie.bullets.update() for buggie in self.buggies.sprites()]
    [buggie.bullets.draw(self.screen) for buggie in self.buggies.sprites()]

    self.player.update()
    self.player.draw(self.screen)

    self.buggies.draw(self.screen)
    self.add_additionals()
    self._check_game_state()
  
  
  


      
