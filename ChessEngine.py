import pygame
import board
import piece
import visualize
import sys

pygame.init()
win = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()

board = board.Board() # default board
visualizer = visualize.Visualizer()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    win.fill((255, 255, 255))
    bg = visualizer.board_to_surface(board.value, 600)
    win.blit(bg, (0, 0))

    clock.tick(60)
    pygame.display.update()
