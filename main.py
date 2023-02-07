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
    Game.item = 0
    Game.field = Filed(Filed.map_list[0])
    Game.field1 = Filed(Filed.map_list[1])

# フォント    
font = pygame.font.Font("font/Ronde-B_square.otf", 55)       
msg_font = pygame.font.Font("font/Ronde-B_square.otf", 45)   
count_font = pygame.font.Font("font/Ronde-B_square.otf", 30)  
 
# メッセージ点滅
def flash_masage(image_list,pos):
    msg_count = 0
    if Game.count % 50 <= 24:
        msg_count = 0
    elif Game.count % 50 <= 49:
        msg_count = 1 
    Game.surface.blit(image_list[msg_count], pos)
    
# ガチャメッセージ・SE
not_gacha_flag = True
gacha_msg = font.render("アイテムが残っていますもう一度回しますか？", True, (0,0,0))
gacha_pic_msg = font.render("結果発表！！！", True, (0,0,0))
gacha_error_msg = font.render("アイテムが足りません！また集めたら来てね！", True, (0,0,0))
map_return_msg1 = msg_font.render("RETURN MAP : R-KEY", True, (255,0,0))
map_return_msg2 = msg_font.render("RETURN MAP : R-KEY", True, (255,187,189))
map_return_msg_list = [map_return_msg1, map_return_msg2]
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
    global stop1, stop2, not_gacha_flag
    pos = (350,200)
    # 確率
    prob = [0.3, 0.8, 0.6, 0.5] 
    # ガチャ一回につき、一体排出
    PIC = 1
    obtain_cara = None
    chara_list = [chara0, chara1, chara2, chara3]
    if Game.item >= 50:
        not_gacha_flag = False
    
    # 所持アイテムが50以下だったら
    if not_gacha_flag:
        Game.gacha = False
        Game.surface.fill((248,0,0))
        pygame.draw.rect(Game.surface, (255,255,255), (30,30,1140,644))
        Game.surface.blit(gacha_error_msg, [20,300]) 
        flash_masage(map_return_msg_list, [400,500])
         
    # 所持アイテムが50以上だったらガチャを回す
    elif not_gacha_flag == False:
        Game.se_flag = 4
        stop2 += 1
        Game.gacha = True
        if stop2 >= 20:
            if Game.gacha:
                if Game.on_okkey():
                    stop2 = 0
                    obtain_cara = random.choices(chara_list , weights=prob, k=PIC)
                    Game.pic_chara = obtain_cara[0]
                    Game.chara_no = chara_list.index(Game.pic_chara) 
                    Game.anime_flag = True          
                if Game.anime_flag:
                    count = Game.count % 10
                    if count >= len(g_list):
                        count = 0
                        stop1 += 1
                    Game.surface.blit(g_list[count], (0,0))
                    if stop1 >= 20:
                        Game.item -= 50     # アイテムを消費
                        Game.anime_flag = False
                        Game.print_flag =True
                        stop1 = 0 
                if Game.print_flag:
                    Game.surface.fill((0,50,100))
                    Game.surface.blit(gacha_pic_msg, [100,50])
                    Game.surface.blit(Game.pic_chara, (pos))      # 結果表示
                    stop2 += 0
                    if Game.item >= 50:
                        if stop2 >= 20:
                            Game.surface.blit(gacha_msg, [15,500])
                            if Game.on_okkey():
                                not_gacha_flag = False   
                                Game.print_flag = False 
                                Game.surface.fill((248,0,0))
                                pygame.draw.rect(Game.surface, (255,255,255), (30,30,1140,644))
                                Game.surface.blit(gacha_error_msg, [20,300]) 
                                flash_masage(map_return_msg_list, [400,500])
                    else:
                        if Game.on_okkey():
                            Game.gacha = False
                            not_gacha_flag = True
                            Game.print_flag = False 

        return Game.chara_no

# BGM
music_flag = 1
t_s_bgm = pygame.mixer.Sound("music/title_start_bgm.wav") 
t_s_bgm.set_volume(0.05)
map_bgm = pygame.mixer.Sound("music/map_bgm.wav") 
map_bgm.set_volume(0.05)
gacha_bgm = pygame.mixer.Sound("music/gacha_bgm.wav") 
gacha_bgm.set_volume(0.05)
g_o_bgm = pygame.mixer.Sound("music/game_over_bgm.wav") 
g_o_bgm.set_volume(0.3)
boss_bgm = pygame.mixer.Sound("music/boss_bgm.wav") 
boss_bgm.set_volume(0.3)

