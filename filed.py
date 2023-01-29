import pygame
from tiles import Tile
from player import Player
from game import Game
from enemy import Enemy, Boss

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
                if cell == 1:
                    tile = Tile((x,y),Game.TILE_SIZE)
                    self.tiles.add(tile)
                if cell == 2:
                    tile = Tile((x,y),Game.TILE_SIZE)
                    self.tiles.add(tile)
                    
                # プレイヤー 
                if cell == 9:
                    player_sprite = Player((x,y))
                    self.player.add(player_sprite)
                # 敵(複数にする)
                if cell == 6:
                    enemy_sprite = Enemy((x,y),Game.TILE_SIZE)
                    self.enemy.add(enemy_sprite)
                # if cell == 7:
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
        #self.horizontal_movement_collision()
        # self.vertical_movement_collision()
        self.player.draw(self.display_surface)  
        
        # 敵
        # self.enemy.update()
        # self.vertical_movement_collision()
        # self.enemy.draw(self.display_surface)  
        
        self.enemy.update(self.world_shift)
        # self.damage()
        self.enemy.draw(self.display_surface)
        self.scroll_x() 
        # self.boss()
        # self.enemy.collided_player(self)

  
 
 
    # マップ(仮)
    map1 = (
    (6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1),
    (1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1),
    (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,1,1),
    (0,0,1,1,1,0,0,0,0,0,0,0,0,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,0,0,1,1),
    (0,9,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1),
    (0,0,0,0,0,0,0,6,0,0,0,0,0,0,0,1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1),
    (0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1),
    (2,2,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,1,1,1),
    (0,0,0,0,2,2,2,0,0,0,0,1,1,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1),
    (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1),
    (1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1))

    map2 = (
    (1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
    (0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
    (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
    (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
    (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
    (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
    (0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
    (0,9,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
    (1,1,1,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
    (0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
    (1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0))
