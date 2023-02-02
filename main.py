import pygame
import sys, cv2 
import numpy as np
import random
from pygame.locals import *
from game import Game, Phase
from filed import Filed

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
Game.surface = pygame.display.set_mode((Game.SCREEN_WIDTH,Game.SCREEN_HEIGHT))
pygame.display.set_caption("***NYAN QUEST***")
Game.field = Filed(Filed.map_list[Game.map_no])

# ゲームの初期化処理
def init_game_info():
    Game.is_gameover = False
    Game.phase = Phase.TITLE
    
# フォント    
font = pygame.font.Font("font/Ronde-B_square.otf", 55)       


# ガチャメッセージ
gacha_msg = font.render("アイテムが残っていますもう一度回しますか？", True, (255,255,255))
gacha_error_msg = font.render("アイテムが足りません！また集めたら来てね！", True, (255,255,255))
gacha_se = pygame.mixer.Sound("music/se/gacha_se.wav")

# 画像
gacha_neko1 = pygame.image.load("bg_images/gg1.png")
gacha_neko2 = pygame.image.load("bg_images/gg2.png")
gacha_neko3 = pygame.image.load("bg_images/gg3.png")
gacha_neko4 = pygame.image.load("bg_images/gg4.png")
gacha_neko5 = pygame.image.load("bg_images/gg5.png")

chara0 = pygame.image.load("chara_images/gacha/0.png")
chara1 = pygame.image.load("chara_images/gacha/1.png")
chara2 = pygame.image.load("chara_images/gacha/2.png")
chara3 = pygame.image.load("chara_images/gacha/3.png")

# アニメーション設定  
def animation():
    g_list = [gacha_neko1, gacha_neko2, gacha_neko3, gacha_neko4, gacha_neko5]
    count = Game.count % 10
    for i in range(10):
        if count >= len(g_list):
            count = 0
        Game.surface.blit(g_list[count], ((0, 0)))
    Game.print_flag = True

# ガチャ処理
def neko_gacha():
    pos = (350,200)
    # 確率
    prob = [0.3, 0.8, 0.6, 0.5] 
    # ガチャ一回につき、一体排出
    PIC = 1
    obtain_cara = None
    chara_list = [chara0, chara1, chara2, chara3]
    color_list = [(255,0,0), (0,255,0), (0,0,255), (100,50,0)]
    pic_chara = None
    Game.gacha_count += 1
    # 所持アイテムが50以下だったら
    if Game.item < 50:
        Game.gacha = False
        Game.surface.blit(gacha_error_msg, [15,300]) 
        Game.gacha_count = 0
         
    # 所持アイテムが10以上だったらガチャを回す
    elif Game.item >= 50:
        Game.gacha = True
        if Game.gacha:
            if Game.on_okkey():
                Game.gacha_count += 1
                Game.item -= 50     # アイテムを消費
                obtain_cara = random.choices(chara_list , weights=prob, k=PIC)
                Game.pic_chara = obtain_cara[0]
                Game.chara_no = chara_list.index(Game.pic_chara)
                # Game.obtain_cara_img = pygame.image.load(obtain_cara[0])
                # Game.my_chara_list.append(obtain_cara[0])       # 手持ちに追加     
                Game.anime_flag = True
        if Game.anime_flag:
            animation()
        elif Game.print_flag:
            Game.anime_flag = False
            Game.surface.blit(Game.pic_chara, (pos))      # 結果表示
        if Game.gacha_count >= 1000 and Game.item >= 50:
            Game.surface.blit(gacha_msg, [15,300]) 
            if Game.on_okkey():
                Game.gacha = True
                Game.print_flag = False
                
        return Game.chara_no


# # 音楽読み込み
# pygame.mixer.Channel(0)
# pygame.mixer.music.load("music/1.wav") 
# m1 = pygame.mixer.Sound("music/1.wav") 
# m2 = pygame.mixer.Sound("music/2.wav") 
# m3 = pygame.mixer.Sound("music/3.wav") 


