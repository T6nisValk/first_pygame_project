import pygame
import random

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Window settings
WIN_WIDTH = 800
WIN_HEIGHT = 600
FPS = 60
clock = pygame.time.Clock()
pygame.display.set_caption("Snake")
WINDOW = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

# Player settings
PLAYER_WIDTH = 20
PLAYER_SPEED = 7


def draw_window(player, new):
    """Draw the player and the new rectangle."""
    WINDOW.fill(BLACK)  # Clear the window
    pygame.draw.rect(WINDOW, RED, player, border_radius=20)  # Draw player
    pygame.draw.rect(WINDOW, RED, new, border_radius=20)  # Draw new rectangle
    pygame.display.update()  # Update the display


def move(key, player):
    """Move the player based on key presses."""
    if (
        not player.x > 0
        or not player.y > 0
        or not player.x < WIN_WIDTH - PLAYER_WIDTH
        or not player.y < WIN_HEIGHT - PLAYER_WIDTH
    ):
        pass
    else:
        player.x += PLAYER_SPEED
        if key[pygame.K_a]:
            player.x -= PLAYER_SPEED
        if key[pygame.K_d]:
            player.x += PLAYER_SPEED
        if key[pygame.K_w]:
            player.y -= PLAYER_SPEED
        if key[pygame.K_s]:
            player.y += PLAYER_SPEED

    # if (key[pygame.K_a] or key[pygame.K_LEFT]) and player.x > 0:  # Move left
    #     player.x -= PLAYER_SPEED
    # elif (
    #     key[pygame.K_d] or key[pygame.K_RIGHT]
    # ) and player.x < WIN_WIDTH - PLAYER_WIDTH:  # Move right
    #     player.x += PLAYER_SPEED
    # elif (key[pygame.K_w] or key[pygame.K_UP]) and player.y > 0:  # Move up
    #     player.y -= PLAYER_SPEED
    # elif (
    #     key[pygame.K_s] or key[pygame.K_DOWN]
    # ) and player.y < WIN_HEIGHT - PLAYER_WIDTH:  # Move down
    #     player.y += PLAYER_SPEED


def respawn_new(new):
    """Respawn the new rectangle at a random position."""
    new.x = random.randint(0, WIN_WIDTH - PLAYER_WIDTH)
    new.y = random.randint(0, WIN_HEIGHT - PLAYER_WIDTH)


def main():
    """Main game loop."""
    run = True
    player = pygame.Rect(10, 10, PLAYER_WIDTH, PLAYER_WIDTH)  # Initialize player position
    new = pygame.Rect(
        random.randint(0, WIN_WIDTH - PLAYER_WIDTH),
        random.randint(0, WIN_HEIGHT - PLAYER_WIDTH),
        PLAYER_WIDTH,
        PLAYER_WIDTH,
    )  # Initialize new rectangle position

    while run:
        clock.tick(FPS)  # Control the frame rate
        draw_window(player, new)  # Draw everything
        key = pygame.key.get_pressed()  # Get pressed keys
        move(key, player)  # Move the player

        # Check for collision with the new rectangle
        if player.colliderect(new):
            respawn_new(new)  # Respawn new rectangle at a random position

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()


if __name__ == "__main__":
    main()
