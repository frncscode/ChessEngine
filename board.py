import pygame
import utils
import piece 
from piece import Queen
import time

'''
Board Class:
The meat of the chess engine
The board class runs the whole game of chess
'''
class Board:
    piece_values = {
        'p': 100,
        'r': 300,
        'n': 300,
        'b': 300,
        'q': 900,
        'k': 0 
            }

    side_conversion = {-1: "WHITE", 1: "BLACK"}

    # constructor
    def __init__(self, FEN = 'rnbkqbnr/pppppppp/00000000/00000000/00000000/00000000/PPPPPPPP/RNBQKBNR'): # default FEN string
        ''' Args: setup is a 2d array of pieces
        for the board to begin as. Default chess
        setup if no argument is passed'''
        self.board = self.createBoard(FEN)
        print(self.board)
        self.moves = []
        self.white_check = False
        self.black_check = False
        self.turn = -1 # white
        self.winner = None

    # evaluation function of a certain side
    def eval(self, side):
        score = 0

        # evaluating presence of pieces
        pieces = self.getPieces(side)
        for piece in pieces:
            score += Board.piece_values[piece.value.lower()] 
        
        # evaluating check positions
        if side == -1:
            if self.white_check:
                score -= 500
        elif side == 1:
            if self.black_check:
                score -= 500

        return score

    # function to return all possible moves excluding check rules
    # check rules are checked in the getValidMoves func
    def getPossibleMoves(self, side = None):
        '''ARGS:
        side -> -1 or 1 > choosing what side to consider
        '''
        if not side:
            side = self.turn
        moves = []
        for piece in self.getPieces(side): 
            # move is the piece 
            # and [1] is the board index of the move
            for move in piece.gen_moves(self.board):
                moves.append((piece, move))
        return moves
    
    # function that returns all valid moves considering check 
    # meta calls getPossibleMoves
    def getValidMoves(self, side = None):
        '''ARGS:
        side -> -1 or 1 > chooses what side to consider
        '''
        if not side:
            side = self.turn

        # generate all possible moves
        moves = self.getPossibleMoves()
        # for each move check if it is valid
        for idx, move in sorted(enumerate(moves), reverse=True):
            # simulate move
            piece = move[0]
            target = move[1]
            b = self.copy()
            b[target[0]][target[1]] = piece
            b[piece.pos[0]][piece.pos[1]] = 0
            temp_pos = piece.pos
            piece.pos = target
            # if move puts the player into check
            if self.inCheck(piece.side, b):
                # then the move is invalid
                moves.pop(idx) # remove the move if invalid
            # resetting the pieces temporary position
            piece.pos = temp_pos
        return moves

    # function that simply returns all pieces of a certain side
    def getPieces(self, side, board = None):
        '''ARGS:
        side -> which side of pieces to get
        board -> optional board to refer to instead of default
        '''
        pieces = []
        if not board:
            board = self.board
        for row in board:
            for piece in row:
                if piece: # not empty
                    if piece.side == side:
                        pieces.append(piece)
        return pieces
    
    # function to check if a certain piece is under attack
    def underAttack(self, piece):
        '''ARGS:
        piece -> piece object to check
        '''
        enemy_moves = self.getPossibleMoves(piece.side * -1)
        for move in enemy_moves:
            if move[1] == piece.pos:
                return True
        return False

    # function to check if certain player is in check
    def inCheck(self, side = None, board = None):
        '''
        ARGS:
        side -> optional side to consider
        board -> optional board to refer to instead of default
        '''
        if not board:
            board = self.board
        # getting the king
        for row in board:
            for p in row:
                if p: # not empty
                    if p.side == side and isinstance(p, piece.King):
                        King = p
        # checking for check
        for p in self.getPieces(side * -1, board):
            if King.pos in p.gen_moves(board):
                return True
        return False
        
    # function to check if a player is in checkmate
    def checkmate(self, side, board=None):
        '''ARGS:
        side -> which side to check for checkmate
        board -> optional board to refer to instead of the default one
        '''
        if not board:
            board = self.board
        for piece in self.getPieces(side, board):
            for move in piece.gen_moves(board):
                # simulate move
                sim_board = self.copy()
                sim_board[move[0]][move[1]] = piece
                sim_board[piece.pos[0]][piece.pos[1]] = 0
                temp_pos = piece.pos
                piece.pos = move
                # check for check
                if not self.inCheck(side, sim_board):
                    piece.pos = temp_pos
                    return False
                piece.pos = temp_pos
        return True
    
    # update that runs after each and every move
    def update(self):
        # evaluating
        black_score = self.eval(1)
        white_score = self.eval(-1)
        print('Eval Results: White:' + str(white_score) + ' Black:' + str(black_score))

        self.black_check = self.inCheck(1)
        self.white_check = self.inCheck(-1)
        start = time.perf_counter()
        if self.checkmate(1):
            # white wins
            self.winner = -1
        elif self.checkmate(-1):
            # black wins
            self.winner = 1

    def move(self, pieceToMove, pos):
        '''ARGS: piece -> piece object to move
        pos -> board index to move to'''
       
        if not ((pieceToMove, pos) in self.getValidMoves()):
            return False

        ## physically moving the piece
        # moving the piece to new position
        self.board[pos[0]][pos[1]] = pieceToMove
        # making pieces previous position empty
        self.board[pieceToMove.pos[0]][pieceToMove.pos[1]] = 0
        # updating the pieces position
        pieceToMove.pos = pos
        
        # checking for promotion
        if pieceToMove.value.lower() == 'p':
            pieceToMove.moved = True
            if pieceToMove.moved and pieceToMove.pos[0] == 7 or pieceToMove.pos[0] == 0:
                # promote the pawn
                self.board[pieceToMove.pos[0]][pieceToMove.pos[1]] = Queen(pieceToMove.pos, 'q')

       
        self.moves.append((pieceToMove, pos))

        # updating
        self.update()

        # swapping the turn
        self.turn *= -1

        # successful
        return True

    def undoMove(self):
        moveToUndo = self.moves.pop[-1]
        pass

    def copy(self):
        board = []
        for row in self.board:
            row_ = []
            for piece in row:
                row_.append(piece)
            board.append(row_)
        return board

    def print(self):
        for row in self.board:
            for col in row:
                if not(col):
                    print("00", end = '')
                else:
                    print(col.value, end='')
            print("")

    def createBoard(self, FEN):
        board = []
        for row_idx, row_ in enumerate(FEN.split("/")):
            row = []
            for col_idx, col in enumerate(row_):
                if col.lower() == "p": # pawn
                    row.append(piece.Pawn((row_idx, col_idx), col))
                elif col.lower() == "r": # rook
                    row.append(piece.Rook((row_idx, col_idx), col))
                elif col.lower() == "n": # knight 
                    row.append(piece.Knight((row_idx, col_idx), col))
                elif col.lower() == "b": # bishop
                    row.append(piece.Bishop((row_idx, col_idx), col))
                elif col.lower() == "q": # queen
                    row.append(piece.Queen((row_idx, col_idx), col))
                elif col.lower() == "k": # king
                    row.append(piece.King((row_idx, col_idx), col))
                elif col == "0":
                    row.append(0)
            board.append(row)

        return board
