import pygame
from game import Game
from character import Character

class Enemy(pygame.sprite.Sprite, Character):
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

        # マップ1ボス
        n1 = pygame.image.load("images/next_stage1.png")
        n2 = pygame.image.load("images/next_stage2.png")
        self.next_list = [n1, n2, n1, n2, n1, n2]

        super().__init__()  
        self.enemy_no = 0
        
        self.all_image_list = [self.z_list, self.y_list, self.next_list]   
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
        
        boss1_1 = pygame.image.load("enemy_images/boss/1.png")
        boss1_2 = pygame.image.load("enemy_images/boss/2.png")
        boss1_3 = pygame.image.load("enemy_images/boss/3.png")
        boss1_4 = pygame.image.load("enemy_images/boss/4.png")
        
        boss2_1 = pygame.image.load("enemy_images/boss/5.png")
        boss2_2 = pygame.image.load("enemy_images/boss/6.png")
        boss2_3 = pygame.image.load("enemy_images/boss/7.png")
        boss2_4 = pygame.image.load("enemy_images/boss/8.png")

        self.boss_list1 = [boss1_1, boss2_1]
        self.boss_list2 = [boss1_2, boss2_2]
        self.boss_list3 = [boss1_3, boss2_3]
        self.boss_list4 = [boss1_4, boss2_4]
        
        super().__init__()  
        self.boss_no = 0
        
        self.all_image_list = [self.boss_list1, self.boss_list2, self.boss_list3, self.boss_list4]   
        self.image_list = self.change_image_list(self.all_image_list, Game.boss_no)
        self.image = self.set_enemy_animation(self.image_list)
        self.rect = self.image.get_rect(topleft=pos)
        
        
    # 画像リストの差し替え
    def change_image_list(self, all_list, boss_no):
        self.image_list = all_list[boss_no]
        return self.image_list

    # 更新処理            
    def update(self, x_shift):
        self.set_enemy_animation(self.image_list)
        self.rect.x += x_shift   