import pygame

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

    def __init__(self, setup = None):
        ''' Args: setup is a 2d array of pieces
        for the board to begin as. Default chess
        setup if no argument is passed'''
        self.value = setup if  setup else Board.default_board

    def print(self):
        for row in self.value:
            print(' '.join(row))
