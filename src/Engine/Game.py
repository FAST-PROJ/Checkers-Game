import pygame
import Engine.constants as const
from Engine.Board import Board
from Engine.Player import Player
from Engine.AI import AI

class Game:
    def __init__(self, win, aiTurn):
        self.win = win

        self.screenBoard = pygame.Surface((const.WIDTH, const.HEIGHT))
        self.screenScore = pygame.Surface((const.WIDTH_SCORE, const.HEIGHT_SCORE))
        self.win.blit(self.screenScore, (0,0))
        self.win.blit(self.screenBoard, (0, const.HEIGHT))
        self.aiTurn = aiTurn
        self.ai = None
        self._init()

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)

        if self.turn == self.aiTurn:
            self.computerTurn()

        pygame.display.update()

    def computerTurn(self):
        action = self.ai.getQTableMaxValueAction(self.board.getState(), self.turn, self.board)
        self.board.moveAI(action)
        self.change_turn()
        pygame.time.delay(2000)

    def _init(self):
        self.selected = None
        self.board = Board(
            Player('RED', const.RED),
            Player('BRANCO', const.WHITE),
            self.win
        )
        self.turn = const.RED
        self.valid_moves = {}
        if self.ai is None:
            self.ai = AI()
            self.ai.training()

    def winner(self):
        return self.board.winner()

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece, self.board.board)
            return True

        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(
                self.win,
                const.BLUE,
                (col * const.SQUARE_SIZE + const.SQUARE_SIZE//2, row * const.SQUARE_SIZE + const.SQUARE_SIZE//2),
                15
            )

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == const.RED:
            self.turn = const.WHITE
        else:
            self.turn = const.RED