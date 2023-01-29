import sys, pygame, cv2
import random
from pygame.locals import *
from game import Game, Phase
from filed import Filed

# 基本処理
pygame.init()
clock = pygame.time.Clock()
Game.surface = pygame.display.set_mode((Game.SCREEN_WIDTH,Game.SCREEN_HEIGHT))
pygame.display.set_caption("***NYAN QUEST***")
font = pygame.font.Font("font/Ronde-B_square.otf", 55)       # フォント 

gacha_msg = font.render("アイテムが残っていますもう一度回しますか？", True, (255,255,255))
gacha_error_msg = font.render("アイテムが足りません！また集めたら来てね！", True, (255,255,255))

Game.field = Filed(Filed.map1,Game.surface)

# ゲームの初期化処理
def init_game_info():
    Game.is_gameover = False
    Game.phase = Phase.TITLE

# ガチャ処理
def neko_gacha():
    # 確率
    prob = [0.3, 0.8, 0.6, 0.5] 
    # ガチャ一回につき、一体排出
    PIC = 1
    obtain_cara = None
    # 所持アイテムが10以下だったら
    if Game.item < 10:
        Game.gacha = False
        # Game.gacha_error_flag = True
        Game.surface.blit(gacha_error_msg, [15,300]) 
        Game.gacha_count = 0
         
    # 所持アイテムが10以上だったらガチャを回す
    elif Game.item >= 10 and Game.gacha:
        # Game.gacha_error_flag = False
        if Game.on_enterkey():
            Game.gacha_count += 1
            Game.gacha = False
            Game.item -= 10     # アイテムを消費
            obtain_cara = random.choices(Game.chara_list , weights=prob, k=PIC)
            Game.obtain_cara_img = pygame.image.load(obtain_cara[0])
            # Game.my_chara_list.append(obtain_cara[0])       # 手持ちに追加     
            Game.surface.blit(Game.obtain_cara_img, (350,200))      # 結果表示
            
            if Game.item >= 10 and Game.gacha_count >= 10000:
                Game.surface.blit(gacha_msg, [15,300]) 
                Game.gacha = True
                    

                
# 音楽再生処理 (改造)
def game_music():
    if Game.music_flag == 0:        # タイトル画面の場合
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.load("music/1.wav") 
        pygame.mixer.music.play(-1)
    elif Game.music_flag == 1:      # ゲーム(フィールド)画面の場合
        pygame.mixer.music.set_volume(0.6)
        pygame.mixer.music.load("music/2.wav") 
        pygame.mixer.music.play(-1) 
    elif Game.music_flag == 2:       # マップ画面の場合
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.load("music/3.wav") 
        pygame.mixer.music.play(-1) 
    # elif Game.music_flag == 3:      # ゲームオーバー画面の場合
    #     pygame.mixer.music.set_volume(0.5)
    #     pygame.mixer.music.load("music/gameover_sound.wav") 
    #     pygame.mixer.music.play(1)
    elif Game.music_flag == 4: # 何もしない処理
        pass
    
# メイン処理
def main():
    # 画像読み込み
    title_bg = pygame.image.load("bg_images/title_img.png")
    start_bg = pygame.image.load("bg_images/start_img.png")
    gacha_bg = pygame.image.load("bg_images/gacha_img.png")
    map1_bg = pygame.image.load("bg_images/map1_img.png")
    gameover_bg = pygame.image.load("bg_images/gameover_img.png")
    key_menu_img = pygame.image.load("bg_images/key_menu_img.png")
    
    # カウントダウン
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    font = pygame.font.SysFont('Consolas', 30)
                       
    # ゲーム情報の初期化
    init_game_info() 
    pygame.mixer.init()

    while True:
        Game.surface.fill((0,0,0))
        game_music()    # 音楽再生
        Game.count += 1     # ゲームカウンタ
        Game.check_event()
        Game.move_flag = False
    
        # global font
        
        # タイトル画面
        if Game.phase == Phase.TITLE:
            Game.music_flag = 4
            Game.surface.blit(title_bg,(0,0))
            if Game.on_enterkey():
                Game.phase = Phase.START

        # スタート画面
        elif Game.phase == Phase.START:
            Game.wait_count -= 1
            Game.surface.blit(start_bg,(0,0))
            # カウントダウン表示
            if Game.wait_count % 60 == 0:
                Game.count_down -= 1
            Game.count_text = str(Game.count_down).rjust(3) if Game.wait_count > 0 else 'ENTER!'
            Game.surface.blit(font.render(Game.count_text, True, (0, 0, 0)), (10, 650))
            pygame.display.flip()
            if Game.on_0key(): # 仮
                Game.phase = Phase.MAP 
                Game.move_flag = True 
                Game.music_flag = 1
            elif Game.wait_count <= 0:
                if Game.on_enterkey():
                    Game.phase = Phase.MAP 
                    Game.move_flag = True 
                    Game.music_flag = 1
                  
        # マップ画面        
        elif Game.phase == Phase.MAP:
            Game.music_flag = 4
            if Game.count % 10 == 0:
                Game.player_count += 1
            if Game.count % 20 == 0:
                Game.enemy_count += 1
            Game.surface.fill((128,224,235))
            # 背景のスライド    
            x = Game.forward_len % Game.SCREEN_WIDTH
            Game.surface.blit(map1_bg, (-x, 0))
            Game.surface.blit(map1_bg, (Game.SCREEN_WIDTH-x, 0))
            # マップ表示
            Game.field.run()
            # 操作方法表示
            Game.surface.blit(key_menu_img,(1000,10))
            
            if Game.on_gkey():
                Game.phase = Phase.GACHAGACHA
                Game.music_flag = 2
            elif Game.boss_flag:
                pass
            if Game.is_gameover:
                Game.phase = Phase.GAME_OVER
        # ボスマップ画面
        if Game.phase == Phase.BOSS:
            pass
                
        # ガチャ画面
        elif Game.phase == Phase.GACHAGACHA:
            Game.music_flag = 4
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
                pygame.mixer.music.stop()
                main()

        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    main()
        