import pygame
from game import Game
from character import Character

class Player(pygame.sprite.Sprite, Character):
    def __init__(self,pos):
        super().__init__()
        # 
        # self.image = pygame.Surface((64,64))
        # self.list1 = (pygame.image.load("kari_img_list/0/1.png"),
        #                 pygame.image.load("kari_img_list/0/2.png"),
        #                 pygame.image.load("kari_img_list/0/3.png"),
        #                 pygame.image.load("kari_img_list/0/4.png"),
        #                 pygame.image.load("kari_img_list/0/5.png"),
        #                 pygame.image.load("kari_img_list/0/6.png"))
        # self.list2 = (pygame.image.load("kari_img_list/1/1.png"),
        #                 pygame.image.load("kari_img_list/1/2.png"),
        #                 pygame.image.load("kari_img_list/1/3.png"),
        #                 pygame.image.load("kari_img_list/1/4.png"),
        #                 pygame.image.load("kari_img_list/1/5.png"),
        #                 pygame.image.load("kari_img_list/1/6.png"))
        # self.list3 = (pygame.image.load("kari_img_list/2/1.png"),
        #                 pygame.image.load("kari_img_list/2/2.png"),
        #                 pygame.image.load("kari_img_list/2/3.png"),
        #                 pygame.image.load("kari_img_list/2/4.png"),
        #                 pygame.image.load("kari_img_list/2/5.png"),
        #                 pygame.image.load("kari_img_list/2/6.png"))        
        # self.list4 = (pygame.image.load("kari_img_list/3/1.png"),
        #                 pygame.image.load("kari_img_list/3/2.png"),
        #                 pygame.image.load("kari_img_list/3/3.png"),
        #                 pygame.image.load("kari_img_list/3/4.png"),
        #                 pygame.image.load("kari_img_list/3/5.png"),
        #                 pygame.image.load("kari_img_list/3/6.png"))
        
        # self.chara_list = [self.list1, self.list2, self.list3, self.list4]
        
        # キャラクター画像
        self.all_image_list = (pygame.image.load("kari_img_list/3/1.png"),
                           pygame.image.load("kari_img_list/3/2.png"),
                           pygame.image.load("kari_img_list/3/3.png"),
                           pygame.image.load("kari_img_list/3/4.png"),
                           pygame.image.load("kari_img_list/3/5.png"),
                            pygame.image.load("kari_img_list/3/6.png"))
        
        
        self.image = self.set_chara_animation(self.all_image_list)
        self.rect = self.image.get_rect(topleft=pos)
        
        # プレイヤーの動き
        self.gravity = 0.8 #0.8
        
        self.screen_pos = 0
        self.now_rect = 0
        
        self.player_attack_img = pygame.image.load("images/attack_star.png")
        self.count = 0
        
        self.jump_coount = 0    # ジャンプカウンタ
        self.landing = True     # 着地判定
    
    # キャラクターによって画像リストの差し替え
    def change_image_list(self):
        pass
    # 画像は先にロードしてリストに キャラ全部のリストを作って 指定のキャラの時に呼び出し
      
    # 移動処理  
    def get_input(self):
        self.count += 1
        self.now_rect = self.rect
        Game.collided_flag = False
        
        # 右移動
        if Game.on_rightkey():
            Game.bg_stop_l = False
            Game.direction_num = 1
            self.rect.x += 8 
            if self.rect.x >= Game.SCREEN_WIDTH-20:
                self.rect.x = Game.SCREEN_WIDTH-20
                Game.bg_stop_r = True
            if Game.field.movement_collision():
                self.rect.x -= 10
            if Game.bg_stop_r:
                Game.forward_len = 0
            
        # 左移動
        if Game.on_leftkey():
            Game.bg_stop_r = False
            if self.rect.x <= 20:
                self.rect.x = 20
                Game.bg_stop_l = True
            Game.direction_num = -1
            self.rect.x -= 8 
            if Game.field.movement_collision():
                self.rect.x += 10
            if Game.bg_stop_l:
                Game.forward_len -= 2
                    
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
        Game.star_x, Game.star_y = self.rect.x, self.rect.y
        if Game.on_skey(): 
            Game.p_attack_flag = True
        
        if Game.p_attack_flag:
            self.count += 20
            Game.surface.blit(self.player_attack_img,(Game.star_x+self.count, Game.star_y))
        if Game.star_x+self.count >= Game.SCREEN_WIDTH:
            self.count = 0
            Game.star_x, Game.star_y = self.rect.x, self.rect.y
            Game.p_attack_flag = False
        
    # リスタート処理      
    def re_start(self):
        if Game.is_gameover:
            self.rect.x, self.rect.y = 30, 30      
    
    # 更新処理            
    def update(self):
        self.player_attack()
        self.get_input()
        self.re_start() 
        self.set_chara_animation(self.image_list)
        
    