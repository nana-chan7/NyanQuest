import pygame
from game import Game
from character import Character

class Player(pygame.sprite.Sprite, Character):
    def __init__(self,pos):
        # プレイヤーキャラ画像
        a_1 = pygame.image.load("chara_images/3/1.png")
        a_2 = pygame.image.load("chara_images/3/2.png")
        a_3 = pygame.transform.flip(a_1, 1, 0)
        a_4 = pygame.transform.flip(a_2, 1, 0)
        a_5 = pygame.image.load("chara_images/3/5.png")
        a_6 = pygame.image.load("chara_images/3/6.png")


        super().__init__()
        # self.chara_list = [self.list1, self.list2, self.list3, self.list4]
        
        # キャラクター画像
        self.all_image_list = [a_1, a_2, a_3, a_4, a_5, a_6]
        
        self.image = self.set_chara_animation(self.all_image_list)
        self.rect = self.image.get_rect(topleft=pos)
        
        self.player_attack_img = pygame.image.load("images/attack_star.png")
        self.count = 0
        
        self.jump_coount = 0    # ジャンプカウンタ
        self.landing = True     # 着地判定
        
        self.on_right_key = False
        self.on_left_key = False
        self.move_dx = 0
    
    # キャラクターによって画像リストの差し替え
    def change_image_list(self):
        pass
    # 画像は先にロードしてリストに キャラ全部のリストを作って 指定のキャラの時に呼び出し
      
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
                self.rect.x += 1
                if Game.field.movement_collision():
                    self.rect.x -= 1
                    break
                self.move_dx = self.rect.x - self.x_before
        else:
            self.on_right_key = False
        # 左移動
        if Game.on_leftkey():
            if Game.move_flag:
                Game.direction_num = -1
            for _ in range(8):
                self.rect.x -= 1
                if Game.field.movement_collision():
                    self.rect.x += 1
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
            self.rect.y += 1
            if Game.field.movement_collision():
                self.landing = True # 着地したら
                self.jump_coount = 0
                self.rect.y -= 1
                break

    # ジャンプ処理    
    def jump(self):
        if self.landing:
            if self.jump_coount < 12:
                self.rect.y -=10
            elif self.jump_coount < 16:
                self.rect.y -= 5
            elif self.jump_coount < 22:
                self.landing = False
        if Game.field.movement_collision():
            for i in range(10):
                self.rect.y += 1
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
        self.set_chara_animation(self.image_list)
        self.player_attack()

        
    