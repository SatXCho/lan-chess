import pygame
import chess

pygame.init()

# Chessboard dimensions
width = 640
height = 640

# Board tiles and highlight colors
LIGHT = (255, 207, 159)
DARK = (210, 140, 69)
HIGHLIGHT = (200, 105, 37)
CHECK = (255, 0, 0)

chessboard_surface = pygame.display.set_mode((width, height)) # makes the window with the tiles
pygame.display.set_caption("Chess Game") #ches gaem

# Loading piece images
pieces_images = {
    "P": pygame.image.load("pieces/wp.png"),
    "R": pygame.image.load("pieces/wr.png"),
    "N": pygame.image.load("pieces/wn.png"),
    "B": pygame.image.load("pieces/wb.png"),
    "Q": pygame.image.load("pieces/wq.png"),
    "K": pygame.image.load("pieces/wk.png"),
    "p": pygame.image.load("pieces/bp.png"),
    "r": pygame.image.load("pieces/br.png"),
    "n": pygame.image.load("pieces/bn.png"),
    "b": pygame.image.load("pieces/bb.png"),
    "q": pygame.image.load("pieces/bq.png"),
    "k": pygame.image.load("pieces/bk.png"),
}

# board object
board = chess.Board()

# Each square is 80x80 pixels i.e 1/8th of the board
square_size = width // 8

# Initializes the selected square to None. This variable will contain the square selected by the user
selected_square = None

# Function to convert string move (e.g., "e2e4") to a move on the board
def parse_move(move_str):
    try:
        move = chess.Move.from_uci(move_str)
        if move in board.legal_moves:
            return move
    except ValueError:
        pass
    return None

# Game loop
running = True
while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                # Mouse click location
                mouse_pos = pygame.mouse.get_pos()

                # Click location to square co-ordinates
                col = mouse_pos[0] // square_size
                row = 7 - (mouse_pos[1] // square_size)

                square = chess.square(col, row)

                if selected_square is None:
                    # If the turn is white and a white piece is clicked, select the piece
                    piece = board.piece_at(square)
                    if piece is not None and piece.color == board.turn:
                        selected_square = square
                else:
                    # Deselect if the same square is clicked again or any other piece from the same color is clicked
                    piece = board.piece_at(square)
                    if piece is not None and piece.color == board.turn:
                        selected_square = square
                    else:
                        # Try to make a legal move
                        move = chess.Move(selected_square, square)
                        if move in board.legal_moves:
                            board.push(move)
                            selected_square = None

                            # checking for checks
                            if board.is_check(): 
                                king_square = board.king(board.turn)
                                king_col = chess.square_file(king_square)
                                king_row = 7 - chess.square_rank(king_square)
                                pygame.draw.rect(chessboard_surface, CHECK, (king_col * square_size, king_row * square_size, square_size, square_size), 4)
    

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_u:
                board.pop()
                selected_square = None

    # Drawing the board
    chessboard_surface.fill(LIGHT)

    # Colors
    for row in range(8):
        for col in range(8):
            square_color = LIGHT if (row + col) % 2 == 0 else DARK
            pygame.draw.rect(chessboard_surface, square_color, (col * square_size, row * square_size, square_size, square_size))

    # Drawing pieces
    for row in range(8):
        for col in range(8):
            piece = board.piece_at(chess.square(col, 7 - row))
            if piece:
                piece_image = pieces_images[piece.symbol()]
                # Centering the piece to the square
                piece_x = col * square_size + (square_size - piece_image.get_width()) // 2
                piece_y = row * square_size + (square_size - piece_image.get_height()) // 2
                chessboard_surface.blit(piece_image, (piece_x, piece_y))

    # Highlight the selected square
    if selected_square is not None:
        selected_col = chess.square_file(selected_square)
        selected_row = 7 - chess.square_rank(selected_square)
        pygame.draw.rect(chessboard_surface, HIGHLIGHT, (selected_col * square_size, selected_row * square_size, square_size, square_size), 4)

        # Valid move highlighting, i.e. highlighting the squares where the selected piece can move
        for move in board.legal_moves:
            if move.from_square == selected_square:
                move_col = chess.square_file(move.to_square)
                move_row = 7 - chess.square_rank(move.to_square)
                move_x = move_col * square_size + square_size // 2
                move_y = move_row * square_size + square_size // 2
                pygame.draw.circle(chessboard_surface, (200, 105, 37), (move_x, move_y), square_size // 6)
        
        # checking for checks
        if board.is_check():
            king_square = board.king(board.turn)
            king_col = chess.square_file(king_square)
            king_row = 7 - chess.square_rank(king_square)
            pygame.draw.rect(chessboard_surface, CHECK, (king_col * square_size, king_row * square_size, square_size, square_size), 4)


    pygame.display.flip()
pygame.quit()
