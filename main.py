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
    Game.surface.fill((226,243,255))
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
gacha_se = pygame.mixer.Sound("music/se/gacha_se.wav")
gacha_se.set_volume(0.7)
gacha_msg = font.render("何が出るかな？", True, (141,255,44))
re_map_msg = count_font.render("戻るときはRキーを押してね！", True, (0,0,0))
re_gacha_msg = font.render("アイテムが残っていますもう一度回しますか？", True, (255,95,148))
gacha_pic_msg = font.render("結果発表！！！", True, (255,60,39))
gacha_ok_msg = msg_font.render("アイテムが50個以上あります！ガチャを回しますか？", True, (0,0,0))
gacha_error_msg = font.render("アイテムが足りません！また集めたら来てね！", True, (0,0,0))
map_return_msg1 = msg_font.render("RETURN MAP : R-KEY", True, (255,0,0))
map_return_msg2 = msg_font.render("RETURN MAP : R-KEY", True, (255,187,189))
map_return_msg_list = [map_return_msg1, map_return_msg2]
enter_msg1 = msg_font.render("PUSH ENTERKEY", True, (255,125,0))
enter_msg2 = msg_font.render("PUSH ENTERKEY", True, (25,203,138))
enter_msg_list = [enter_msg1, enter_msg2] 

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
chara4 = pygame.image.load("chara_images/gacha/4.png")
chara5 = pygame.image.load("chara_images/gacha/5.png")

