import pygame
from game import Game
from character import Character

class Enemy(pygame.sprite.Sprite, Character):
    def __init__(self, pos):
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

        # マップ1ボス
        boss1 = pygame.image.load("enemy_images/3/1.png")
        boss2 = pygame.image.load("enemy_images/3/2.png")
        self.boss_list = [boss1, boss2]

        super().__init__()  
        self.enemy_no = 0
        
        self.all_image_list = [self.z_list, self.z_list, self.z_list, self.z_list, self.z_list, 
                               self.y_list, self.y_list, self.y_list, self.y_list, self.y_list, self.boss_list]   
        self.image_list = self.change_image_list(self.all_image_list, Game.enemy_no)
        self.image = self.set_enemy_animation(self.image_list)
        self.rect = self.image.get_rect(topleft=pos)
        
        
    # キャラクターによって画像リストの差し替え
    def change_image_list(self, all_list, enemy_no):
        self.image_list = all_list[enemy_no]
        return self.image_list

      
    # 更新処理            
    def update(self, x_shift):
        self.set_enemy_animation(self.image_list)
        self.rect.x += x_shift   
            
        
class Boss(pygame.sprite.Sprite, Character):
    def __init__(self, pos, size):
       
        boss1 = pygame.image.load("enemy_images/3/1.png")
        boss2 = pygame.image.load("enemy_images/3/2.png")
        self.image_list = [boss1, boss2]

        super().__init__()  
        self.image = self.set_enemy_animation(self.image_list)
        self.rect = self.image.get_rect(topleft=pos)
      
    # 更新処理            
    def update(self, x_shift):
        self.set_enemy_animation(self.image_list)
        self.rect.x += x_shift    

    