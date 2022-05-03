import pygame
import time
import board as bd
import piece
import random
import visualize
import sys

# pygame set up
pygame.init()
win = pygame.display.set_mode((800,800))
clock = pygame.time.Clock()

def restart():
    global board
    global visualizer
    global selected
    # board set up
    board = bd.Board() # default board
    visualizer = visualize.Visualizer(800, move_prompts=False) # board size
    selected = False

restart()
while True:
    mouse_pos = pygame.mouse.get_pos()
    if board.winner:
        if board.winner > 0:
            print('BLACK WINS BY CHECKMATE')
        else:
            print('WHITE WINS BY CHECKMATE')
        restart()
        
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # selected pieces and moving them
                selected_index = (mouse_pos[1] // visualizer.tile_size, mouse_pos[0] // visualizer.tile_size)
                selected_piece = board.board[selected_index[0]][selected_index[1]]
                
                # select a piece
                if selected == False and selected_piece != 0:
                    if selected_piece.side == board.turn:
                        selected = board.board[selected_index[0]][selected_index[1]]
                
                # if a piece is already selected try move
                elif selected != False: 
                    if selected_index != [selected.pos[0], selected.pos[1]]: # not the same tile as before
                        moves = selected.gen_moves(board.board)
                        if selected_index in moves:
                            # move the piece
                            board.move(selected, selected_index)
                            # deselect
                            selected = False
                        else:
                            # deselect
                            selected = False
                    else:
                        # deselect
                        selected = False
            elif event.button == 3:
                print("Black in check:", board.inCheck(1, board.board))
                print("White in check:", board.inCheck(-1, board.board))
                selected = False
    
    # displaying the chess board 
    win.fill((255, 255, 255))
    bg = visualizer.board_to_surface(board.board)
    win.blit(bg, (0, 0))
    
    if visualizer.move_prompts:
        # visual effects
        if selected:
            # draw circles over possible moves
            for move in selected.gen_moves(board.board):
                if board.board[move[0]][move[1]]:
                    # the move is a take
                    take = True
                else:
                    take = False
                # creating a temporary surface so that the circle can be transparent
                move_screen_pos = (move[1] * visualizer.tile_size, move[0] * visualizer.tile_size)
                circle_surface = pygame.Surface((visualizer.tile_size, visualizer.tile_size), pygame.SRCALPHA)
                if not take:
                    # if the move is a take then we draw a circle around it
                    pygame.draw.circle(circle_surface, (80, 80, 80, 100),
                            (visualizer.tile_size // 2, 
                            visualizer.tile_size // 2),
                            int(visualizer.tile_size * 0.15))
                else:
                    # if move is not a take then we draw a small filled circle in it
                    pygame.draw.circle(circle_surface, (80, 80, 80, 100),
                            (visualizer.tile_size // 2,
                            visualizer.tile_size // 2),
                            int(visualizer.tile_size * 0.4),
                            width=int(visualizer.tile_size * 0.1))

                # display the details to the screen
                win.blit(circle_surface, move_screen_pos)

    if selected:
        # draw square around selected tile
        pygame.draw.rect(win, (0, 210, 15),
                (selected.pos[1] * visualizer.tile_size,
                selected.pos[0] * visualizer.tile_size,
                visualizer.tile_size, visualizer.tile_size), 3)
    
    # pygame things
    clock.tick(60)
    pygame.display.update()
