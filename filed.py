import pygame
from tiles import Tile
from player import Player
from enemy import Enemy, Boss
from game import Game, Phase

class Filed:
    def __init__(self,level_data): 
        
        # セットアップ
        self.setup_level(level_data)
        self.world_shift = 0    # 移動→背景も動くための ブロック タイル
        self.current_x = 0
        
        self.map = Game.map_no         # マップ番号(初期値は１)

    # マップ(フィールド全体)処理
    def setup_level(self, layout):
       self.tiles = pygame.sprite.Group()           # ブロック タイル
       self.player = pygame.sprite.GroupSingle()    # プレイヤーキャラ
       self.enemy0 = pygame.sprite.GroupSingle()    # 敵0
       self.enemy1 = pygame.sprite.GroupSingle()    # 敵1
       self.enemy2 = pygame.sprite.GroupSingle()    # 敵2
       self.enemy3 = pygame.sprite.GroupSingle()    # 敵3       
       self.enemy4 = pygame.sprite.GroupSingle()    # 敵4
       self.enemy5 = pygame.sprite.GroupSingle()    # 敵5
       self.enemy6 = pygame.sprite.GroupSingle()    # 敵6
       self.enemy7 = pygame.sprite.GroupSingle()    # 敵7
       self.enemy8 = pygame.sprite.GroupSingle()    # 敵8
       self.enemy9 = pygame.sprite.GroupSingle()    # 敵9       
       self.enemy10 = pygame.sprite.GroupSingle()   # 敵10

       self.boss = pygame.sprite.GroupSingle()      # map1ボス

       
       for row_index, row in enumerate(layout):
           for col_index, cell in enumerate(row):
                x = col_index * Game.TILE_SIZE
                y = row_index * Game.TILE_SIZE
                # タイル ブロック
                Game.block_no = cell - 1 
                # 半ブロック 上半分  
                if cell == 1:
                    tile = Tile((x,y+32),Game.TILE_SIZE)
                    self.tiles.add(tile)
                # 半ブロック 下半分 
                if cell == 2:
                    tile = Tile((x,y),Game.TILE_SIZE)
                    self.tiles.add(tile)
                # ブロック
                if cell == 3:
                    tile = Tile((x,y),Game.TILE_SIZE)
                    self.tiles.add(tile)
                # 草ブロック
                if cell == 4:
                    tile = Tile((x,y),Game.TILE_SIZE)
                    self.tiles.add(tile)                    
                    
                # プレイヤー
                if cell == 22:
                    player_sprite = Player((x,y))
                    self.player.add(player_sprite)
                    
                # エネミーキャラ
                Game.enemy_no = cell - 5
                if cell == 5:
                    enemy_sprite0 = Enemy((x,y))
                    self.enemy0.add(enemy_sprite0)  
                if cell == 6:
                    enemy_sprite1 = Enemy((x,y))
                    self.enemy1.add(enemy_sprite1)
                if cell == 7:
                    enemy_sprite2 = Enemy((x,y))
                    self.enemy2.add(enemy_sprite2)  
                if cell == 8:
                    enemy_sprite3 = Enemy((x,y))
                    self.enemy3.add(enemy_sprite3)
                if cell == 9:
                    enemy_sprite4 = Enemy((x,y))
                    self.enemy4.add(enemy_sprite4)  
                if cell == 10:
                    enemy_sprite5 = Enemy((x,y))
                    self.enemy5.add(enemy_sprite5)
                if cell == 11:
                    enemy_sprite6 = Enemy((x,y))
                    self.enemy6.add(enemy_sprite6)  
                if cell == 12:
                    enemy_sprite7 = Enemy((x,y))
                    self.enemy7.add(enemy_sprite7)
                if cell == 13:
                    enemy_sprite8 = Enemy((x,y))
                    self.enemy8.add(enemy_sprite8)  
                if cell == 14:
                    enemy_sprite8 = Enemy((x,y))
                    self.enemy8.add(enemy_sprite8)
          
                # ボスキャラ 遷移
                if cell == 15:
                    boss_sprite = Enemy((x,y))
                    self.boss.add(boss_sprite)
     
    
    # プレイヤーの移動による画面処理
    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.x
        self.world_shift = 0
        self.flag = False

        if player_x > Game.SCREEN_WIDTH - (Game.SCREEN_WIDTH / 4) and Game.direction_num > 0 and player.move_dx != 0:
            self.world_shift = -player.move_dx
            Game.move_flag = False 
               
        elif player_x < (Game.SCREEN_WIDTH / 4) and Game.direction_num < 0 and player.move_dx != 0:
            self.world_shift = player.move_dx
            Game.move_flag = False
    
        else:
            self.world_shift = 0
            Game.move_flag = True
            
    # プレイヤーとブロックの当たり判定        
    def movement_collision(self):
        player = self.player.sprite
        flag = pygame.sprite.spritecollide(player, self.tiles.sprites(), False)
        if len(flag) != 0:
            return True
                
    def damage_collision(self):
        player = self.player.sprite
        a_flag = pygame.sprite.spritecollide(player, self.enemy0, False)
        b_flag = pygame.sprite.spritecollide(player, self.enemy1, False)
        c_flag = pygame.sprite.spritecollide(player, self.enemy2, False)
        d_flag = pygame.sprite.spritecollide(player, self.enemy3, False)
        e_flag = pygame.sprite.spritecollide(player, self.enemy4, False)
        f_flag = pygame.sprite.spritecollide(player, self.enemy5, False)
        g_flag = pygame.sprite.spritecollide(player, self.enemy6, False)
        h_flag = pygame.sprite.spritecollide(player, self.enemy7, False)
        i_flag = pygame.sprite.spritecollide(player, self.enemy8, False)
        j_flag = pygame.sprite.spritecollide(player, self.enemy9, False)
        k_flag = pygame.sprite.spritecollide(player, self.enemy10, False)
        if len(a_flag) != 0:
            Game.enemy_self = 0
            return True 
        elif len(b_flag) != 0:
            Game.enemy_self = 1
            return True
        elif len(c_flag) != 0:
            Game.enemy_self = 23
            return True
        elif len(d_flag) != 0:
            Game.enemy_self = 3
            return True
        elif len(e_flag) != 0:
            Game.enemy_self = 4
            return True
        elif len(f_flag) != 0:
            Game.enemy_self = 5
            return True
        elif len(g_flag) != 0:
            Game.enemy_self = 6
            return True
        elif len(h_flag) != 0:
            Game.enemy_self = 7
            return True
        elif len(i_flag) != 0:
            Game.enemy_self = 8
            return True
        elif len(j_flag) != 0:
            Game.enemy_self = 9
            return True
        elif len(k_flag) != 0:
            Game.enemy_self = 10
            return True
                
    def run(self):
        # プレイヤー
        self.player.update()
        self.player.draw(Game.surface)  
        
        # ブロック(タイル)
        if self.world_shift < 0:
            for i in range(-self.world_shift):
                self.tiles.update(-1)
                if self.movement_collision():
                    self.tiles.update(1)
                    break
                else:
                    self.player.sprite.rect.x -= 1
        elif self.world_shift > 0:
            for e in range(self.world_shift):
                self.tiles.update(1)
                if self.movement_collision():
                    self.tiles.update(-1)
                    break
                else:
                    self.player.sprite.rect.x += 1
                    
                    
        self.tiles.draw(Game.surface)
        self.scroll_x() 
     
        
        # 敵
        self.enemy0.update(self.world_shift)
        self.enemy0.draw(Game.surface)
        self.enemy1.update(self.world_shift)
        self.enemy1.draw(Game.surface)
        self.enemy2.update(self.world_shift)
        self.enemy2.draw(Game.surface)
        self.enemy3.update(self.world_shift)
        self.enemy3.draw(Game.surface)
        self.enemy4.update(self.world_shift)
        self.enemy4.draw(Game.surface)
        self.enemy5.update(self.world_shift)
        self.enemy5.draw(Game.surface)
        self.enemy6.update(self.world_shift)
        self.enemy6.draw(Game.surface)
        self.enemy7.update(self.world_shift)
        self.enemy7.draw(Game.surface)
        self.enemy8.update(self.world_shift)
        self.enemy8.draw(Game.surface)
        self.enemy9.update(self.world_shift)
        self.enemy9.draw(Game.surface)
        self.enemy10.update(self.world_shift)
        self.enemy10.draw(Game.surface)
        self.boss.update(self.world_shift)
        self.boss.draw(Game.surface)
        # self.enemies = [self.enemy0,self.enemy1,self.enemy2,self.enemy3,self.enemy4,self.enemy5,
        #  self.enemy6,self.enemy7,self.enemy8,self.enemy9,self.enemy10]
        # if Game.kill:
        #     self.enemies[Game.enemy_self].kill()
        #     Game.item += 10

            

    # マップ(仮)
    map1 = [
    [4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [3,6,0,0,0,0,0,0,0,0,0,10,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0],
    [3,2,2,0,0,0,0,0,0,2,2,2,0,0,0,0,0,0,0,0,0,0,0,13,0,0,0,0,0,0],
    [3,0,0,0,2,1,0,0,0,0,0,0,0,0,0,1,1,0,0,9,0,0,0,1,1,2,2,0,0,0],
    [3,0,0,0,0,0,1,2,0,0,0,1,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0,0,0,0],
    [3,0,22,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,7,0,0,0,15],
    [3,2,2,0,0,0,0,1,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,0,0,2,4],
    [3,0,0,0,1,8,1,0,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
    [3,0,0,0,0,2,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14,0,3],
    [3,11,0,1,4,0,0,0,0,0,0,0,0,0,0,0,12,0,0,4,0,0,0,0,0,1,1,2,0,3],
    [3,4,4,3,3,1,0,4,2,1,1,1,1,1,2,1,1,0,4,3,2,3,1,1,2,3,3,0,0,3]]

    map2 = [
    [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [3,0,0,0,0,0,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [3,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,0,0,0],
    [3,9,0,0,0,0,0,1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
    [3,0,0,0,0,0,0,3,0,0,2,2,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,0,0,3],
    [3,0,0,0,0,2,2,3,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,3],
    [3,0,2,2,0,0,0,3,6,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,1,1,0,0,3],
    [3,3,0,0,0,0,0,3,2,1,1,1,1,1,2,0,1,1,1,2,2,3,0,1,2,3,3,0,2,3]]



    map_list = [map1,map2]

