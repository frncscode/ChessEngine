import pygame

pygame.init()

images = {
        "wp":pygame.image.load("Assets/Pieces/w_pawn.png"),
        "wr":pygame.image.load("Assets/Pieces/w_rook.png"),
        "wb":pygame.image.load("Assets/Pieces/w_bishop.png"),
        "wk":pygame.image.load("Assets/Pieces/w_knight.png"),
        "wK":pygame.image.load("Assets/Pieces/w_king.png"),
        "wq":pygame.image.load("Assets/Pieces/w_queen.png"),

        "bq":pygame.image.load("Assets/Pieces/b_queen.png"),
        "bp":pygame.image.load("Assets/Pieces/b_pawn.png"),
        "br":pygame.image.load("Assets/Pieces/b_rook.png"),
        "bb":pygame.image.load("Assets/Pieces/b_bishop.png"),
        "bk":pygame.image.load("Assets/Pieces/b_knight.png"),
        "bK":pygame.image.load("Assets/Pieces/b_king.png")
        }

class Visualizer:

    def __init__(self):
        pass

    def swap_colour(self, colour):
        if colour == (255, 255, 255):
            colour = (0, 0, 0)
        else:
            colour = (255, 255, 255)
        return colour

    def board_to_surface(self, board, size):
        '''
        Takes a 2d array of the board and returns a surface
        to blit onto the main screen
        '''
        piece_size = size // 8
        size = piece_size * 8

        # creating the board surface
        board_surface = pygame.Surface((size, size))
        colour = (255, 255, 255)
        for row_idx, row in enumerate(board):
            colour = self.swap_colour(colour)
            for piece_idx, piece in enumerate(row):
                    colour = self.swap_colour(colour)
                    pygame.draw.rect(board_surface, colour, (piece_idx * piece_size,
                    row_idx * piece_size,
                    piece_size, piece_size))
        
        # putting the pieces onto the board surface
        for row_idx, row in enumerate(board):
            for piece_idx, piece in enumerate(row):
                if piece != "0":
                    board_surface.blit(pygame.transform.scale(
                        images[piece],
                        (piece_size, piece_size)),
                        (piece_idx * piece_size, row_idx * piece_size))

        return board_surface
