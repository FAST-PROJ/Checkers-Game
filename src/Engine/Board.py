from copy import deepcopy

import pygame
import random
import Engine.constants as const
from Engine.Piece import Piece


class Board:
    def __init__(self, redPlayer, whitePlayer, screen):
        self.screen = screen
        self.myFont = pygame.font.SysFont('Comic Sans MS', 15)
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.possible_moves = {}
        self.redPlayer = redPlayer
        self.whitePlayer = whitePlayer

        self.create_board()

    def resetBoard(self):
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.possible_moves = {}
        self.create_board()
        return tuple(map(tuple, self.board))

    def getState(self):
        return tuple(map(tuple, self.board))

    def draw_squares(self, win):
        win.fill(const.BLACK)
        for row in range(const.ROWS):
            for col in range(row % 2, const.COLS, 2):
                pygame.draw.rect(win, const.WHITE, (
                    row * const.SQUARE_SIZE, col * const.SQUARE_SIZE, const.SQUARE_SIZE, const.SQUARE_SIZE))

    def move(self, piece, row, col):
        reward = const.MOVE_REWARD
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if (row == const.ROWS - 1 or row == 0) and not piece.king:
            piece.make_king()
            if piece.color == const.WHITE:
                self.white_kings += 1
                reward = const.KING_REWARD
            else:
                self.red_kings += 1
                reward = const.KING_REWARD

        return reward

    def simulateMove(self, board, white_kings, red_kings, piece, row, col):
        reward = const.MOVE_REWARD
        board[piece.row][piece.col], board[row][col] = board[row][col], board[piece.row][piece.col]
        piece.move(row, col)

        if (row == const.ROWS - 1 or row == 0) and not piece.king:
            piece.make_king()
            if piece.color == const.WHITE:
                white_kings += 1
                reward = const.KING_REWARD
            else:
                red_kings += 1
                reward = const.KING_REWARD

        return reward

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(const.ROWS):
            self.board.append([])
            for col in range(const.COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, const.WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, const.RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)

    def draw(self, win):
        self.draw_squares(win)
        for row in range(const.ROWS):
            for col in range(const.COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        reward = 0
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == const.RED:
                    self.red_left -= 1
                    reward += const.GET_PIECE_REWARD
                else:
                    self.white_left -= 1
                    reward += const.GET_PIECE_REWARD

        return reward

    def simulateRemove(self, board, red_left, white_left, pieces):
        reward = 0
        for piece in pieces:
            board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == const.RED:
                    red_left -= 1
                    reward += const.GET_PIECE_REWARD
                else:
                    white_left -= 1
                    reward += const.GET_PIECE_REWARD

        return reward

    def getAllPiecesWithMovements(self, color, board):
        allPieces = []
        for piece in self.getAllPieces(color, board):
            validMoves = self.get_valid_moves(piece, board)
            if len(validMoves) > 0:
                allPieces.append(piece)

        return allPieces

    def getAllPieces(self, color, board):
        pieces = []
        for row in board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def winner(self):
        if self.red_left <= 0:
            return const.WHITE
        elif self.white_left <= 0:
            return const.RED

        if not self.verifyValidMoves(self.redPlayer.color, self.board):
            return const.WHITE

        if not self.verifyValidMoves(self.whitePlayer.color, self.board):
            return const.RED

        return None


    def verifyValidMoves(self, player, board):

        for piece in self.getAllPieces(player, board):
            validMoves = self.get_valid_moves(piece, board)
            if len(validMoves) > 0:
                return True

        return False

    def simulateWinner(self, red_left, white_left, board):
        if red_left <= 0:
            return const.WHITE
        elif white_left <= 0:
            return const.RED

        if not self.verifyValidMoves(self.redPlayer.color, board):
            return const.WHITE

        if not self.verifyValidMoves(self.whitePlayer.color, board):
            return const.RED

        return None

    def get_valid_moves(self, piece, board):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == const.RED or piece.king:
            moves.update(self._traverse_left(piece.king, row - 1, max(row - 3, -1), -1, piece.color, left, board))
            moves.update(self._traverse_right(piece.king, row - 1, max(row - 3, -1), -1, piece.color, right, board))
        if piece.color == const.WHITE or piece.king:
            moves.update(self._traverse_left(piece.king, row + 1, min(row + 3, const.ROWS), 1, piece.color, left, board))
            moves.update(self._traverse_right(piece.king, row + 1, min(row + 3, const.ROWS), 1, piece.color, right, board))

        return moves

    def _traverse_left(self, king, start, stop, step, color, left, board, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, -1)
                        moves.update(self._traverse_left(king, r + step, row, step, color, left - 1, board, skipped=last))
                        moves.update(self._traverse_right(king, r + step, row, step, color, left + 1, board, skipped=last))
                    else:
                        row = min(r + 3, const.ROWS)
                        moves.update(self._traverse_left(king, r + step, row, step, color, left - 1, board, skipped=last))
                        moves.update(self._traverse_right(king, r + step, row, step, color, left + 1, board, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1

        return moves

    def _traverse_right(self, king, start, stop, step, color, right, board, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= const.COLS:
                break

            current = board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, -1)
                        moves.update(self._traverse_left(king, r + step, row, step, color, right - 1, board, skipped=last))
                        moves.update(self._traverse_right(king, r + step, row, step, color, right + 1, board, skipped=last))
                    else:
                        row = min(r + 3, const.ROWS)
                        moves.update(self._traverse_left(king, r + step, row, step, color, right - 1, board, skipped=last))
                        moves.update(self._traverse_right(king, r + step, row, step, color, right + 1, board, skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1

        return moves

    def randomMove(self, playerColor):

        piece = None
        allPieces = self.getAllPiecesWithMovements(playerColor, self.board)
        validMoves = {}
        move = None

        if(len(allPieces) > 0) :
            while len(validMoves) == 0:
                piece = random.choice(allPieces)
                validMoves = self.get_valid_moves(piece, self.board)

        if len(validMoves) > 0:
            move = random.choice(list(validMoves.keys()))

        return deepcopy(piece), move

    def bestMove(self, playerColor):
        piece = 0
        validMoves = {}
        row = col = 0
        reward = 0
        move = None
        piece = None

        allPieces = self.getAllPiecesWithMovements(playerColor, self.board)

        for pieceAux in allPieces:
            validMoves = self.get_valid_moves(pieceAux, self.board)
            if len(validMoves) > 0:
                for moveAux in validMoves:
                    rowAux, colAux = moveAux
                    rewardAux = self.simulateMoveAI((pieceAux, (rowAux, colAux)))
                    if rewardAux >= reward:
                        reward = rewardAux
                        move = moveAux
                        piece = pieceAux


        return deepcopy(piece), move

    def moveAI(self, action, ai=None):
        reward = 0
        pieceAux, move = action
        row, col = move
        piece = self.get_piece(pieceAux.row, pieceAux.col)
        # piece = Piece(pieceAux.row, pieceAux.col, pieceAux.color)
        validMoves = self.get_valid_moves(piece, self.board)

        # move piece
        reward += self.move(piece, row, col)

        # verify if it win a piece
        skipped = validMoves.get((row, col))

        if skipped:
            reward += self.remove(skipped)

        # verify if it win the game
        winner = self.winner()

        if winner == piece.color:
            reward += const.WIN_REWARD

        # see the oponent next move
        if ai is not None and winner != piece.color:
            oponentNextAction = ai.getQTableMaxValueActionTraining(self.getState(), ai.getNextPlayerTurn(), self)
            reward -= self.simulateMoveAI(oponentNextAction)

        return self.getState(), reward, winner is not None

    def simulateMoveAI(self, action):
        boardSimulated = deepcopy(self.board)
        white_kings = deepcopy(self.white_kings)
        red_kings = deepcopy(self.red_kings)
        red_left = deepcopy(self.red_left)
        white_left = deepcopy(self.white_left)
        reward = 0
        pieceAux, move = action
        row, col = move
        piece = deepcopy(pieceAux)
        validMoves = self.get_valid_moves(piece, boardSimulated)

        # move piece
        reward += self.simulateMove(boardSimulated, white_kings, red_kings, piece, row, col)

        # verify if it win a piece
        skipped = validMoves.get((row, col))

        if skipped:
            reward += self.simulateRemove(boardSimulated, red_left, white_left, skipped)

        # verify if it win the game
        winner = self.simulateWinner(red_left, white_left, boardSimulated)

        if winner == piece.color:
            reward += const.WIN_REWARD

        return reward