# SE
se1 = pygame.mixer.Sound("music/se/atack_se.wav")
se1.set_volume(0.3)
se2 = pygame.mixer.Sound("music/se/game_over_se.wav")
se2.set_volume(0.2)
se3 = pygame.mixer.Sound("music/se/damage_se.wav")
se3.set_volume(0.2)

# 画像読み込み
title_bg = pygame.image.load("bg_images/title_img.png")
start_bg = pygame.image.load("bg_images/start_img.png")
map1_bg = pygame.image.load("bg_images/map1_img.png")
gameover_bg = pygame.image.load("bg_images/gameover_img.png")
gameclear_bg = pygame.image.load("bg_images/gameclear_img.png")
key_menu_img = pygame.image.load("bg_images/key_menu_img.png")
frame_img = pygame.image.load("bg_images/frame_img.png")
# メッセージ
title_msg1 = msg_font.render("START : PUSH ENTERKEY", True, (255,125,0))
title_msg2 = msg_font.render("START : PUSH ENTERKEY", True, (25,203,138))
title_msg_list = [title_msg1, title_msg2]
retry_msg1 = msg_font.render("RESTART : PUSH ENTERKEY", True, (0,47,129))
retry_msg2 = msg_font.render("RESTART : PUSH ENTERKEY", True, (205,220,233))
retry_msg_list = [retry_msg1, retry_msg2]
clear_msg1 = msg_font.render("RESTURN TITLE : PUSH ENTERKEY", True, (255,125,0))
clear_msg2 = msg_font.render("RESTURN TITLE : PUSH ENTERKEY", True, (25,203,138))
clear_msg_list = [clear_msg1, clear_msg2]
item_msg = count_font.render("ちゅ～る", True, (0,0,0))

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
        Game.field.game_over_judge()
        
        # タイトル画面
        if Game.phase == Phase.TITLE:
            if music_flag == 1:
                t_s_bgm.play(-1)
                music_flag = 0
            Game.surface.blit(title_bg,(0,0))
            flash_masage(title_msg_list, [400,550])
            if Game.on_okkey():
                Game.phase = Phase.START

        # スタート画面
        elif Game.phase == Phase.START:
            Game.wait_count -= 1
            Game.surface.blit(start_bg,(0,0))
            # カウントダウン表示
            if Game.wait_count % 30 == 0:
                Game.count_down -= 1
            Game.count_text = str(Game.count_down).rjust(3) if Game.wait_count > 0 else 'PUSH ENTER!'
            Game.surface.blit(font.render(Game.count_text, True, (0, 0, 0)), (50, 600))
            if Game.on_0key(): # 仮
                Game.phase = Phase.MAP 
                if music_flag == 0:
                    t_s_bgm.stop()
                    music_flag = 2

            elif Game.wait_count <= 0:
                if Game.on_okkey():
                    if music_flag == 0:
                        t_s_bgm.stop()
                        music_flag = 2
                    Game.phase = Phase.MAP 
                    Game.move_flag = True
    
        # マップ画面        
        elif Game.phase == Phase.MAP:
            if music_flag ==2:
                map_bgm.play(-1)
                music_flag = 0
            if Game.count % 5 == 0:
                Game.player_count += 1
            if Game.count % 9 == 0:
                Game.enemy_count += 1
            if Game.count % 9 == 0:
                Game.enemy_count += 1
            Game.surface.fill((226,243,255))
            # 背景
            Game.surface.blit(map1_bg, (0, 0))
            # マップ表示
            Game.field.run()
            # フレーム
            Game.surface.blit(frame_img, (0, 0))
            # 操作方法表示
            Game.surface.blit(key_menu_img,(950,45))
            # アイテムカウンタ
            Game.surface.blit(item_msg,(50,60))
            Game.surface.blit(msg_font.render(": "+str(Game.item), True, (0, 0, 0)), (180, 50))
            # HP
            Game.surface.blit(msg_font.render("HP : "+str(Game.hp), True, (0, 0, 0)), (60, 100))
            
            # 効果音
            if Game.se_flag == 1:
                se1.play(0)
                Game.se_flag = 0
            if Game.se_flag == 3:
                se3.play(0)
                Game.se_flag = 0
            if music_flag == 4:
                music_flag = 0
            
            # ガチャ画面へ
            if Game.on_gkey():
                Game.phase = Phase.GACHAGACHA
                if Game.se_flag == 4:
                    gacha_se.play(0)
                    Game.se_flag = 0
                if music_flag == 0:
                    map_bgm.stop()
                    music_flag = 3
                    
            # ボスマップへ
            if Game.boss_map:
                Game.phase = Phase.BOSS
                if music_flag == 0:
                    map_bgm.stop()
                    music_flag = 4

            # HPが０になったらゲームオーバー
            if Game.is_gameover:
                Game.phase = Phase.GAME_OVER
                if music_flag == 0:
                    map_bgm.stop()
                    Game.se_flag = 9
                    music_flag = 9
                    
            # クリア画面
            if Game.is_clear:
                Game.boss_flag = False
                Game.phase = Phase.GAME_CLEAR
                
        # ガチャ画面
        elif Game.phase == Phase.GACHAGACHA:
            if music_flag == 3:
                gacha_bgm.play(-1)
                music_flag = 0
            Game.surface.blit(gacha_bg,(0,0))
            neko_gacha()
            # アイテムカウンタ
            Game.surface.blit(item_msg,(50,60))
            Game.surface.blit(frame_msg,(50,60))
            Game.surface.blit(msg_font.render(": "+str(Game.item), True, (0, 0, 0)), (180, 50))

            # 戻るボタンを押したら、マップ画面へ戻る
            if Game.on_returnkey():
                Game.print_flag = False
                if music_flag == 0:
                    gacha_bgm.stop()
                    music_flag = 2
                # 元々いたマップに戻る
                if Game.boss_map:
                    if music_flag== 0:
                        gacha_bgm.stop()
                        music_flag = 4
                    Game.phase = Phase.BOSS
                else:
                    if music_flag== 0:
                        gacha_bgm.stop()
                        music_flag = 2
                    Game.phase = Phase.MAP
                    
        # ボスマップ画面
        if Game.phase == Phase.BOSS:
            if music_flag ==2:
                map_bgm.play(-1)
                music_flag = 0
            if Game.count % 5 == 0:
                Game.player_count += 1
            if Game.count % 9 == 0:
                Game.enemy_count += 1
            if Game.count % 9 == 0:
                Game.enemy_count += 1
            Game.surface.fill((191,104,98))
            Game.surface.blit(map1_bg, (0, 0))
            Game.field.run()
            # フレーム
            Game.surface.blit(frame_img, (0, 0))
            # 操作方法表示
            Game.surface.blit(key_menu_img,(950,45))
            # アイテムカウンタ
            Game.surface.blit(item_msg,(50,60))
            Game.surface.blit(msg_font.render(": "+str(Game.item), True, (0, 0, 0)), (180, 50))
            # HP
            Game.surface.blit(msg_font.render("HP : "+str(Game.hp), True, (0, 0, 0)), (60, 100))
            
            # 効果音
            if Game.se_flag == 1:
                se1.play(0)
                Game.se_flag = 0
            if Game.se_flag == 3:
                se3.play(0)
                Game.se_flag = 0
            if music_flag == 4:
                music_flag = 0
            if music_flag == 4:
                pass
            
            if Game.on_gkey():
                Game.phase = Phase.GACHAGACHA
                if music_flag == 0:
                    
                    music_flag = 3

            if Game.is_clear:
                Game.boss_flag = False
                Game.phase = Phase.GAME_CLEAR

        # ゲームオーバー           
        elif Game.phase == Phase.GAME_OVER:
            if music_flag == 9:
                g_o_bgm.play(-1)
                music_flag = 0
            if Game.se_flag == 9:
                se2.play(0)
                Game.se_flag = 0
            Game.surface.blit(gameover_bg, (0,0))
            flash_masage(retry_msg_list, [390,650])
        
            if Game.on_okkey():
                if music_flag == 0:
                    g_o_bgm.stop()
                    music_flag = 1
                Game.is_gameover = False
                main()
                
        # ゲームクリア
        elif Game.phase == Phase.GAME_CLEAR:
            Game.surface.blit(gameclear_bg, (0,0))
            flash_masage(clear_msg_list, [350,650])
            if Game.on_okkey():
                # if music_flag == 0:
                #     m2.stop()
                Game.is_gameclear = False
                main()
  
        pygame.display.update()
        clock.tick(30)

if __name__ == '__main__':
    main()
        