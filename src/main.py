import pygame
import Engine.constants as const
from Engine.Game import Game

FPS = 60

WIN = pygame.display.set_mode((const.WIDTH, const.HEIGHT))
pygame.display.set_caption('Damas')
pygame.font.init()

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // const.SQUARE_SIZE
    col = x // const.SQUARE_SIZE
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN, const.WHITE)

    while run:
        clock.tick(FPS)

        if game.winner() != None:
            print(game.winner())
            game.reset()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()

    pygame.quit()

main()