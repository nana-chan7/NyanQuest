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
    keymap = []     
    field = None 
    surface = None
    phase = None
    count = 0               # ゲームカウンタ
    is_gameover = False     # ゲームオーバーフラグ
    
    # タイマー(カウンタ―)関連
    count_down, wait_count, count_text = 2, 120, '2'.rjust(3) # 5, 300, '5'.rjust(3)

    # ガチャ関連
    item = 0                  # 所持アイテム(初期値：０)
    gacha_error_flag = False    # ガチャ可能フラグ
    obtain_cara_img = None      # 排出したキャラ
    my_chara_list = []          # 所持キャラリスト ※重複したくない
    gacha_count = 0
    gacha = True

    # プレイヤー(キャラクター)
    chara_no = 0        # キャラクターナンバー(初期値は０)
    # 全てのキャラリスト
    # CHARACTER_LIST1 = ["chara_images/obake_neko.png","chara_images/robo_neko.png","chara_images/fue_neko.png",
    #                     "chara_images/kotatu_neko.png","chara_images/natu_neko.png","chara_images/yume_neko.png"]         
    # CHARACTER_LIST = ["obake_neko","robo_neko","fue_neko"]
    
    # キャラクター画像ダウンロード characters_image_list

    # chara_list = ["chara_images/gacha/0.png","chara_images/gacha/1.png","chara_images/gacha/2.png","chara_images/gacha/3.png"]

                      
    # プレイヤー処理関連
    jump_flag = False           # ジャンプ
    # プレイヤー攻撃
    p_attack_flag = False       # アタックフラグ
    star_x, star_y = 0, 0       
    
    # 画面等処理関連
    map_no = 0              # マップ番号(初期値は０)
    direction_num = 0       # マップスクロール
    move_flag = True        # 移動可能フラグ
    block_no = 0            # ブロック番号
    enemy_no = 0            # エネミーキャラ番号
    boss_flag = False       # ボスフラグ
    
    player_count = 0      # プレイヤーキャラアニメーション番号
    enemy_count = 0       # エネミーキャラアニメーション番号x 
    
    # 雑多組
    forward_len = 0     # 背景？
    bg_pos = 0      # 背景の位置
    player_pos = 0 ##
    player = None
    enemy_x, enemy_y = 0, 0
    
    chara_image = None
    number = 0
    start = False
    
    command_able =True      # キー操作
    print_flag = False
    pic_chara = 0
    music_stop = False
    music_flag = 0
    video_flag = False
    


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
    # @classmethod
    # def on_upkey(cls):
    #     return K_UP in Game.keymap
    # @classmethod
    # def on_downkey(cls):
    #     return K_DOWN in Game.keymap
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

    # # メニュー
    # @classmethod        
    # def on_mkey(cls):
    #     return K_m in Game.keymap
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
    # 仮用
    @classmethod
    def on_9key(cls):
        return K_9 in Game.keymap
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
    GACHARESULT = 60      # ガチャ結果画面
    
    GAME_OVER = 99      # ゲームオーバー
