import pygame
import time
import board
import piece
import visualize
import sys

pygame.init()
win = pygame.display.set_mode((800,800))
clock = pygame.time.Clock()

board = board.Board() # default board
visualizer = visualize.Visualizer(800) # board size
selected = False
while True:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # LMB: selecting pieces
                selected_index = (mouse_pos[1] // visualizer.tile_size, mouse_pos[0] // visualizer.tile_size)
                if selected == False:
                    selected = board.board[selected_index[0]][selected_index[1]]
                elif selected != False: 
                    if selected_index != [selected.pos[0], selected.pos[1]]: # not the same tile as before
                        moves = selected.gen_moves(board.board)
                        board.print()
                        if selected_index in moves:
                            # moving the piece
                            # move the piece to new position
                            board.board[selected_index[0]][selected_index[1]] = selected
                            # make previous piece position cleared
                            board.board[selected.pos[0]][selected.pos[1]] = 0
                            # update the piece's objects position
                            selected.pos = [selected_index[0], selected_index[1]]

                            if isinstance(selected, piece.Pawn):
                                selected.moved = True

                            # deselect
                            selected = False
                        else:
                            selected = False
                    else:
                        selected = False
            elif event.button == 3:
                print('Deselecting')
                selected = False

    win.fill((255, 255, 255))
    bg = visualizer.board_to_surface(board.board)
    win.blit(bg, (0, 0))
    
    if selected:
        # draw circles over possible moves
        for move in selected.gen_moves(board.board):
            if board.board[move[0]][move[1]]:
                # the move is a take
                colour = (250, 0, 0, 255)
            else:
                colour = (80, 80, 80, 70)
            # creating a temporary surface so that the circle can be transparent
            move_screen_pos = (move[1] * visualizer.tile_size, move[0] * visualizer.tile_size)
            circle_surface = pygame.Surface((visualizer.tile_size, visualizer.tile_size), pygame.SRCALPHA)
            pygame.draw.circle(circle_surface, colour,
                    (visualizer.tile_size // 2, 
                    visualizer.tile_size // 2), 15)
            win.blit(circle_surface, move_screen_pos)

        # draw square around selected tile
        pygame.draw.rect(win, (0, 210, 15), (selected.pos[1] * visualizer.tile_size, selected.pos[0] * visualizer.tile_size, visualizer.tile_size, visualizer.tile_size), 3)

    clock.tick(60)
    pygame.display.update()
