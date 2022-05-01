import pygame

def onBoard(pos):
    '''
    Args: pos -> oposite to index on board (simulating x and y values)
    '''
    return 0 <= pos[1] <= 8 - 1 and 0 <= pos[0] <= 8 - 1

class Piece:
    
    def __init__(self, pos, value):
        self.pos = pos
        self.value = value
        self.side = -1 if value[0] == "w" else 1

class Pawn(Piece):

    def __init__(self, pos, value):
        super().__init__(pos, value)
        self.moved = False

    def gen_moves(self, board):
        moves = []
        move = (self.pos[1] + (1 * self.side), self.pos[0]) # up one
        if not board[move[0]][move[1]] and onBoard(move):
            moves.append(move)
            move = (move[0] + (1 * self.side), move[1]) # up two
            # double jump rule
            if not self.moved:
                if not board[move[0]][move[1]] and onBoard(move):
                    moves.append(move)
        return moves


class Rook(Piece):

    def __init__(self, pos, value):
        super().__init__(pos, value)
    
    def gen_moves(self, board):
        pass

class Knight(Piece):

    def __init__(self, pos, value):
        super().__init__( pos, value)

    def gen_moves(self, board):
        pass

class Bishop(Piece):

    def __init__(self, pos, value):
        super().__init__(pos, value)
    
    def gen_moves(self, board):
        pass

class Queen(Piece):

    def __init__(self, pos, value):
        super().__init__(pos, value)

    def gen_moves(self, board):
        pass

class King(Piece):

    def __init__(self, pos, value):
        super().__init__(pos, value)

    def gen_moves(self, board):
        pass
