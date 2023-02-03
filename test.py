import pygame
from game import Game
from character import Character

class Player(pygame.sprite.Sprite, Character):
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
        self.enemy_no = 0
        self.all_image_list = [self.z_list, self.y_list]   
        self.image = self.set_enemy_animation(self.all_image_list[Game.enemy_no])
        self.rect = self.image.get_rect(topleft=pos)
        
        self.enemy_no = 0
        
        self.player_attack_img = pygame.image.load("images/attack_star.png")
        self.count = 0
        Game.enemy_x, Game.enemy_y = self.rect.x, self.rect.y
        self.hp = 50
        self.d_flag = False
        
        self.r_flag = True
        self.l_flag = False
    
    def enemy_move(self):
        self.befor_move = self.rect.x
        if self.r_flag:
            self.rect.x += 10
        if self.rect.x - self.befor_move >= 20:
            self.befor_move = self.rect.x
            self.l_flag = True
        if self.l_flag: 
            self.rect.x -= 10
        if self.befor_move - self.rect.x >= 20:
            self.befor_move = self.rect.x
            self.r_flag = True
           
        
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

      


    

 
    
    # 仮
    
    
    
        
    # 攻撃処理              
    def player_attack(self):
        r_atack_x, r_atack_y = self.rect.x + 70, self.rect.y + 10
        l_atack_x, l_atack_y = self.rect.x-30, self.rect.y+10
        if Game.on_ckey(): 
            Game.surface.blit(self.player_attack_img,(r_atack_x, r_atack_y))
        elif Game.on_xkey(): 
            Game.surface.blit(self.player_attack_img,(l_atack_x, l_atack_y))
        
    # リスタート処理      
    def re_start(self):
        if Game.is_gameover:
            self.rect.x, self.rect.y = 100, 30      
    
    # 更新処理            
    def update(self):
        self.get_input()
        self.re_start() 
        self.change_image_list(self.all_image_list, Game.chara_no)
        self.set_chara_animation(self.image_list)
        self.player_attack()

        
    