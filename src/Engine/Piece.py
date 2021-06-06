import pygame
import Engine.constants as const

class Piece:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = const.SQUARE_SIZE * self.col + const.SQUARE_SIZE // 2
        self.y = const.SQUARE_SIZE * self.row + const.SQUARE_SIZE // 2

    def make_king(self):
        self.king = True

    def draw(self, win):
        radius = const.SQUARE_SIZE//2 - self.PADDING
        pygame.draw.circle(win, const.GREY, (self.x, self.y), radius + self.OUTLINE)
        pygame.draw.circle(win, self.color, (self.x, self.y), radius)
        if self.king:
            win.blit(const.CROWN, (self.x - const.CROWN.get_width()//2, self.y - const.CROWN.get_height()//2))

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self):
        return str(self.color)