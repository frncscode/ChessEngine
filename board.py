import pygame
import piece

'''
def get_pieces(side, board):
    '' ARGS: side -> 1 or -1
    -1: white 1: black
    pieces = []
    for row in board:
        for piece in row:
            if piece:
                if piece.side == side:
                    pieces.append(piece)
    return pieces

def isCheck(side, board=None):
    ARGS: board -> the board object
    side -> the side of who to check is in check
   
    if not board:
       board = self.board
    opposite_side_pieces = get_pieces(side * -1, board)
    for row in board:
       for piece in row:
           if piece:
               if piece.side == side and piece.value[1] == 'K':
                   king = piece
    for piece in opposite_side_pieces:
       if king.pos in piece.gen_moves(board):
         return True
    return False
'''
class Board:
    side_conversion = {-1: "WHITE", 1: "BLACK"}

    default_board = [
        ["br","bk","bb","bq","bK","bb","bk","br"],
        ["bp" for _ in range(8)],
        ["0" for _ in range(8)],
        ["0" for _ in range(8)],
        ["0" for _ in range(8)],
        ["0" for _ in range(8)],
        ["wp" for _ in range(8)],
        ["wr","wk","wb","wq","wK","wb","wk","wr"]
        ]

    def __init__(self, setup = default_board):
        ''' Args: setup is a 2d array of pieces
        for the board to begin as. Default chess
        setup if no argument is passed'''
        self.board = self.str_to_classed(setup)
        self.white_check = False
        self.black_check = False
        self.turn = -1 # white

    def getPieces(self, side, board = None):
        pieces = []
        if not board:
            board = self.board
        for row in board:
            for piece in row:
                if piece: # not empty
                    if piece.side == side:
                        pieces.append(piece)
        return pieces

    def inCheck(self, side, board = None):
        if not board:
            board = self.board
        # getting the king
        for row in board:
            for piece in row:
                if piece: # not empty
                    if piece.side == side and piece.value[1] == 'K':
                        King = piece
        # checking for check
        for piece in self.getPieces(side * -1, board):
            if King.pos in piece.gen_moves(board):
                return True
        return False


    def move(self, piece, pos):
        '''ARGS: piece -> piece object to move
        pos -> board index to move to'''
        # moving the piece to new position
        self.board[pos[0]][pos[1]] = piece
        # making pieces previous position empty
        self.board[piece.pos[0]][piece.pos[1]] = 0
        # updating the pieces position
        piece.pos = pos
        
        # updating the moved attribute of piece if its a pawn
        if piece.value[1] == 'p': # pawn
            piece.moved = True
        
        # checking for check of the opposite team
        if self.turn == -1:
            self.black_check = self.inCheck(self.turn * -1, self.board)
        elif self.turn == 1:
            self.white_check = self.inCheck(self.turn * -1, self.board)
           
        print('Black in check:', str(self.black_check))
        print('White in check:', str(self.white_check))
        
        # swapping the turn
        self.turn *= -1

    def classed_to_str(self, classed_board):
        board = []
        for row in classed_board:
            print(row)
            row = []
            for col in row:
                print(col)
                if col == 0:
                    row.append("0")
                else:
                    row.append(col.value)
                    print(col.value)
            board.append(row)
        return board


    def print(self):
        for row in self.board:
            for col in row:
                if not(col):
                    print("00", end = '')
                else:
                    print(col.value, end='')
            print("")

    def str_to_classed(self, value):
        board = []
        for row_idx, _row in enumerate(value):
            row = []
            for col_idx, col in enumerate(_row):
                # col is the piece
                if col == "0":
                    row.append(0)
                else:
                    piece_type = col[1]
                    pos = (row_idx, col_idx)
                    if piece_type == "p": # pawn
                        row.append(piece.Pawn(pos, col))
                    elif piece_type == "r": # rook
                        row.append(piece.Rook(pos, col))
                    elif piece_type == "k": # knight
                        row.append(piece.Knight(pos, col))
                    elif piece_type == "b": # bishop
                        row.append(piece.Bishop(pos, col))
                    elif piece_type == "q": # queen
                        row.append(piece.Queen(pos, col))
                    elif piece_type == "K": # king
                        row.append(piece.King(pos, col))
            board.append(row)
        return board

