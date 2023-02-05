from game import Game

# キャラクターのアニメーションクラス
class Character:
    def __init__(self):
        # 画像リスト
        self.image = None
        # 初期画像番号 0
        self.image_no = 0
        
    # プレイヤーキャラアニメーション設定  
    def set_chara_animation(self, image_list):
        self.image_list = image_list
        if Game.player_count >= 2:
            Game.player_count = 0
        self.image_no = Game.player_count
        if Game.on_rightkey() or Game.on_ckey():
            self.image_no 
        elif Game.on_leftkey() or Game.on_xkey():
            self.image_no += 2
        elif Game.on_spacekey():
            self.image_no += 4

        self.image = self.image_list[self.image_no]
        return self.image
    
    # エネミーキャラアニメーション設定  
    def set_enemy_animation(self, image_list):
        self.image_list = image_list
        if Game.enemy_count >= len(self.image_list):
            Game.enemy_count = 0
        self.image_no = Game.enemy_count
        self.image = self.image_list[self.image_no]
        return self.image
    
        
    
        
 



