import pygame, sys
from pygame.locals import *
from enum import Enum

class Game:
# 基本 
    # 定数
    TILE_SIZE = 64          # ブロックの１辺
    SCREEN_WIDTH = 1200     # ウィンドウの幅
    SCREEN_HEIGHT = 704     # ウィンドウの高さ
    
    # クラス変数
    keymap = []             # キーマップ
    field = None            # フィールド
    field1 = None
    surface = None          # 描画
    phase = None            # フェーズ
    count = 0               # ゲームカウンタ
    is_gameover = False     # ゲームオーバーフラグ
    is_clear = False        # ゲームクリアフラグ
    
    # タイマー処理
    count_down, wait_count, count_text = 10, 300, '10'.center(5)

    # ガチャ処理等
    item = 0                    # 所持アイテム(初期値：０)
    gacha = True                # ガチャフラグ
    pic_chara = 0               # ピックキャラ
    anime_flag = False          # ガチャ回転中アニメーションフラグ
    print_flag = False          # 結果表示フラグ
    command_able =True          # キー押下判定用フラグ
    
    # プレイヤー(キャラクター)
    player_pos = None
    chara_no = 0        # キャラクターナンバー(初期値は０)
    hp = 100
    hp_list = [100, 20, 40, 70]
    se_flag = 0     # SE
                      
    # プレイヤー処理関連
    jump_flag = False          # ジャンプ   
    
    # 画面等処理関連
    map_no = 0              # マップ番号(初期値は０)
    direction_num = 0       # マップスクロール
    move_flag = True        # 移動可能フラグ
    block_no = 0            # ブロック番号
    enemy_no = 0            # エネミーキャラ番号
    boss_no = 0
    boss_flag = False       # ボスフラグ
    boss_map = False
    
    player_count = 0      # プレイヤーキャラアニメーション番号
    enemy_count = 0       # エネミーキャラアニメーション番号
    boss_count = 0        # ボスキャラアニメーション番号
    atack_count = 0
    
    # イベントチェック処理
    @classmethod
    def check_event(cls):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if not event.key in Game.keymap:
                    Game.keymap.append(event.key)
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == KEYUP:
                Game.keymap.remove(event.key)
                

    # キーチェック処理
    @classmethod
    def on_rightkey(cls):
        return K_RIGHT in Game.keymap
    @classmethod
    def on_leftkey(cls):
        return K_LEFT in Game.keymap
    @classmethod
    def on_spacekey(cls):
        return K_SPACE in Game.keymap
    @classmethod
    def on_enterkey(cls):
        return K_RETURN in Game.keymap
    
    @classmethod
    def on_okkey(cls):
        if Game.command_able:
            if Game.on_enterkey():
                Game.command_able = False
                return True
            else:
                return False
        else:
            if not Game.on_enterkey():
                Game.command_able = True   
        return False    

    # ガチャ
    @classmethod        
    def on_gkey(cls):
        return K_g in Game.keymap
    # 戻る
    @classmethod
    def on_returnkey(cls):
        return K_r in Game.keymap
    # 仮用
    @classmethod
    def on_0key(cls):
        return K_0 in Game.keymap
    # 攻撃 右方向
    @classmethod
    def on_ckey(cls):
        return K_c in Game.keymap
    # 攻撃 左方向
    @classmethod
    def on_xkey(cls):
        return K_x in Game.keymap
    
# 段階処理
class Phase(Enum):
    TITLE = 1           # タイトル画面
    START = 10          # スタート    
    MAP = 20            # マップ 
    BOSS = 30
    
    GACHAGACHA = 50      # ガチャ画面
    # GACHARESULT = 60     # ガチャ結果画面
    
    GAME_CLEAR = 77          # ゲームクリア
    GAME_OVER = 99      # ゲームオーバー
