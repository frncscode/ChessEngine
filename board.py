import pygame
import piece

class Board:
    
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

    def __init__(self, setup = Board.default_board):
        ''' Args: setup is a 2d array of pieces
        for the board to begin as. Default chess
        setup if no argument is passed'''
        self.board = self.str_to_classed(setup)

    def classed_to_str(self, classed_board):
        board = []
        for row in classed_board:
            row = []
            for col in row:
                row.append(col.value)
            board.append(row)
        return board

    def print(self):
        for row in self.value:
            print(' '.join(row))

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
                    pos = (col_idx, row_idx)
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