# 画像読み込み
title_bg = pygame.image.load("bg_images/title_img.png")
start_bg = pygame.image.load("bg_images/start_img.png")
gacha_bg = pygame.image.load("bg_images/gacha_img.png")
map1_bg = pygame.image.load("bg_images/map1_img.png")
gameover_bg = pygame.image.load("bg_images/gameover_img.png")
key_menu_img = pygame.image.load("bg_images/key_menu_img.png")

# メイン処理
def main():                 
    # ゲーム情報の初期化
    init_game_info() 
    
    while True:
        Game.surface.fill((0,0,0))
        # game_music()    # 音楽再生
        Game.count += 1     # ゲームカウンタ
        Game.item = Game.count # アイテム 一旦
        Game.check_event()
        Game.move_flag = False
        
        
    
        # global font
        
        # タイトル画面
        if Game.phase == Phase.TITLE:
            Game.music_flag = 1
            Game.surface.blit(title_bg,(0,0))
            if Game.on_enterkey():
                Game.phase = Phase.START
                Game.music_flag = 1

        # スタート画面
        elif Game.phase == Phase.START:
            
            Game.wait_count -= 1
            Game.surface.blit(start_bg,(0,0))
            # カウントダウン表示
            if Game.wait_count % 60 == 0:
                Game.count_down -= 1
            Game.count_text = str(Game.count_down).rjust(3) if Game.wait_count > 0 else 'ENTER!'
            Game.surface.blit(font.render(Game.count_text, True, (0, 0, 0)), (10, 650))
            # pygame.display.flip()
            if Game.on_0key(): # 仮
                Game.phase = Phase.MAP 
                Game.move_flag = True 
                Game.music_stop = True
            elif Game.wait_count <= 0:
                if Game.on_enterkey():
                    Game.phase = Phase.MAP 
                    Game.move_flag = True
                    Game.music_stop = True
            if Game.music_stop:
                pass
              
        # マップ画面        
        elif Game.phase == Phase.MAP:
            # Game.r_flag = True
            if Game.count % 10 == 0:
                Game.player_count += 1
            if Game.count % 20 == 0:
                Game.enemy_count += 1
            Game.surface.fill((128,224,235))
            # 背景
            Game.surface.blit(map1_bg, (0, 0))
            # # のスライド    
            # x = Game.forward_len % Game.SCREEN_WIDTH
            # Game.surface.blit(map1_bg, (-x, 0))
            # Game.surface.blit(map1_bg, (Game.SCREEN_WIDTH-x, 0))
            # マップ表示
            Game.field.run()
            # 操作方法表示
            Game.surface.blit(key_menu_img,(1000,10))
            # アイテムカウンタ
            Game.surface.blit(font.render(str(Game.item), True, (0, 0, 0)), (10, 30))

            if Game.on_gkey():
                Game.phase = Phase.GACHAGACHA
            elif Game.boss_flag:
                pass
            if Game.is_gameover:
                Game.phase = Phase.GAME_OVER
        # ボスマップ画面
        if Game.phase == Phase.BOSS:
            Game.map_no = 1
            Game.field.run()
                
        # ガチャ画面
        elif Game.phase == Phase.GACHAGACHA:
            Game.surface.blit(gacha_bg,(0,0))
            if Game.on_enterkey():
                Game.phase = Phase.GACHARESULT

        # ガチャ結果画面
        elif Game.phase == Phase.GACHARESULT:
            Game.surface.fill((200,100,100))
            neko_gacha()
            # 戻るボタンを押したら、マップ画面へ戻る
            if Game.on_returnkey():
                Game.phase = Phase.MAP

            # video()
   
        # ゲームオーバー           
        elif Game.phase == Phase.GAME_OVER:
            Game.surface.blit(gameover_bg,(0,0))
            if Game.on_enterkey():
                Game.is_gameover = False
                pygame.mixer.stop()
                main()
  
        pygame.display.update()
        clock.tick(60)
        

if __name__ == '__main__':
    main()
        