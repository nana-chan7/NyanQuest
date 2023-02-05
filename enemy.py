import pygame
from game import Game
from character import Character
from player import Player
        
class Enemy(pygame.sprite.Sprite,Character):
    def __init__(self, pos, size):
        # 敵1
        z_1 = pygame.image.load("enemy_images/1/1.png")
        z_2 = pygame.image.load("enemy_images/1/2.png")
        z_3 = pygame.image.load("enemy_images/1/3.png")
        z_4 = pygame.transform.flip(z_1, 1, 0)
        z_5 = pygame.transform.flip(z_2, 1, 0)
        z_6 = pygame.transform.flip(z_3, 1, 0)
        self.z_list = [z_1, z_2, z_3, z_4, z_5, z_6]
        # 敵2
        y_1 = pygame.image.load("enemy_images/2/1.png")
        y_2 = pygame.image.load("enemy_images/2/2.png")
        y_3 = pygame.image.load("enemy_images/2/3.png")
        y_4 = pygame.transform.flip(y_1, 1, 0)
        y_5 = pygame.transform.flip(y_2, 1, 0)
        y_6 = pygame.transform.flip(y_3, 1, 0)
        self.y_list = [y_1, y_2, y_3, y_4, y_5, y_6]
        super().__init__()  
        # self.enemy_no = 0
        self.all_image_list = [self.z_list, self.y_list]   
        self.image = self.set_enemy_animation(self.all_image_list[Game.enemy_no])
        self.rect = self.image.get_rect(topleft=pos)

    # # 仮
    # def get_action(self):
    #     if Game.field.atack_collision():
    #         self.hp -= 10
    #         if self.hp <= 0:
    #             self.d_flag = True
            

        
    # def collided_player(self):
    #     self.rect.colliderect(Game.player_pos)
    #     Game.is_gameover = True
    
    # # 仮 敵の動き    
    # def enemy_move(self):
    #     self.befor_move = self.rect.x
    #     if self.r_flag:
    #         self.rect.x += 10
    #     if self.rect.x - self.befor_move >= 20:
    #         self.befor_move = self.rect.x
    #         self.l_flag = True
    #     if self.l_flag: 
    #         self.rect.x -= 10
    #     if self.befor_move - self.rect.x >= 20:
    #         self.befor_move = self.rect.x
    #         self.r_flag = True

        
        
        
        
    def update(self, x_shift):
        self.rect.x += x_shift    
        self.set_enemy_animation(self.image_list)  
    
class Boss(pygame.sprite.Sprite,Character):
    def __init__(self,pos):
        # super().__init__()
        super().__init__()  
        self.image_list = (pygame.image.load("enemy_images/0/1.png"),
                    pygame.image.load("enemy_images/0/2.png"))

        # self.enemy_no = 0  
        self.image = self.set_enemy_animation(self.image_list[Game.enemy_no])
        self.rect = self.image.get_rect(topleft=pos)
        
    def update(self, x_shift):
        self.rect.x += x_shift    
        self.set_enemy_animation(self.image_list)  

