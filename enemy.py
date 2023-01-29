import pygame
from game import Game
from character import Character
from player import Player
        
class Enemy(pygame.sprite.Sprite,Character):
    def __init__(self, pos, size):
        super().__init__()
        # self.image = pygame.Surface((size,size))
        self.enemy1_list = (pygame.image.load("enemy_images/1/1.png"),
                            pygame.image.load("enemy_images/1/2.png"),
                            pygame.image.load("enemy_images/1/3.png"))
        
        self.enemy2_list = (pygame.image.load("enemy_images/2/1.png"),
                            pygame.image.load("enemy_images/2/2.png"),
                            pygame.image.load("enemy_images/2/3.png"))
        
        self.all_image_list = [self.enemy1_list, self.enemy2_list]
        
        self.image = self.set_enemy_animation(self.all_image_list[0])
        self.rect = self.image.get_rect(topleft=pos)
        Game.enemy_x, Game.enemy_y = self.rect.x, self.rect.y

        
    # def collided_player(self):
    #     self.rect.colliderect(Game.player_pos)
    #     Game.is_gameover = True
        
    def update(self, x_shift):
        self.rect.x += x_shift    
        self.set_enemy_animation(self.image_list)  
    
class Boss(pygame.sprite.Sprite,Character):
    def __init__(self,pos):
        super().__init__()
        self.image_list = (pygame.image.load("enemy_images/0/1.png"),
                            pygame.image.load("enemy_images/0/2.png"))

        self.image = self.set_enemy_animation(self.image_list)
        self.rect = self.image.get_rect(topleft=pos)
        # Game.enemy_x, Game.enemy_y = self.rect.x, self.rect.y
