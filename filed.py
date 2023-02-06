import pygame
from tiles import Tile
from player import Player, Atack
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
       
       all = pygame.sprite.RenderUpdates()   # 描画グループ 仮↓
       self.enemy = pygame.sprite.Group()    # 敵
       self.atack = pygame.sprite.GroupSingle()
       Atack.containers = all
       Player.containers = all
       Enemy.containers = all, self.enemy

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
        # flag = pygame.sprite.spritecollide(player, self.tiles.sprites(), False)
        flag = pygame.sprite.spritecollide(player, self.tiles, False)
        # if len(flag) != 0:
        #     return True
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
            Game.se_flag = 1
            Game.hp -= 5
            return True
            
    # アタック判定          
    def step_on_collision(self):
        player = self.player.sprite
        step_on_enemy = pygame.sprite.spritecollide(player, self.enemy, True)
        if step_on_enemy:
            oldrect = player.rect
            for enemy in step_on_enemy:
            # 上からは踏み攻撃 
                if oldrect.top < enemy.rect.top < oldrect.bottom < enemy.rect.bottom:
                    Game.item += 40
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
        self.enemy.update(self.world_shift)
        self.enemy.draw(Game.surface)
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
    [3,5,0,0,0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0],
    [3,2,2,0,0,0,0,0,0,2,2,2,0,0,0,0,0,0,0,0,0,0,0,5,0,0,0,0,0,0],
    [3,0,0,0,2,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,2,2,0,0,0],
    [3,0,0,0,0,0,1,2,0,0,0,1,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0,0,0,0],
    [3,0,22,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,5,0,0,0,7],
    [3,2,2,0,0,0,0,1,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,2,0,0,2,4],
    [3,0,0,0,1,5,1,0,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3],
    [3,0,0,0,0,2,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0,3],
    [3,5,0,1,5,0,0,0,0,0,0,0,0,0,0,0,5,0,0,4,0,0,0,0,0,1,1,2,0,3],
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

