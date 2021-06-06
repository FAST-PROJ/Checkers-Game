class Player():
    def __init__(self, name, color):
        self.color = color
        self.name = name
        self.pieces = 12

    '''
        Create the players pieces
    '''
    def piecesLeft(self):
        return self.pieces

    def removePiece(self):
        self.pieces -= 1