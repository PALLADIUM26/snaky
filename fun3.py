import pygame
import sys
import random

# High score file
HIGH_SCORE_FILE = ".\\highscore.txt"

def load_high_score():
    try:
        with open(HIGH_SCORE_FILE, "r") as f:
            return int(f.read())
    except:
        return 0

def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as f:
        f.write(str(score))

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Setup window and font
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Load sound (optional)
try:
    eat_sound = pygame.mixer.Sound("eat.wav")
except:
    eat_sound = None

def random_apple():
    return [random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)]

def reset_game():
    return [[5, 5]], 1, [1, 0], random_apple(), False

# Game state
snake_body, snake_length, direction, apple_pos, game_over = reset_game()
high_score = load_high_score()

# Game loop
running = True
while running:
    clock.tick(10)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if not game_over:
                if event.key == pygame.K_UP and direction != [0, 1]:
                    direction = [0, -1]
                elif event.key == pygame.K_DOWN and direction != [0, -1]:
                    direction = [0, 1]
                elif event.key == pygame.K_LEFT and direction != [1, 0]:
                    direction = [-1, 0]
                elif event.key == pygame.K_RIGHT and direction != [-1, 0]:
                    direction = [1, 0]
            else:
                if event.key == pygame.K_r:
                    # Reset game
                    snake_body, snake_length, direction, apple_pos, game_over = reset_game()

    if not game_over:
        # Move snake
        new_head = [snake_body[0][0] + direction[0], snake_body[0][1] + direction[1]]

        # Check collision
        if (
            new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or
            new_head in snake_body[1:]
        ):
            game_over = True
        else:
            snake_body.insert(0, new_head)
            if new_head == apple_pos:
                snake_length += 1
                apple_pos = random_apple()
                if eat_sound:
                    eat_sound.play()
            else:
                snake_body.pop()

    # Draw everything
    screen.fill(BLACK)

    # Draw apple
    pygame.draw.rect(screen, RED,
                     pygame.Rect(apple_pos[0] * CELL_SIZE, apple_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw snake
    for segment in snake_body:
        pygame.draw.rect(screen, GREEN,
                         pygame.Rect(segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Just before drawing score
    score = snake_length - 1
    if score > high_score:
        high_score = score
        save_high_score(high_score)

    # Draw score
    score_text = font.render(f"Score: {snake_length - 1}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Draw high score
    high_text = font.render(f"High Score: {high_score}", True, WHITE)
    screen.blit(high_text, (WIDTH - 220, 10))

    # Game over message
    if game_over:
        text = font.render("Game Over! Press R to Restart", True, WHITE)
        screen.blit(text, (WIDTH // 2 - 180, HEIGHT // 2 - 20))

    pygame.display.flip()

# Quit
pygame.quit()
sys.exit()
