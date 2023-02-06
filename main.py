import pygame, sys, random
from pygame.locals import *
from game import Game, Phase
from filed import Filed

pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()
Game.surface = pygame.display.set_mode((Game.SCREEN_WIDTH,Game.SCREEN_HEIGHT))
pygame.display.set_caption("***NYAN QUEST***")

# ゲームの初期化処理
def init_game_info():
    Game.is_gameover = False
    Game.phase = Phase.TITLE
    Game.hp = 100
    Game.field = Filed(Filed.map_list[Game.map_no])

# フォント    
font = pygame.font.Font("font/Ronde-B_square.otf", 55)       
msg_font = pygame.font.Font("font/Ronde-B_square.otf", 45)   
    
# ガチャメッセージ・SE
gacha_msg = font.render("アイテムが残っていますもう一度回しますか？", True, (0,0,0))
gacha_pic_msg = font.render("結果発表！！！", True, (0,0,0))
gacha_error_msg = font.render("アイテムが足りません！また集めたら来てね！", True, (0,0,0))
gacha_se = pygame.mixer.Sound("music/se/gacha_se.wav")

# ガチャ画像
gacha_bg = pygame.image.load("bg_images/gacha_img.png")
gacha_neko1 = pygame.image.load("bg_images/gg1.png")
gacha_neko2 = pygame.image.load("bg_images/gg2.png")
gacha_neko3 = pygame.image.load("bg_images/gg3.png")
gacha_neko4 = pygame.image.load("bg_images/gg4.png")
gacha_neko5 = pygame.image.load("bg_images/gg5.png")
g_list = [gacha_neko1, gacha_neko2, gacha_neko3, gacha_neko4, gacha_neko5]
stop1 = 0
stop2 = 0
chara0 = pygame.image.load("chara_images/gacha/0.png")
chara1 = pygame.image.load("chara_images/gacha/1.png")
chara2 = pygame.image.load("chara_images/gacha/2.png")
chara3 = pygame.image.load("chara_images/gacha/3.png")
# ガチャ処理
def neko_gacha():
    count = 0
    global stop1, stop2
    pos = (350,200)
    # 確率
    prob = [0.3, 0.8, 0.6, 0.5] 
    # ガチャ一回につき、一体排出
    PIC = 1
    obtain_cara = None
    chara_list = [chara0, chara1, chara2, chara3]
    #Game.gacha_count += 1
    # 所持アイテムが50以下だったら
    if Game.item < 50:
        Game.gacha = False
        Game.surface.fill((255,255,255))
        Game.surface.blit(gacha_error_msg, [15,300]) 
        #Game.gacha_count = 0
         
    # 所持アイテムが50以上だったらガチャを回す
    elif Game.item >= 50:
        Game.gacha = True
        if Game.gacha:
            if Game.on_okkey():
                # Game.print_flag = False
                stop2 = 0
                #Game.gacha_count += 1
                obtain_cara = random.choices(chara_list , weights=prob, k=PIC)
                Game.pic_chara = obtain_cara[0]
                Game.chara_no = chara_list.index(Game.pic_chara) 
                Game.anime_flag = True 
                Game.item -= 50     # アイテムを消費
                     
        if Game.anime_flag:
            count = Game.count % 10
            if count >= len(g_list):
                count = 0
                stop1 += 1
            Game.surface.blit(g_list[count], (0,0))
            if stop1 >= 20:
                Game.anime_flag = False
                Game.print_flag =True
                stop1 = 0 

        elif Game.print_flag:
            stop2 += 1
            Game.surface.fill((0,50,100))
            Game.surface.blit(gacha_pic_msg, [100,50])
            Game.surface.blit(Game.pic_chara, (pos))      # 結果表示
            if Game.item >= 50 and stop2 >= 20:
                Game.surface.blit(gacha_msg, [15,500])

        return Game.chara_no

# 音楽読み込み
m1 = pygame.mixer.Sound("music/1.wav") 
m1.set_volume(0.05)
m2 = pygame.mixer.Sound("music/2.wav") 
m2.set_volume(0.05)
m3 = pygame.mixer.Sound("music/3.wav") 
m3.set_volume(0.05)
music_flag = 1

# 画像読み込み
title_bg = pygame.image.load("bg_images/title_img.png")
start_bg = pygame.image.load("bg_images/start_img.png")
map1_bg = pygame.image.load("bg_images/map1_img.png")
boss_bg = pygame.image.load("bg_images/boss_stage_img.png")
gameover_bg = pygame.image.load("bg_images/gameover_img.png")
gameclear_bg = pygame.image.load("bg_images/gameclear_img.png")
key_menu_img = pygame.image.load("bg_images/key_menu_img.png")
frame_img = pygame.image.load("bg_images/frame_img.png")
# メッセージ
retry_msg1 = msg_font.render("RESTART : PUSH ENTERKEY", True, (0,47,129))
retry_msg2 = msg_font.render("RESTART : PUSH ENTERKEY", True, (205,220,233))
retry_msg_list = [retry_msg1, retry_msg2]
clear_msg1 = msg_font.render("RESTURN TITLE : PUSH ENTERKEY", True, (255,125,0))
clear_msg2 = msg_font.render("RESTURN TITLE : PUSH ENTERKEY", True, (25,203,138))
clear_msg_list = [clear_msg1, clear_msg2]

