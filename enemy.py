import pygame
from game import Game
from character import Character
from player import Player

# class Enemy(pygame.sprite.Sprite,Character):
#     def __init__(self,pos):
#         super().__init__()
#         # self.image = pygame.Surface((64,64))
#         # self.player = Player()
#         self.image_list = (pygame.image.load("enemy_images/nekomy1.png"),
#                             pygame.image.load("enemy_images/nekomy2.png"))
#         self.player_animation = Character(self.image_list,7)
#         self.image = self.image_list[0]
#         self.rect = self.image.get_rect(topleft=pos)
#         self.player = Player()
        
class Enemy(pygame.sprite.Sprite,Character):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.image_list = (pygame.image.load("enemy_images/nekomy1.png"),
                            pygame.image.load("enemy_images/nekomy2.png"))
        self.image = self.image_list[0]
        # self.image.fill((100,100,100))
        self.rect = self.image.get_rect(topleft=pos)
        Game.enemy_x, Game.enemy_y = self.rect.x, self.rect.y

        
    # def collided_player(self):
    #     self.rect.colliderect(Game.player_pos)
    #     Game.is_gameover = True
        
    def update(self, x_shift):
        self.rect.x += x_shift      
    
class Boss(pygame.sprite.Sprite,Character):
    def __init__(self,pos):
        super().__init__()
        # self.image = pygame.Surface((64,64))
        # self.player = Player()
        self.image_list = (pygame.image.load("enemy_images/nekomy1.png"),
                            pygame.image.load("enemy_images/nekomy2.png"))
        self.player_animation = Character(self.image_list,7)
        self.image = self.image_list[1]
        self.rect = self.image.get_rect(topleft=pos)
