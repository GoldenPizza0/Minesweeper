# import pygame

# # Initialisation
# screen = pygame.display.set_mode((1280,720))
# clock = pygame.time.Clock()
# taille_case = 70
# nb_cases = 10
# screen = pygame.display.set_mode((nb_cases * taille_case, nb_cases * taille_case))
# running = True
# pygame.init()
# pygame.font.init()

# while running:
#     screen.fill("white")  # Effacer l'écran

#     # Dessiner une grille 10x10
#     for x in range(nb_cases):
#         for y in range(nb_cases):
#             pygame.draw.rect(screen, (0, 0, 0), (x * taille_case, y * taille_case, taille_case, taille_case), 1)

#     pygame.display.flip()

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         # if event.type == pygame.MOUSEBUTTONDOWN:
#         #     if button5.collidepoint(event.pos):  # Vérifie si on clique sur le bouton
#         #         taille_case = 70
#         #         nb_cases = 5
#         #         screen = pygame.display.set_mode((nb_cases * taille_case, nb_cases * taille_case))
#         #         # Dessiner une grille 5x5
#         #         for x in range(nb_cases):
#         #             for y in range(nb_cases):
#         #                 pygame.draw.rect(screen, (0, 0, 0), (x * taille_case, y * taille_case, taille_case, taille_case), 1)

#     clock.tick(60)

# pygame.quit()

# Your pygame initialization and game code here
import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
CELL_SIZE = 30
GRID_SIZE = 10
MINES = 10
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE + 50

# Colors
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)
DARK_GRAY = (158, 158, 158)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Démineur")


class Cell:

    def __init__(self):
        self.is_mine = False
        self.revealed = False
        self.flagged = False
        self.neighbor_mines = 0


def create_board():
    board = [[Cell() for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    mines_placed = 0

    while mines_placed < MINES:
        x = random.randint(0, GRID_SIZE - 1)
        y = random.randint(0, GRID_SIZE - 1)
        if not board[y][x].is_mine:
            board[y][x].is_mine = True
            mines_placed += 1

    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            count = 0
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < GRID_SIZE and 0 <= nx < GRID_SIZE:
                        if board[ny][nx].is_mine:
                            count += 1
            board[y][x].neighbor_mines = count

    return board


def reveal_cell(board, y, x):
    if not (0 <= y < GRID_SIZE and 0 <= x < GRID_SIZE):
        return

    cell = board[y][x]
    if cell.revealed or cell.flagged:
        return

    cell.revealed = True

    if cell.neighbor_mines == 0:
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                reveal_cell(board, y + dy, x + dx)


def main():
    board = create_board()
    game_over = False
    won = False
    font = pygame.font.Font(None, 36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
                x = event.pos[0] // CELL_SIZE
                y = event.pos[1] // CELL_SIZE

                if y < GRID_SIZE:
                    if event.button == 1:  # Left click
                        if board[y][x].is_mine:
                            game_over = True
                            # Révéler toute la grille
                            for row in range(GRID_SIZE):
                                for col in range(GRID_SIZE):
                                    board[row][col].revealed = True
                        else:
                            reveal_cell(board, y, x)

                    elif event.button == 3:  # Right click
                        board[y][x].flagged = not board[y][x].flagged

        # Draw board
        screen.fill(WHITE)

        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                cell = board[y][x]
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE,
                                   CELL_SIZE)
                color = DARK_GRAY if cell.revealed else GRAY
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, BLACK, rect, 1)

                if cell.revealed:
                    if cell.is_mine:
                        pygame.draw.circle(screen, BLACK,
                                           (x * CELL_SIZE + CELL_SIZE // 2,
                                            y * CELL_SIZE + CELL_SIZE // 2),
                                           CELL_SIZE // 3)
                    elif cell.neighbor_mines > 0:
                        text = font.render(str(cell.neighbor_mines), True,
                                           BLUE)
                        screen.blit(text, (x * CELL_SIZE + CELL_SIZE // 3,
                                           y * CELL_SIZE + CELL_SIZE // 4))
                elif cell.flagged:
                    pygame.draw.polygon(screen, RED,
                                        [(x * CELL_SIZE + CELL_SIZE // 4,
                                          y * CELL_SIZE + CELL_SIZE // 4),
                                         (x * CELL_SIZE + CELL_SIZE // 4,
                                          y * CELL_SIZE + CELL_SIZE * 3 // 4),
                                         (x * CELL_SIZE + CELL_SIZE * 3 // 4,
                                          y * CELL_SIZE + CELL_SIZE // 2)])

        # Check win condition
        if not game_over:
            won = True
            for y in range(GRID_SIZE):
                for x in range(GRID_SIZE):
                    if not board[y][x].is_mine and not board[y][x].revealed:
                        won = False
                        break

        # Draw game over or win message
        if game_over:
            text = font.render("Game Over!", True, RED)
            screen.blit(text, (WIDTH // 2 - 70, HEIGHT - 40))
        elif won:
            text = font.render("You Win!", True, BLUE)
            screen.blit(text, (WIDTH // 2 - 50, HEIGHT - 40))

        pygame.display.flip()


if __name__ == "__main__":
    main()

