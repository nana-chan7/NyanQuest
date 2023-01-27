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
# フォント
# font = pygame.font.Font(sys, 55)

Game.field = Filed(Filed.map1,Game.surface)

# ゲームの初期化処理
def init_game_info():
    Game.is_gameover = False
    Game.phase = Phase.TITLE

    
# 基本描画処理   
# def basic_draw(fill_no,img):
#     Game.surface.fill(fill_no)
    # if Game.phase == Phase.MAP:
    #     # if Game.on_rightkey():
    #     #     Game.forward_len += 5
    #     # elif Game.on_leftkey():
    #     #     Game.forward_len -= 5
    #     if Game.on_rightkey():
    #         if Game.player_pos >= 1050 or Game.r_flag:
    #             Game.l_flag = True
    #             Game.forward_len += 5
    #     elif Game.on_leftkey():
    #         if Game.player_pos <= 25 or Game.l_flag:
    #             Game.r_flag = True
    #             Game.forward_len -= 5
    #     if Game.move_flag:
    #         x = Game.forward_len % Game.SCREEN_WIDTH
    #         Game.surface.blit(img, (-x, 0))
    #         Game.surface.blit(img, (Game.SCREEN_WIDTH-x, 0))

# ガチャ処理
def neko_gacha():
    # メッセージ
    # gacha_error_msg = font.render("アイテムが足りません！また集めたら来てね！", True, (255,255,255))
    # 確率
    prob = [0, 0.8, 0.6, 0.5, 0.3, 0.1] 
    # ガチャ一回につき、一体排出
    PIC = 1
    obtain_cara = None
    # 所持アイテムが10以下だったらフラグをTrue
    if Game.item < 10:
        Game.gacha_error_flag = True
    # 所持アイテムが10以上だったらガチャを回す
    elif Game.item >= 10:
        Game.gacha_error_flag = False
        if Game.on_enterkey():
            # アイテムを消費
            Game.item -= 10
            obtain_cara = random.choices(Game.CHARACTER_LIST, weights=prob, k=PIC)
            Game.obtain_cara_img = pygame.image.load(obtain_cara[0])
            # 手持ちに追加
            Game.my_chara_list.append(obtain_cara[0])
            # 所持アイテムが10以下になったらフラグをTrue
            if Game.item < 10:
                Game.gacha_error_flag = True   
    # アイテムが足りなくて、回せない場合            
    if Game.gacha_error_flag:
        # Game.surface.blit(gacha_error_msg, [0,300]) 
        if Game.on_return():
            Game.phase = Phase.MAP 
    # ガチャを回した場合、結果を表示       
    else:
        Game.surface.blit(Game.obtain_cara_img,  (200,200))
        # まだアイテムが１０以上残っていたら
        if Game.item >= 10:
            if Game.on_0key():
                Game.gacha_error_flag = False
                Game.phase = Phase.GACHAGACHA
            elif Game.on_return():
                Game.phase = Phase.MAP
        # アイテム数が１０以下になったら ボタン表示も変えたい
        else:
            # Game.surface.blit(gacha_error_msg, (200,200))        
            if Game.on_return():
                Game.phase = Phase.MAP     
                  
# メイン処理
def main():
    # 画像読み込み
    title_bg = pygame.image.load("bg_images/title_img.png")
    start_bg = pygame.image.load("bg_images/start_img.png")
    gacha_bg = pygame.image.load("bg_images/gacha_img.png")
    map1_bg = pygame.image.load("bg_images/map1_img.png")
    gameover_bg = pygame.image.load("bg_images/gameover_img.png")
    
    # カウントダウン
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    font = pygame.font.SysFont('Consolas', 30)
                       
    # ゲーム情報の初期化
    init_game_info() 

    while True:
        Game.surface.fill((0,0,0))
        Game.count += 1     # ゲームカウンタ
        Game.check_event()
        Game.move_flag = False
    
        # global font
        
        # タイトル画面
        if Game.phase == Phase.TITLE:
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
            elif Game.wait_count <= 0:
                if Game.on_enterkey():
                    Game.phase = Phase.MAP 
                    Game.move_flag = True 
                  
        # マップ画面        
        elif Game.phase == Phase.MAP:
            if Game.count % 10 == 0:
                Game.player_count += 1
            if Game.count % 20 == 0:
                Game.enemy_count += 1
            Game.surface.fill((128,224,235))
            # 背景のスライド    
            x = Game.forward_len % Game.SCREEN_WIDTH
            Game.surface.blit(map1_bg, (-x, 0))
            Game.surface.blit(map1_bg, (Game.SCREEN_WIDTH-x, 0))

            Game.field.run()  
            if Game.on_gkey():
                Game.phase = Phase.GACHAGACHA
            if Game.is_gameover:
                Game.phase = Phase.GAME_OVER
                
        # ガチャ画面
        elif Game.phase == Phase.GACHAGACHA:
            Game.surface.blit(gacha_bg,(0,0))
            if Game.on_enterkey():
                Game.phase = Phase.GACHARESULT
                
        # ガチャ結果画面
        elif Game.phase == Phase.GACHARESULT:
            Game.surface.fill((200,100,100))
            neko_gacha()   
            # video()
   
        # ゲームオーバー           
        elif Game.phase == Phase.GAME_OVER:
            Game.surface.blit(gameover_bg,(0,0))
            if Game.on_enterkey():
                Game.is_gameover = False
                main()

        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    main()
         