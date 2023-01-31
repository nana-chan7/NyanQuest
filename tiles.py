import pygame
from game import Game

# 1タイル
class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image_list = (pygame.image.load("images/block0.png"),
                        pygame.image.load("images/block1.png"),
                        pygame.image.load("images/block2.png"),
                        pygame.image.load("images/grass_block.png"))
        
        self.image = self.image_list[Game.block_no]
        self.rect = self.image.get_rect(topleft=pos)
        
    def update(self, x_shift):
        self.rect.x += x_shift
        if x_shift >= 1100:
            x_shift = 1100
               