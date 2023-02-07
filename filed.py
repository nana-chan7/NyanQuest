import pygame
from tiles import Tile
from player import Player
from enemy import Enemy
# from enemy import Enemy, Boss
from game import Game
class Filed:

    def __init__(self,level_data): 
        
        # セットアップ
        self.setup_level(level_data)
        self.world_shift = 0    # 移動→背景も動くための ブロック タイル
        self.current_x = 0
        
        self.map = Game.map_no         # マップ番号(初期値は１)
        self.clear = False       # クリア判定
        
    # マップ(フィールド全体)処理
    def setup_level(self, layout):
       self.map = Game.map_no         # マップ番号(初期値は１)

       self.tiles = pygame.sprite.Group()           # ブロック タイル
       self.player = pygame.sprite.GroupSingle()    # プレイヤーキャラ
       
       all = pygame.sprite.RenderUpdates()   
       self.enemy = pygame.sprite.Group()           # 敵
       Player.containers = all
       Enemy.containers = all, self.enemy
       self.boss = pygame.sprite.GroupSingle()      
       
       
       
       for row_index, row in enumerate(layout):
           for col_index, cell in enumerate(row):
                x = col_index * Game.TILE_SIZE
                y = row_index * Game.TILE_SIZE
                # タイル ブロック
                Game.block_no = cell - 1 
                # 半ブロック 下半分  
                if cell == 1:
                    tile = Tile((x,y+32),Game.TILE_SIZE)
                    self.tiles.add(tile)
                # 半ブロック 上半分   
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
                Game.enemy_no = cell - 5
                if cell == 5:
                    enemy_sprite = Enemy((x,y),Game.TILE_SIZE)
                    self.enemy.add(enemy_sprite)  
                if cell == 6:
                    enemy_sprite = Enemy((x,y),Game.TILE_SIZE)
                    self.enemy.add(enemy_sprite)  
                # map1 ボスキャラ遷移用
                if cell == 7:
                    boss_sprite = Enemy((x,y),Game.TILE_SIZE)
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
        if flag:
            oldrect = player.rect
            for tile in flag:        
                # 左から衝突
                if oldrect.left < tile.rect.left < oldrect.right < tile.rect.right:
                    return True
                # 右から衝突
                if tile.rect.left < oldrect.left < tile.rect.right < oldrect.right:
                    return True
                # 上から衝突
                if oldrect.top < tile.rect.top < oldrect.bottom < tile.rect.bottom:
                    return True
                # 下から衝突
                if tile.rect.top < oldrect.top < tile.rect.bottom < oldrect.bottom:
                    return True
            
    # ダメージ判定
    def damage_collision(self):
        player = self.player.sprite
        flag = pygame.sprite.spritecollide(player, self.enemy.sprites(), False)
        if len(flag) != 0:
            Game.se_flag = 3
            Game.hp -= 5
            return True
        # マップ1でボスに接触するとボスマップへ遷移 
        flag_boss = pygame.sprite.spritecollide(player, self.boss.sprites(), False)
        # ボスマップの時はゲームクリア
        if len(flag_boss) != 0: 
            Game.se_flag = 3
            # if Game.boss_map:
            #     Game.is_clear = True
            if not Game.boss_flag:
                player.rect.x = 30
                player.rect.y = 30
                Game.boss_flag = True 
      
    # アタック判定          
    def step_on_collision(self):
        player = self.player.sprite
        step_on_enemy = pygame.sprite.spritecollide(player, self.enemy, True)
        if step_on_enemy:
            Game.se_flag = 1
            oldrect = player.rect
            for enemy in step_on_enemy:
            # 上からは踏み攻撃 
                if oldrect.top < enemy.rect.top < oldrect.bottom < enemy.rect.bottom:
                    Game.item += 40
                    return True

    # 描画処理
    def run(self):
        # プレイヤー
        self.player.update()
        self.player.draw(Game.surface)  
        # ブロック(タイル)
        if self.world_shift < 0:
            for i in range(-self.world_shift):
                self.tiles.update(-1)
                self.enemy.update(-1)
                self.boss.update(-1)
                if self.movement_collision():
                    self.tiles.update(1)
                    self.enemy.update(1)
                    self.boss.update(1)
                    break
                else:
                    self.player.sprite.rect.x -= 1
        elif self.world_shift > 0:
            for e in range(self.world_shift):
                self.tiles.update(1)
                self.enemy.update(1)
                self.boss.update(1)
                if self.movement_collision():
                    self.tiles.update(-1)
                    self.enemy.update(-1)
                    self.boss.update(-1)
                    break
                else:
                    self.player.sprite.rect.x += 1
                    
        self.tiles.draw(Game.surface)
        self.enemy.draw(Game.surface)
        
        self.scroll_x() 
        
        # クリア画面へ遷移
        if Game.is_clear:
            tiles = self.tiles.sprites()
            player = self.player.sprite
            enemies = self.enemy.sprites()
            for tile in tiles:
                tile.kill() 
            player.kill()
            for enemy in enemies:
                enemy.kill() 
        # ボスマップへ遷移            
        elif Game.boss_flag and not Game.is_clear:
            tiles = self.tiles.sprites()
            player = self.player.sprite
            enemies = self.enemy.sprites()
            for tile in tiles:
                tile.kill() 
            player.kill()
            for enemy in enemies:
                enemy.kill() 
            Game.map_no = 1
            player.rect.x = 30
            player.rect.y = 30
            Game.boss_flag = False
            self.setup_level(self.map2)
            self.run()
            
    # マップ(仮)
    map1 = [
    [4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
    [3,0,0,0,1,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,3],
    [3,6,0,0,0,0,0,0,0,0,6,0,0,0,0,0,0,0,1,0,2,2,2,0,0,0,0,0,6,3],
    [3,2,0,0,0,0,5,0,1,2,2,0,5,0,0,0,0,2,0,0,0,0,0,0,1,0,0,0,2,3],
    [3,0,0,0,1,2,2,0,0,0,0,0,2,2,2,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0],
    [3,0,9,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,1,0,0,0,0,0,0,7],
    [3,2,1,0,0,0,0,0,0,0,0,0,0,0,5,0,0,1,1,0,0,0,0,0,1,1,0,0,1,4],
    [3,0,0,0,2,2,6,0,0,0,0,0,0,2,2,1,0,0,0,0,5,0,0,0,0,0,0,2,0,3],
    [3,0,0,0,0,0,2,0,0,1,5,0,0,0,0,0,0,0,0,1,2,1,0,0,0,0,0,0,0,3],
    [3,0,0,0,2,0,0,4,0,3,4,0,0,6,0,0,1,1,0,0,0,0,0,6,0,0,0,0,5,3],
    [3,4,4,0,0,4,4,3,0,3,3,2,2,4,4,0,0,0,0,0,0,4,4,4,4,0,0,4,4,3]]

    map2 = [
    [4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4],
    [3,0,0,0,1,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,3],
    [3,6,0,0,0,0,0,0,0,0,6,0,0,0,0,0,0,0,1,0,2,2,2,0,0,0,0,0,6,3],
    [3,2,0,0,0,0,5,0,1,2,2,0,5,0,0,0,0,2,0,0,0,0,0,0,1,0,0,0,2,3],
    [3,0,0,0,1,2,2,0,0,0,0,0,2,2,2,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0],
    [3,0,9,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,1,0,0,0,0,0,0,7],
    [3,2,1,0,0,0,0,0,0,0,0,0,0,0,5,0,0,1,1,0,0,0,0,0,1,1,0,0,1,4],
    [3,0,0,0,2,2,6,0,0,0,0,0,0,2,2,1,0,0,0,0,5,0,0,0,0,0,0,2,0,3],
    [3,0,0,0,0,0,2,0,0,1,5,0,0,0,0,0,0,0,0,1,2,1,0,0,0,0,0,0,0,3],
    [3,0,0,0,2,0,0,4,0,3,4,0,0,6,0,0,1,1,0,0,0,0,0,6,0,0,0,0,5,3],
    [3,4,4,0,0,4,4,3,0,3,3,2,2,4,4,0,0,0,0,0,0,4,4,4,4,0,0,4,4,3]]

    map_list = [map1,map2]

    # map = [
    # [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    # [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    # [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    # [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    # [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    # [0,0,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    # [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    # [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    # [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    # [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    # [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]


