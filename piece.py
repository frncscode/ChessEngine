class Piece:
    
    def __init__(self, pos, value):
        self.pos = pygame.math.Vector2(pos)
        self.value = value
        self.side = "BLACK" if value[0] == "b" else "WHITE"

class Pawn(Piece):

    def __init__(self, pos, value):
        super().__init__(self, pos, value)
        self.moved = False

    def gen_moves(self, board):
        pass

class Rook(Piece):

    def __init__(self, pos, value):
        super().__init__(self, pos, value)
    
    def gen_moves(self, board):
        pass

class Knight(Piece):

    def __init__(self, pos, value):
        super().__init__(self, pos, value)

    def gen_moves(self, board):
        pass

class Bishop(Piece):

    def __init__(self, pos, value):
        super().__init__(self, pos, value)
    
    def gen_moves(self, board):
        pass

class Queen(Piece):

    def __init__(self, pos, value):
        super().__init__(self, pos, value)

    def gen_moves(self, board):
        pass

class King(Piece):

    def __init__(self, pos, value):
        super().__init__(self, pos, value)

    def gen_moves(self, board):
        pass
