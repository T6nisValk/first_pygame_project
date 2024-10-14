import pygame
import random
import sys

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BROWN = (160, 82, 45)
WHITE = (255, 255, 255)

# Window settings
WIN_WIDTH = 800
WIN_HEIGHT = 600
FPS = 60
clock = pygame.time.Clock()
pygame.display.set_caption("Snake")
WINDOW = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

# Player settings
PLAYER_WIDTH = 20

# Bottom info bar
INFO_WIDTH = 50
INFO = pygame.Rect(0, 550, WIN_WIDTH, INFO_WIDTH)

# Info text
pygame.font.init()
font = pygame.font.SysFont(None, 36)


def draw_window(snake_segments, new, score):
    """Draw the snake and the new rectangle."""
    WINDOW.fill(BLACK)
    for segment in snake_segments:
        pygame.draw.rect(WINDOW, RED, segment, border_radius=10)
    pygame.draw.rect(WINDOW, RED, new, border_radius=10)
    pygame.draw.rect(WINDOW, BROWN, INFO)
    score_info = font.render(f"Score: {score}", True, WHITE)
    WINDOW.blit(score_info, (20, 565))
    pygame.display.update()


def respawn_new(new):
    """Respawn the new rectangle at a random position."""
    new.x = random.randint(0, WIN_WIDTH - PLAYER_WIDTH)
    new.y = random.randint(0, (WIN_HEIGHT - INFO_WIDTH) - PLAYER_WIDTH)


def boundary(player):
    """Check if player hits the wall"""
    if player.x < -PLAYER_WIDTH:
        player.x = WIN_WIDTH
    if player.x > WIN_WIDTH:
        player.x = -PLAYER_WIDTH
    if player.y < -PLAYER_WIDTH:
        player.y = WIN_HEIGHT - INFO_WIDTH
    if player.y > WIN_HEIGHT - INFO_WIDTH:
        player.y = -PLAYER_WIDTH


def move_player(key, PLAYER_SPEED, DIR_X, DIR_Y):
    """Player direction"""
    if key == pygame.K_a and DIR_X == 0:
        return -PLAYER_SPEED, 0
    if key == pygame.K_d and DIR_X == 0:
        return PLAYER_SPEED, 0
    if key == pygame.K_w and DIR_Y == 0:
        return 0, -PLAYER_SPEED
    if key == pygame.K_s and DIR_Y == 0:
        return 0, PLAYER_SPEED
    return DIR_X, DIR_Y


def add_segment(snake_segments):
    """Add a new segment to the snake."""
    last_segment = snake_segments[-1]
    new_segment = pygame.Rect(last_segment.x, last_segment.y, PLAYER_WIDTH, PLAYER_WIDTH)
    snake_segments.append(new_segment)


def move_snake(snake_segments, DIR_X, DIR_Y):
    """Move the snake segments."""
    for i in range(len(snake_segments) - 1, 0, -1):
        snake_segments[i].x = snake_segments[i - 1].x
        snake_segments[i].y = snake_segments[i - 1].y

    snake_segments[0].x += DIR_X
    snake_segments[0].y += DIR_Y


def main():
    """Main game loop."""
    run = True
    score = 0

    snake_segments = [pygame.Rect(10, 10, PLAYER_WIDTH, PLAYER_WIDTH)]
    PLAYER_SPEED = 2
    DIR_X, DIR_Y = PLAYER_SPEED, 0

    new = pygame.Rect(
        random.randint(0, WIN_WIDTH - PLAYER_WIDTH),
        random.randint(0, WIN_HEIGHT - PLAYER_WIDTH),
        PLAYER_WIDTH,
        PLAYER_WIDTH,
    )

    while run:
        clock.tick(FPS)
        draw_window(snake_segments, new, score)

        if snake_segments[0].colliderect(new):
            respawn_new(new)
            add_segment(snake_segments)
            PLAYER_SPEED += 0.1
            score += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                DIR_X, DIR_Y = move_player(event.key, PLAYER_SPEED, DIR_X, DIR_Y)

        move_snake(snake_segments, DIR_X, DIR_Y)

        boundary(snake_segments[0])

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
