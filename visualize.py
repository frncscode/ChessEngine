import pygame

pygame.init()

images = {
        "P":pygame.image.load("Assets/Pieces/w_pawn.png"),
        "R":pygame.image.load("Assets/Pieces/w_rook.png"),
        "B":pygame.image.load("Assets/Pieces/w_bishop.png"),
        "N":pygame.image.load("Assets/Pieces/w_knight.png"),
        "K":pygame.image.load("Assets/Pieces/w_king.png"),
        "Q":pygame.image.load("Assets/Pieces/w_queen.png"),

        "q":pygame.image.load("Assets/Pieces/b_queen.png"),
        "p":pygame.image.load("Assets/Pieces/b_pawn.png"),
        "r":pygame.image.load("Assets/Pieces/b_rook.png"),
        "b":pygame.image.load("Assets/Pieces/b_bishop.png"),
        "n":pygame.image.load("Assets/Pieces/b_knight.png"),
        "k":pygame.image.load("Assets/Pieces/b_king.png")
        }

class Visualizer:

    def __init__(self, size, move_prompts = True):
        self.move_prompts = move_prompts
        self.size = size
        self.tile_size = self.size // 8

    def swap_colour(self, colour):
        if colour == (119, 149, 86):
            colour = (235, 236, 208)
        else:
            colour = (119, 149, 86)
        return colour

    def board_to_surface(self, board):
        '''
        Takes a 2d array of the board and returns a surface
        to blit onto the main screen
        '''

        piece_size = self.tile_size
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
                if piece != 0:
                    # visual piece size that fits nicer
                    visual_piece_size = int(piece_size * 0.7)
                    board_surface.blit(pygame.transform.scale(
                        images[piece.value],
                        (visual_piece_size, visual_piece_size)),
                        (piece_idx * piece_size + ((piece_size - visual_piece_size) // 2),
                            row_idx * piece_size + ((piece_size - visual_piece_size) // 2)))

        return board_surface
