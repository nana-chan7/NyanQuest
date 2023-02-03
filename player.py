import pygame
from game import Game
from character import Character

class Player(pygame.sprite.Sprite, Character):
    def __init__(self,pos):
        # プレイヤーキャラ画像
        # 棒人間
        a_1 = pygame.image.load("chara_images/0/1.png")
        a_2 = pygame.image.load("chara_images/0/2.png")
        a_3 = pygame.transform.flip(a_1, 1, 0)
        a_4 = pygame.transform.flip(a_2, 1, 0)
        a_5 = pygame.image.load("chara_images/0/5.png")
        a_6 = pygame.image.load("chara_images/0/6.png")
        a_list = [a_1, a_2, a_3, a_4, a_5, a_6]
        # 猫王
        b_1 = pygame.image.load("chara_images/1/1.png")
        b_2 = pygame.image.load("chara_images/1/2.png")
        b_3 = pygame.transform.flip(b_1, 1, 0)
        b_4 = pygame.transform.flip(b_2, 1, 0)
        b_5 = pygame.image.load("chara_images/1/5.png")
        b_6 = pygame.image.load("chara_images/1/6.png")
        b_list = [b_1, b_2, b_3, b_4, b_5, b_6]
        # マラソン猫
        c_1 = pygame.image.load("chara_images/2/1.png")
        c_2 = pygame.image.load("chara_images/2/2.png")
        c_3 = pygame.transform.flip(c_1, 1, 0)
        c_4 = pygame.transform.flip(c_2, 1, 0)
        c_5 = pygame.image.load("chara_images/2/5.png")
        c_6 = pygame.image.load("chara_images/2/6.png")
        c_list = [c_1, c_2, c_3, c_4, c_5, c_6]
        # ドラ？もん
        d_1 = pygame.image.load("chara_images/3/1.png")
        d_2 = pygame.image.load("chara_images/3/2.png")
        d_3 = pygame.transform.flip(d_1, 1, 0)
        d_4 = pygame.transform.flip(d_2, 1, 0)
        d_5 = pygame.image.load("chara_images/3/5.png")
        d_6 = pygame.image.load("chara_images/3/6.png")
        d_list = [d_1, d_2, d_3, d_4, d_5, d_6]

        super().__init__()
        # self.chara_list = [self.list1, self.list2, self.list3, self.list4]
        self.chara_no = 0
        # キャラクター画像
        self.all_image_list = [a_list, b_list, c_list, d_list]
        self.image_list = self.change_image_list(self.all_image_list, Game.chara_no)
        
        self.image = self.set_chara_animation(self.image_list)
        self.rect = self.image.get_rect(topleft=pos)
        
        self.player_attack_img = pygame.image.load("images/attack_star.png")
        self.count = 0
        
        self.jump_coount = 0    # ジャンプカウンタ
        self.landing = True     # 着地判定
        
        self.on_right_key = False
        self.on_left_key = False
        self.move_dx = 0
        
        self.move_list = [2, 1, 2, 1]
        self.jump_list1 = [15, 10, 18, 20]
        self.jump_list2 = [8, 5, 4, 6]
        
    # キャラクターによって画像リストの差し替え
    def change_image_list(self, all_list, chara_no):
        self.image_list = all_list[chara_no]
        return self.image_list

      
    # 移動処理  
    def get_input(self):
        self.count += 1
        self.now_rect = self.rect
        # Game.collided_flag = False
        Game.move_flag = True
        self.move_dx = 0
        self.x_before = self.rect.x

        # 右移動
        if Game.on_rightkey():
            if Game.move_flag:
                Game.direction_num = 1
            for _ in range(8):
                self.rect.x += self.move_list[Game.chara_no]
                if Game.field.movement_collision():
                    self.rect.x -= self.move_list[Game.chara_no]
                    break
                self.move_dx = self.rect.x - self.x_before
        else:
            self.on_right_key = False
        # 左移動
        if Game.on_leftkey():
            if Game.move_flag:
                Game.direction_num = -1
            for _ in range(8):
                self.rect.x -= self.move_list[Game.chara_no]
                if Game.field.movement_collision():
                    self.rect.x += self.move_list[Game.chara_no]
                    break
                self.move_dx = self.rect.x + self.x_before
        else:
            self.on_left_key = False
            
        # ジャンプ
        if self.landing and Game.on_spacekey():  
            self.jump()

        # 重力
        else:        
            self.apply_gravity()
            
            
        # 画面外に落下した場合ゲームオーバー
        if self.rect.y > 704:
            Game.is_gameover = True 
            
    

    # 重力処理  
    def apply_gravity(self):
        for i in range(10):
            self.rect.y += 2
            if Game.field.movement_collision():
                self.landing = True # 着地したら
                self.jump_coount = 0
                self.rect.y -= 2
                break

    # ジャンプ処理    
    def jump(self):
        if self.landing:
            if self.jump_coount < 6:
                self.rect.y -=self.jump_list1[Game.chara_no]
            elif self.jump_coount < 8:
                self.rect.y -= self.jump_list2[Game.chara_no]
            elif self.jump_coount < 11:
                self.landing = False
        if Game.field.movement_collision():
            for i in range(10):
                self.rect.y += 2
            self.landing = False
            
        self.jump_coount += 1
        
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

        
    