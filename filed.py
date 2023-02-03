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
        self.move_count = 0     # 一定数進むとマップを変える


    # マップ(フィールド全体)処理
    def setup_level(self, layout):
       self.tiles = pygame.sprite.Group()
       self.player = pygame.sprite.GroupSingle()
       self.enemy = pygame.sprite.Group()
       
       self.boss = pygame.sprite.Group()

       
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
                # ドア マップ遷移用
                if cell == 5:
                    tile = Tile((x,y),Game.TILE_SIZE) 
                    self.tiles.add(tile)
                    self.tile_rect = tile
                    
                    
                # プレイヤー
                if cell == 9:
                    player_sprite = Player((x,y))
                    self.player.add(player_sprite)
                    
                # エネミーキャラ
                Game.enemy_no = cell - 6
                if cell == 6:
                    enemy_sprite = Enemy((x,y),Game.TILE_SIZE)
                    self.enemy.add(enemy_sprite)
                        
                if cell == 7:
                    enemy_sprite = Enemy((x,y),Game.TILE_SIZE)
                    self.enemy.add(enemy_sprite)

                # ボスキャラ
                # if cell == 8:
                #     boss_sprite = Boss((x,y),Game.TILE_SIZE)
                #     self.boss.add(boss_sprite)
     
    
    # プレイヤーの移動による画面処理
    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.x
        self.world_shift = 0

        if player_x > Game.SCREEN_WIDTH - (Game.SCREEN_WIDTH / 4) and Game.direction_num > 0 and player.move_dx != 0:
            self.world_shift = -player.move_dx
            Game.move_flag = False         
        elif player_x < Game.SCREEN_WIDTH / 4 and Game.direction_num < 0 and player.on_left_key:
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
        
        if self.tile_rect.rect.x <= player.rect.x:
            if self.tile_rect.rect.y <= player.rect.y:
                Game.phase == Phase.BOSS
                
    # def atack_collision(self):
    #     player = self.player.sprite
    #     a_flag = pygame.sprite.spritecollide(player, self.enemy.sprite(), False)
    #     if len(a_flag) != 0:
    #         return True
        
    # リスタート時
    def re_start(self):
        if Game.is_gameover:
            self.map = Game.map_no 
            Game.direction_num = 0     
            self.world_shift = 0   
            self.current_x = 0

    # def boss(self):
    #     if Game.player_pos == Game.enemy_pos:
    #         Game.map_no = 2
            
    # def damage(self):
    #     if Game.enemy_x <= Game.star_x >= Game.enemy_x+64: 
    #         if Game.enemy_y <= Game.star_y >= Game.enemy_y+64:
    #             Game.is_gameover = True  
                                 
    def run(self):
        # self.bg_move()
        
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
        self.re_start()
        
        # 敵
        self.enemy.update(self.world_shift)
        self.enemy.draw(Game.surface)
        # self.enemy.enemy_move()
        # self.enemy.get_action()
        self.scroll_x() 

    # マップ(仮)
    map1 = [
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
    [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
    [1,0,0,2,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
    [1,0,0,0,0,0,1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
    [1,0,0,0,0,0,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,2,0,0,0,0,0,1,2,1,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5],
    [1,0,0,0,0,0,0,3,0,0,2,2,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,0,0,3],
    [1,0,0,0,0,2,2,3,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,3,3],
    [1,0,2,2,0,0,0,3,6,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,1,1,3,0,3],
    [3,3,0,0,0,0,0,3,2,1,1,1,1,1,2,0,1,1,1,2,2,3,0,1,2,3,3,0,2,3]]

    map2 = [
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
    [1,0,0,0,0,0,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
    [1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,9,0,0,0,0,0,1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,3,0,0,2,2,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,0,0,3],
    [1,0,0,0,0,2,2,3,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,3],
    [1,0,2,2,0,0,0,3,6,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,1,1,0,0,3],
    [3,3,0,0,0,0,0,3,2,1,1,1,1,1,2,0,1,1,1,2,2,3,0,1,2,3,3,0,2,3]]



    map2 = (
    (1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3),
    (1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3),
    (1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3),
    (1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3),
    (1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3),
    (1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,0,0,8,3),
    (1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,2,0,0,3),
    (1,9,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,3),
    (1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,2,2,0,0,0,0,0,0,0,0,0,0,0,3),
    (1,4,4,3,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,2,2,2,0,4,0,0,0,0,0,0,3),
    (1,1,1,1,0,0,1,1,2,2,2,2,2,2,1,0,0,0,0,0,0,0,1,1,0,1,0,2,2,2,2))

    map3 = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
    
    map = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,0],
    [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

    map_list = [map1,map2]

    # map = (
    # (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
    # (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
    # (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
    # (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
    # (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
    # (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
    # (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
    # (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
    # (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
    # (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
    # (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0))
