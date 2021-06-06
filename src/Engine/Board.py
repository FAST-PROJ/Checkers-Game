import pygame
import Engine.constants as const
from Engine.Piece import Piece

class Board:
    def __init__(self, redPlayer, whitePlayer, screen):
        self.screen = screen
        self.myFont = pygame.font.SysFont('Comic Sans MS', 15)
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0

        self.redPlayer = redPlayer
        self.whitePlayer = whitePlayer

        self.create_board()

    def draw_squares(self, win):
        win.fill(const.BLACK)
        for row in range(const.ROWS):
            for col in range(row % 2, const.COLS, 2):
                pygame.draw.rect(win, const.WHITE, (row*const.SQUARE_SIZE, col *const.SQUARE_SIZE, const.SQUARE_SIZE, const.SQUARE_SIZE))

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == const.ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == const.WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(const.ROWS):
            self.board.append([])
            for col in range(const.COLS):
                if col % 2 == ((row +  1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, const.WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, const.RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def drawPoints(self, players):
        textPoints = ""
        heightPoints = 12

        for player in players:
            textPoints = "{player} - tem {pieces} x peças".format(player=player.name, pieces=player.pieces)
            textsurface = self.myFont.render(textPoints, True, pygame.Color("blue"))
            self.screen.blit(textsurface, (10, heightPoints))
            heightPoints = (heightPoints + 20)

    def draw(self, win):
        self.draw_squares(win)
        self.drawPoints([self.redPlayer, self.whitePlayer])
        for row in range(const.ROWS):
            for col in range(const.COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == const.RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1

    def winner(self):
        if self.red_left <= 0:
            return const.WHITE
        elif self.white_left <= 0:
            return const.RED

        return None

    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == const.RED or piece.king:
            moves.update(self._traverse_left(row -1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row -1, max(row-3, -1), -1, piece.color, right))
        if piece.color == const.WHITE or piece.king:
            moves.update(self._traverse_left(row +1, min(row+3, const.ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row +1, min(row+3, const.ROWS), 1, piece.color, right))

        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, const.ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left + 1, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1

        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= const.COLS:
                break

            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, const.ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1

        return moves