animation_flag = False
print_flag = False
# ガチャ処理
def neko_gacha():
    Game.blit_item = Game.item
    global stop1, stop2, animation_flag, print_flag
    # global not_gacha_flag
    pos = (500,30)
    # 確率
    prob = [0.3, 0.8, 0.6, 0.5, 0.4, 0.7] 
    # ガチャ一回につき、一体排出
    PIC = 1
    obtain_cara = None
    chara_list = [chara0, chara1, chara2, chara3, chara4, chara5]
    # 所持アイテムが50以下だったら
    if Game.gacha == False:
        Game.surface.fill((248,0,0))
        pygame.draw.rect(Game.surface, (255,255,255), (30,30,1140,644))
        Game.surface.blit(gacha_error_msg, [20,300]) 
        flash_masage(map_return_msg_list, [400,500])
    # 所持アイテムが50以上だったらガチャを回す
    if Game.gacha:
        Game.gacha = False
        Game.surface.blit(gacha_ok_msg, [76,100]) 
        flash_masage(enter_msg_list, [500,620])
        if Game.on_okkey():
            animation_flag = True    
        # ガチャアニメーション        
        if animation_flag:
            stop1 = Game.count % 15
            stop2 += 1
            if stop1 >= len(g_list):
                stop1 = 0
            Game.surface.blit(g_list[stop1], (0,0))
            Game.surface.blit(gacha_msg, (400, 60))
            if stop2 >= 60:
                # ガチャ回す
                obtain_cara = random.choices(chara_list , weights=prob, k=PIC)
                Game.pic_chara = obtain_cara[0]
                Game.chara_no = chara_list.index(Game.pic_chara) 
                animation_flag = False
                print_flag = True
                stop2 = 0
                Game.se_flag = 5
        if print_flag:
            if Game.se_flag == 5:
                gacha_se.play(0)
                Game.se_flag = 0
            Game.surface.blit(gacha_bg, (0,0))
            Game.surface.blit(gacha_pic_msg, [450,620])
            Game.surface.blit(re_map_msg, [1000,620])
            Game.surface.blit(Game.pic_chara, (pos))      # 結果表示
            Game.blit_item -= 50
            stop1 += 1
            if Game.blit_item >= 50:
                if stop1 >= 60:
                    Game.surface.blit(re_gacha_msg, [15,500])
                    if stop1 >= 90:
                        Game.item = Game.blit_item
                        if Game.on_okkey():
                            stop1 = 0
                            Game.print_flag = False 
                            Game.gacha = True
                            animation_flag = True
                            
            if Game.blit_item < 50:
                if Game.on_okkey():
                    Game.gacha = False
                    Game.print_flag = False 
                    Game.item = Game.blit_item

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
boss_bgm.set_volume(0.1)
clear_bgm = pygame.mixer.Sound("music/game_clear_bgm.wav") 
clear_bgm.set_volume(0.2)
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
clear_after_msg1 = msg_font.render("クリア記念！キャラクターの一覧を見ますか？", True, (0,0,0))
clear_after_msg2 = msg_font.render("ゲームをやめるときはESCキーで終了します", True, (0,0,0))

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

        if Game.count % 5 == 0:
            Game.player_count += 1
        if Game.count % 9 == 0:
            Game.enemy_count += 1
        if Game.count % 9 == 0:
            Game.boss_count += 1
        
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
            if Game.on_skey(): 
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
            Game.surface.fill((226,243,255))
            # 背景
            Game.surface.blit(map1_bg, (0, 0))
            # マップ表示
            Game.field.run()
            Game.field.game_over_judge()
            # フレーム
            Game.surface.blit(frame_img, (0, 0))
            # 操作方法表示
            Game.surface.blit(key_menu_img,(950,45))
            # アイテムカウンタ
            Game.surface.blit(item_msg,(50,60))
            Game.surface.blit(msg_font.render(": "+str(Game.item), True, (0, 0, 0)), (180, 50))
            # HP
            Game.surface.blit(msg_font.render("HP : "+str(Game.hp), True, (0, 0, 0)), (60, 100))
            # HP回復
            if Game.on_ckey():
                Game.recovery_flag = True
                Game.se_flag = 6
            if Game.recovery_flag:
                if Game.item >= 30:
                    if Game.se_flag == 6:
                        se1.play(0)
                        Game.se_flag = 0
                    Game.item -= 30
                    Game.hp += 10
                    Game.recovery_flag = False
                elif Game.item < 30:
                    Game.recovery_flag = False
                
            # 効果音
            if Game.se_flag == 1:
                se1.play(0)
                Game.se_flag = 0
            if Game.se_flag == 3:
                se3.play(0)
                Game.se_flag = 0
            if Game.se_flag == 5:
                se3.play(0)
                Game.se_flag = 0
            
            # ガチャ画面へ
            if Game.on_gkey():
                if music_flag == 0:
                    map_bgm.stop()
                    music_flag = 4
                Game.phase = Phase.GACHAGACHA
            # ボスマップへ
            if Game.boss_map:
                Game.phase = Phase.BOSS
                if music_flag == 0:
                    map_bgm.stop()
                    music_flag = 3

            # HPが０になったらゲームオーバー
            if Game.is_gameover:
                Game.phase = Phase.GAME_OVER
                if music_flag == 0:
                    map_bgm.stop()
                    Game.se_flag = 9
                    music_flag = 9
                    
                
        # ガチャ画面
        elif Game.phase == Phase.GACHAGACHA:
            if music_flag == 4:
                gacha_bgm.play(-1)
                music_flag = 0
            Game.surface.blit(gacha_bg,(0,0))
            if Game.item >= 50:
                Game.gacha = True
            neko_gacha()
            # アイテムカウンタ
            Game.surface.blit(item_msg,(50,60))
            Game.surface.blit(frame_img,(0,0))
            Game.surface.blit(msg_font.render(": "+str(Game.blit_item), True, (255, 0, 0)), (180, 50))

            # 戻るボタンを押したら、マップ画面へ戻る
            if Game.on_returnkey():
                Game.print_flag = False
                if music_flag == 0:
                    gacha_bgm.stop()
                    # 元々いたマップに戻る
                    if Game.boss_map:
                        music_flag = 3
                        Game.phase = Phase.BOSS
                    else:
                        music_flag = 2
                        Game.phase = Phase.MAP
                    
        # ボスマップ画面
        if Game.phase == Phase.BOSS:
            if music_flag == 3:
                boss_bgm.play(-1)
                music_flag = 0
            # if Game.hp <= 0:
            #     Game.is_gameover = Ture
            Game.surface.fill((191,104,98))
            Game.surface.blit(map1_bg, (0, 0))
            Game.field.run()
            Game.field.game_over_judge()
            # フレーム
            Game.surface.blit(frame_img, (0, 0))
            # 操作方法表示
            Game.surface.blit(key_menu_img,(950,45))
            # アイテムカウンタ
            Game.surface.blit(item_msg,(50,60))
            Game.surface.blit(msg_font.render(": "+str(Game.item), True, (0, 0, 0)), (180, 50))
            # HP
            Game.surface.blit(msg_font.render("HP : "+str(Game.hp), True, (0, 0, 0)), (60, 100))
            # HP回復
            if Game.on_ckey():
                Game.recovery_flag = True
                Game.se_flag = 6
            if Game.recovery_flag:
                if Game.item >= 30:
                    if Game.se_flag == 6:
                        se1.play(0)
                        Game.se_flag = 0
                    Game.item -= 30
                    Game.hp += 10
                elif Game.item < 30:
                    pass

            # 効果音
            if Game.se_flag == 1:
                se1.play(0)
                Game.se_flag = 0
            if Game.se_flag == 3:
                se3.play(0)
                Game.se_flag = 0
            if Game.se_flag == 5:
                se3.play(0)
                Game.se_flag = 0
    
            
            if Game.on_gkey():
                if music_flag == 0:
                    boss_bgm.stop()
                    music_flag = 4
                Game.phase = Phase.GACHAGACHA
            if Game.is_gameover:
                if music_flag ==0:
                    boss_bgm.stop()
                    music_flag = 9
                    Game.se_flag = 9
                Game.phase = Phase.GAME_OVER
            
            if Game.is_clear:
                if music_flag == 0:
                    boss_bgm.stop()
                    music_flag =8
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
            Game.surface.blit(clear_after_msg2, [135,650])

        # ゲームクリア
        elif Game.phase == Phase.GAME_CLEAR:
            Game.time_count += 1
            if music_flag == 8:
                clear_bgm.play(0)
                music_flag = 0
            Game.surface.blit(gameclear_bg, (0,0))
            if Game.time_count >= 50:
                Game.surface.blit(clear_after_msg1, (80,300))
                Game.surface.blit(clear_after_msg2, (80,400))
                if Game.time_count >= 65:
                    flash_masage(enter_msg_list, [350,650])
                    if Game.on_okkey():
                        Game.surface.blit(chara_table_img, (0,0))
                        flash_masage(clear_msg_list,[400,600])
                        if Game.on_okkey():
                            if music_flag == 0:
                                pass
                            Game.is_gameclear = False
                            main()
  
        pygame.display.update()
        clock.tick(30)

if __name__ == '__main__':
    main()
        