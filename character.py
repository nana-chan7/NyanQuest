from game import Game

# キャラクターのアニメーションクラス
class Character:
    def __init__(self, image_list):
        # 画像リスト
        # self.image_list = image_list
        self.image = None
        # self.image_list = []*2
        # 初期画像番号 0
        self.image_no = 0
        
    # アニメーション設定  
    def set_chara_animation(self, image_list):
    # def set_chara_animation(self):
        self.image_list = image_list
        if Game.test_count >= 2:
            Game.test_count = 0
        self.image_no = Game.test_count
        if Game.on_rightkey():
            self.image_no 
        elif Game.on_leftkey():
            self.image_no += 2
        elif Game.on_spacekey():
            self.image_no += 4
            
        self.image = self.image_list[self.image_no]
        return self.image
        
 



