import pygame
import sys
import visualize
import board as bd
import random

# dictionaries to convert indexes into chess notation
# e.g. 0 on x = a
# e.g. 2 on y = 6
abc = 'abcdefghi'
index_notation_x = {i: abc[i] for i in range(8)}
index_notation_y = {i: '87654321'[i] for i in range(8)}

# pygame setup
pygame.init()
win = pygame.display.set_mode((600, 600))
caption = "Chess Test - Francis Lee | "
pygame.display.set_caption(caption)

# chess engine setup
board = bd.Board()
print(board.board)
visualizer = visualize.Visualizer(600)

def randomMove():
    moves = board.getValidMoves() 
    return random.choice(moves)
    
playing = True
interval = 1
ticks = 10
moves = 0

def restart():
    global playing
    global board
    global ticks
    global moves
    playing = True
    ticks = 0 
    moves = 0
    board = bd.Board()

clock = pygame.time.Clock()
while True:
    # checking for wins
    if board.winner and playing:
        print('[#]', bd.Board.side_conversion[board.winner], 'WON')
        playing = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == 32 and not playing: # space
                # restart game
                restart()
            if False and event.key == 32 and playing:
                ticks += 1

    # QOL
    # moves time out
    if moves >= 500 and playing:
        playing = False
        print('[!] Moves Timeout! No Winner')

    # auto moving
    if playing:
        if ticks >= interval:
            moved = False
            while not moved:
                piece, move = randomMove()
                piece_pos = piece.pos
                move_pos = move
                moved = board.move(piece, move)
            print('[+] ' + bd.Board.side_conversion[board.turn * -1] + ': ' + 
                    '['+index_notation_x[piece_pos[1]]+index_notation_y[piece_pos[0]] + ']' +
                    ' -> ' +
                    '['+index_notation_x[move_pos[1]]+index_notation_y[move_pos[0]] + ']')
            moves += 1

            ticks = 0

    # rendering
    win.fill((255, 255, 255))
    win.blit(visualizer.board_to_surface(board.board), (0, 0))

    if playing:
        pygame.display.set_caption(caption + 'Moves: ' + str(moves))
    
    ticks += 1
    pygame.display.update()
    #clock.tick(60)
