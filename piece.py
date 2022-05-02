import pygame
import board as bd

def onBoard(pos):
    '''
    ARGS: pos -> a tuple of the board index of the position
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
        move = (self.pos[0] + (1 * self.side), self.pos[1]) # one up
        if onBoard(move):
            if not board[move[0]][move[1]]:
                moves.append(move)
                move = (move[0] + (1 * self.side), move[1]) # up two
                # double jump rule
                if not self.moved:
                    if onBoard(move):
                        if not board[move[0]][move[1]]:
                            moves.append(move)
        # taking
        for move in [(self.pos[0] + 1 * self.side, self.pos[1] + 1),
                (self.pos[0] + 1 * self.side, self.pos[1] - 1)]:
            if onBoard(move):
                if board[move[0]][move[1]]:
                    if board[move[0]][move[1]].side == self.side * -1:
                        moves.append(move)

        return moves


class Rook(Piece):

    def __init__(self, pos, value):
        super().__init__(pos, value)
    
    def gen_moves(self, board):
        moves = []
        # up
        interval = 1
        while onBoard((self.pos[0] + interval * self.side, self.pos[1])):
            if board[self.pos[0] + interval * self.side][self.pos[1]]:
                if  board[self.pos[0] + interval * self.side][self.pos[1]].side == self.side * -1:
                    moves.append((self.pos[0] + interval * self.side, self.pos[1]))
                break # if any piece is in the way then stop
            moves.append((self.pos[0] + interval * self.side, self.pos[1]))
            interval += 1
        # down
        interval = -1
        while onBoard((self.pos[0] + interval * self.side, self.pos[1])): 
            if board[self.pos[0] + interval * self.side][self.pos[1]]:
                if board[self.pos[0] + interval * self.side][self.pos[1]].side == self.side * -1:
                    # if the piece that is in the way is of the opposide side
                    # then we add that move before we stop
                    moves.append((self.pos[0] + interval * self.side, self.pos[1]))
                break
            moves.append((self.pos[0] + interval * self.side, self.pos[1]))
            interval -= 1

        
        # left 
        interval = 1
        while onBoard((self.pos[0], self.pos[1] + interval * self.side)):
            if board[self.pos[0]][self.pos[1] + interval * self.side]:
                if board[self.pos[0]][self.pos[1] + interval * self.side].side == self.side * -1:
                    moves.append((self.pos[0], self.pos[1] + interval * self.side))
                break
            moves.append((self.pos[0], self.pos[1] + interval * self.side))
            interval += 1

        # right
        interval = -1
        while onBoard((self.pos[0], self.pos[1] + interval * self.side)):
            if board[self.pos[0]][self.pos[1] + interval * self.side]:
                if board[self.pos[0]][self.pos[1] + interval * self.side].side == self.side * -1:
                    moves.append((self.pos[0], self.pos[1] + interval * self.side))
                break
            moves.append((self.pos[0], self.pos[1] + interval * self.side))
            interval -= 1

        return moves

class Knight(Piece):

    def __init__(self, pos, value):
        super().__init__( pos, value)

    def gen_moves(self, board):
        moves = []
        for move in [
            (self.pos[0] - 2, self.pos[1] - 1),
	    (self.pos[0] - 2, self.pos[1] + 1),
	    (self.pos[0] - 1, self.pos[1] - 2),
            (self.pos[0] + 1, self.pos[1] - 2),
    	    (self.pos[0] - 1, self.pos[1] + 2),
	    (self.pos[0] + 1, self.pos[1] + 2),
	    (self.pos[0] + 2, self.pos[1] - 1),
	    (self.pos[0] + 2, self.pos[1] + 1)
            ]:
            if onBoard(move):
                if not(board[move[0]][move[1]]) or (
                        board[move[0]][move[1]].side == self.side * -1):
                    moves.append(move)
        return moves
         

class Bishop(Piece):

    def __init__(self, pos, value):
        super().__init__(pos, value)
    
    def gen_moves(self, board):
        moves = []
        
        # down and right
        interval = [1, 1]
        while onBoard((self.pos[0] + interval[0], self.pos[1] + interval[1])):
            if board[self.pos[0] + interval[0]][self.pos[1] + interval[1]]:
                if board[self.pos[0] + interval[0]][self.pos[1] + interval[1]].side == self.side * -1:
                    moves.append((self.pos[0] + interval[0], self.pos[1] + interval[1]))
                break
            moves.append((self.pos[0] + interval[0], self.pos[1] + interval[1]))
            interval[0] += 1
            interval[1] += 1 

        # down and left
        interval = [1, -1]
        while onBoard((self.pos[0] + interval[0], self.pos[1] + interval[1])):
            if board[self.pos[0] + interval[0]][self.pos[1] + interval[1]]:
                if board[self.pos[0] + interval[0]][self.pos[1] + interval[1]].side == self.side * -1:
                    moves.append((self.pos[0] + interval[0], self.pos[1] + interval[1]))
                break
            moves.append((self.pos[0] + interval[0], self.pos[1] + interval[1]))
            interval[0] += 1
            interval[1] -= 1
        
        # up and right
        interval = [-1, 1]
        while onBoard((self.pos[0] + interval[0], self.pos[1] + interval[1])):
            if board[self.pos[0] + interval[0]][self.pos[1] + interval[1]]:
                if board[self.pos[0] + interval[0]][self.pos[1] + interval[1]].side == self.side * -1:
                    moves.append((self.pos[0] + interval[0], self.pos[1] + interval[1]))
                break
            moves.append((self.pos[0] + interval[0], self.pos[1] + interval[1]))
            interval[0] -= 1
            interval[1] += 1

        # up and left
        interval = [-1, -1]
        while onBoard((self.pos[0] + interval[0], self.pos[1] + interval[1])):
            if board[self.pos[0] + interval[0]][self.pos[1] + interval[1]]:
                if board[self.pos[0] + interval[0]][self.pos[1] + interval[1]].side == self.side * -1:
                    moves.append((self.pos[0] + interval[0], self.pos[1] + interval[1]))
                break
            moves.append((self.pos[0] + interval[0], self.pos[1] + interval[1]))
            interval[0] -= 1
            interval[1] -= 1

        return moves


class Queen(Piece):

    def __init__(self, pos, value):
        super().__init__(pos, value)

    def gen_moves(self, board):
        moves = []
        # down and right
        interval = [1, 1]
        while onBoard((self.pos[0] + interval[0], self.pos[1] + interval[1])):
            if board[self.pos[0] + interval[0]][self.pos[1] + interval[1]]:
                if board[self.pos[0] + interval[0]][self.pos[1] + interval[1]].side == self.side * -1:
                    moves.append((self.pos[0] + interval[0], self.pos[1] + interval[1]))
                break
            moves.append((self.pos[0] + interval[0], self.pos[1] + interval[1]))
            interval[0] += 1
            interval[1] += 1 

        # down and left
        interval = [1, -1]
        while onBoard((self.pos[0] + interval[0], self.pos[1] + interval[1])):
            if board[self.pos[0] + interval[0]][self.pos[1] + interval[1]]:
                if board[self.pos[0] + interval[0]][self.pos[1] + interval[1]].side == self.side * -1:
                    moves.append((self.pos[0] + interval[0], self.pos[1] + interval[1]))
                break
            moves.append((self.pos[0] + interval[0], self.pos[1] + interval[1]))
            interval[0] += 1
            interval[1] -= 1
        
        # up and right
        interval = [-1, 1]
        while onBoard((self.pos[0] + interval[0], self.pos[1] + interval[1])):
            if board[self.pos[0] + interval[0]][self.pos[1] + interval[1]]:
                if board[self.pos[0] + interval[0]][self.pos[1] + interval[1]].side == self.side * -1:
                    moves.append((self.pos[0] + interval[0], self.pos[1] + interval[1]))
                break
            moves.append((self.pos[0] + interval[0], self.pos[1] + interval[1]))
            interval[0] -= 1
            interval[1] += 1

        # up and left
        interval = [-1, -1]
        while onBoard((self.pos[0] + interval[0], self.pos[1] + interval[1])):
            if board[self.pos[0] + interval[0]][self.pos[1] + interval[1]]:
                if board[self.pos[0] + interval[0]][self.pos[1] + interval[1]].side == self.side * -1:
                    moves.append((self.pos[0] + interval[0], self.pos[1] + interval[1]))
                break
            moves.append((self.pos[0] + interval[0], self.pos[1] + interval[1]))
            interval[0] -= 1
            interval[1] -= 1
        
        # up
        interval = 1
        while onBoard((self.pos[0] + interval * self.side, self.pos[1])):
            if board[self.pos[0] + interval * self.side][self.pos[1]]:
                if  board[self.pos[0] + interval * self.side][self.pos[1]].side == self.side * -1:
                    moves.append((self.pos[0] + interval * self.side, self.pos[1]))
                break # if any piece is in the way then stop
            moves.append((self.pos[0] + interval * self.side, self.pos[1]))
            interval += 1
        # down
        interval = -1
        while onBoard((self.pos[0] + interval * self.side, self.pos[1])): 
            if board[self.pos[0] + interval * self.side][self.pos[1]]:
                if board[self.pos[0] + interval * self.side][self.pos[1]].side == self.side * -1:
                    # if the piece that is in the way is of the opposide side
                    # then we add that move before we stop
                    moves.append((self.pos[0] + interval * self.side, self.pos[1]))
                break
            moves.append((self.pos[0] + interval * self.side, self.pos[1]))
            interval -= 1

        
        # left 
        interval = 1
        while onBoard((self.pos[0], self.pos[1] + interval * self.side)):
            if board[self.pos[0]][self.pos[1] + interval * self.side]:
                if board[self.pos[0]][self.pos[1] + interval * self.side].side == self.side * -1:
                    moves.append((self.pos[0], self.pos[1] + interval * self.side))
                break
            moves.append((self.pos[0], self.pos[1] + interval * self.side))
            interval += 1

        # right
        interval = -1
        while onBoard((self.pos[0], self.pos[1] + interval * self.side)):
            if board[self.pos[0]][self.pos[1] + interval * self.side]:
                if board[self.pos[0]][self.pos[1] + interval * self.side].side == self.side * -1:
                    moves.append((self.pos[0], self.pos[1] + interval * self.side))
                break
            moves.append((self.pos[0], self.pos[1] + interval * self.side))
            interval -= 1
        
        return moves


class King(Piece):

    def __init__(self, pos, value):
        super().__init__(pos, value)

    def gen_moves(self, board):
        moves = []

        for move in [
            (self.pos[0] + 1, self.pos[1] + 0), # up
            (self.pos[0] + -1, self.pos[1] + 0), # down
            (self.pos[0] + 0, self.pos[1] + -1), # left
            (self.pos[0] + 0, self.pos[1] + 1), # right
            (self.pos[0] + 1, self.pos[1] + 1), # down and right
            (self.pos[0] + 1, self.pos[1] + -1), # down and left
            (self.pos[0] + -1, self.pos[1] + 1), # up and right
            (self.pos[0] + -1, self.pos[1] + -1) # up and left
                ]:
            if onBoard(move):
                if not board[move[0]][move[1]] or (
                    board[move[0]][move[1]].side == self.side * -1
                    ):
                    moves.append(move)
                    
        return moves
