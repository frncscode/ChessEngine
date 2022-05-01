import pygame
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
                selected_pos = (mouse_pos[1] // visualizer.tile_size, mouse_pos[0] // visualizer.tile_size)
                if selected == False:
                    selected = board.board[selected_pos[0]][selected_pos[1]]
                elif selected != False: 
                    if selected_pos != [selected.pos[1], selected.pos[0]]: # not the same tile as before
                        moves = selected.gen_moves(board.board)
                        if selected_pos in moves:
                            # moving the piece
                            # move the piece to new position
                            board.board[selected_pos[0]][selected_pos[1]] = selected
                            # make previous piece position cleared
                            board.board[selected.pos[1]][selected.pos[0]] = 0
                            # update the piece's objects position
                            selected.pos = [selected_pos[1], selected_pos[0]]

                            if isinstance(selected, piece.Pawn):
                                selected.moved = True

                            # deselect
                            selected = False

            elif event.button == 3:
                print('Deselecting')
                selected = False

    win.fill((255, 255, 255))
    bg = visualizer.board_to_surface(board.board)
    win.blit(bg, (0, 0))
    if selected:
        pygame.draw.rect(win, (0, 210, 15), (selected.pos[0] * visualizer.tile_size, selected.pos[1] * visualizer.tile_size, visualizer.tile_size, visualizer.tile_size), 3)

    clock.tick(60)
    pygame.display.update()
