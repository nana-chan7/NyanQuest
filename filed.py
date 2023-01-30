import pygame
from tiles import Tile
from player import Player
from enemy import Enemy, Boss
from game import Game

class Filed:
    def __init__(self,level_data,surface): 
        
        # セットアップ
        self.display_surface = surface
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
        player_x = player.rect.centerx
        direction_x = Game.direction_num
        if player_x < 20 and direction_x < 0: 
            self.world_shift = 8
        elif player_x > 1000 and direction_x > 0:
            self.world_shift = -8
        else:
            self.world_shift = 0
    
    # プレイヤーとブロックの当たり判定        
    def movement_collision(self):
        player = self.player.sprite
        flag = pygame.sprite.spritecollide(player, self.tiles.sprites(), False)
        if len(flag) != 0:
            return True
    
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
        # self.collided()
        
        # ブロック(タイル)
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x() 
        self.re_start()
        
        # プレイヤー
        self.player.update()
        self.player.draw(self.display_surface)  
        
        # 敵
        self.enemy.update(self.world_shift)
        self.enemy.draw(self.display_surface)
        self.scroll_x() 

    # マップ(仮)
    map1 = (
    (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3),
    (7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3),
    (2,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3),
    (0,0,0,2,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3),
    (0,0,0,0,0,0,1,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3),
    (0,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
    (2,2,0,0,0,0,0,1,2,1,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
    (0,0,0,0,0,0,0,3,0,0,2,2,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,0,0,0,3),
    (0,0,0,0,0,2,2,3,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,3),
    (6,0,2,2,0,0,0,3,6,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,1,1,0,0,0,3),
    (3,3,0,0,0,0,0,3,2,1,1,1,1,1,2,0,1,1,1,2,2,3,0,1,2,3,3,0,2,2,3))

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

    map3 = (
    (1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
    (0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
    (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
    (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
    (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,0),
    (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
    (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
    (0,9,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
    (1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
    (0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
    (1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0))
    
    map_list = [map1, map2, map3]

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