# メッセージ点滅
def flash_masage(image_list,pos):
    msg_count = 0
    if Game.count % 50 == 0:
        msg_count = 0
    elif Game.count % 50 == 25:
        msg_count = 1 
    Game.surface.blit(image_list[msg_count], pos)

# メイン処理
def main():                 
    # ゲーム情報の初期化
    init_game_info() 
    
    while True:
        Game.surface.fill((0,0,0))
        Game.count += 1     # ゲームカウンタ
        Game.check_event()
        Game.move_flag = False
        global music_flag
        Game.map = 0
        
        # タイトル画面
        if Game.phase == Phase.TITLE:
            if music_flag == 1:
                m1.play(-1)
                music_flag = 0
            Game.surface.blit(title_bg,(0,0))
            if Game.on_okkey():
                Game.phase = Phase.START

        # スタート画面
        elif Game.phase == Phase.START:
            Game.wait_count -= 1
            Game.surface.blit(start_bg,(0,0))
            # カウントダウン表示
            if Game.wait_count % 30 == 0:
                Game.count_down -= 1
            Game.count_text = str(Game.count_down).rjust(3) if Game.wait_count > 0 else 'ENTER!'
            Game.surface.blit(font.render(Game.count_text, True, (0, 0, 0)), (10, 650))
            # pygame.display.flip()
            if Game.on_0key(): # 仮
                Game.phase = Phase.MAP 
                if music_flag == 0:
                    m1.stop()
                    music_flag = 2

            elif Game.wait_count <= 0:
                if Game.on_okkey():
                    Game.phase = Phase.MAP 
                    Game.move_flag = True
                    if music_flag == 0:
                        m1.stop()
                        music_flag = 2
  
        # マップ画面        
        elif Game.phase == Phase.MAP:
            if music_flag ==2:
                m2.play(-1)
                music_flag = 0
            # Game.surface.blit(gacha_bg,(0,0))
            if Game.count % 5 == 0:
                Game.player_count += 1
            if Game.count % 9 == 0:
                Game.enemy_count += 1
            Game.surface.fill((128,224,235))
            # 背景
            Game.surface.blit(map1_bg, (0, 0))
            # マップ表示
            Game.field.run()
            # 操作方法表示
            Game.surface.blit(key_menu_img,(1000,10))
            # アイテムカウンタ
            Game.surface.blit(font.render(str(Game.item), True, (0, 0, 0)), (10, 30))
            # HP
            Game.surface.blit(font.render(str(Game.hp), True, (0, 0, 0)), (10, 100))
            # フレーム
            Game.surface.blit(frame_img, (0, 0))
            
            # ガチャ画面へ
            if Game.on_gkey():
                Game.phase = Phase.GACHAGACHA
                if music_flag == 0:
                    m2.stop()
                    music_flag = 3
                    
            # ボスマップへ
            elif Game.boss_flag:
                Game.phase = Phase.BOSS
                if music_flag == 0:
                    m2.stop()
                    music_flag = 4
                    
            # HPが０になったらゲームオーバー
            if Game.is_gameover:
                Game.phase = Phase.GAME_OVER
                if music_flag == 0:
                    m2.stop()
                    music_flag = 5

        # ボスマップ画面
        if Game.phase == Phase.BOSS:
            Game.boss_map = True
            Game.surface.blit(boss_bg, (0, 0))
            if music_flag == 4:
                pass
            if Game.on_gkey():
                Game.phase = Phase.GACHAGACHA
                if music_flag == 0:
                    m2.stop()
                    music_flag = 3

            if Game.is_clear:
                Game.boss_flag = False
                Game.phase = Phase.GAME_CLEAR
                
        # ガチャ画面
        elif Game.phase == Phase.GACHAGACHA:
            if music_flag == 3:
                m3.play(-1)
                music_flag = 0
            Game.surface.blit(gacha_bg,(0,0))
            neko_gacha()
            # 戻るボタンを押したら、マップ画面へ戻る
            if Game.on_returnkey():
                Game.print_flag = False
                if music_flag == 0:
                    m3.stop()
                    music_flag = 2
                # 元々いたマップに戻る
                if Game.boss_map:
                    Game.phase = Phase.BOSS
                else:
                    Game.phase = Phase.MAP
   
        # ゲームオーバー           
        elif Game.phase == Phase.GAME_OVER:
            if music_flag == 5:
                m2.play(-1)
                music_flag = 0
            Game.surface.blit(gameover_bg, (0,0))
            flash_masage(retry_msg_list, [420,650])
        
            if Game.on_okkey():
                if music_flag == 0:
                    m2.stop()
                Game.is_gameover = False
                main()
                
        # ゲームクリア
        elif Game.phase == Phase.GAME_CLEAR:
            Game.surface.blit(gameclear_bg, (0,0))
            flash_masage(clear_msg_list, [380,650])
            if Game.on_okkey():
                # if music_flag == 0:
                #     m2.stop()
                Game.is_gameclear = False
                main()
  
        pygame.display.update()
        clock.tick(30)

if __name__ == '__main__':
    main()
        