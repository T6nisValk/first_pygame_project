import pygame

# Initialize Pygame
pygame.init()

# Colors
RED_COLOR = (255, 0, 0)
BLACK_COLOR = (0, 0, 0)
GREEN_COLOR = (0, 255, 0)
BLUE_COLOR = (0, 0, 255)
WHITE_COLOR = (255, 255, 255)

# Set screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Init player
velocity_y = 0
GRAVITY = 0.01  # Reduced gravity for slower falling
JUMP_HEIGHT = 3  # Lower jump strength for slower jump
PLAYER_WIDTH = 20
PLAYER_HEIGHT = 20
STARTING_X_POSITION = 10
STARTING_Y_POSITION = SCREEN_HEIGHT - PLAYER_HEIGHT - 50
player = pygame.Rect(STARTING_X_POSITION, STARTING_Y_POSITION, PLAYER_WIDTH, PLAYER_HEIGHT)

# Init obstacle
OBSTACLE_SPEED = 0.05
obstacle_x = 850
OBSTACLE_Y = STARTING_Y_POSITION - 20
OBSTACLE_WIDTH = 20
OBSTACLE_HEIGHT = 40
obstacle = pygame.Rect(obstacle_x, OBSTACLE_Y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)

# Set fractional movement speed
MOVEMENT_SPEED = 0.3  # Slow movement speed

# Init World (ground)
GROUND_X_POSITION = 0
GROUND_Y_POSITION = STARTING_Y_POSITION + PLAYER_HEIGHT
GROUND_WIDTH = 800
GROUND_HEIGHT = 1
ground = pygame.Rect(GROUND_X_POSITION, GROUND_Y_POSITION, GROUND_WIDTH, GROUND_HEIGHT)

# Floating-point position for more precise movement
player_x = player.x
player_y = player.y

# Font
font = pygame.font.SysFont(None, 55)

# Event loop
is_jumping = False
run = True
game_over = False  # Flag for game over state


def display_game_over():
    game_over_text = font.render("Game Over", True, WHITE_COLOR)
    restart_text = font.render("Press 'R' to Restart or 'Q' to Quit", True, WHITE_COLOR)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 30))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 + 10))
    pygame.display.update()


while run:

    # Fill screen with black color (background)
    screen.fill(BLACK_COLOR)

    if not game_over:
        # Draw obstacle
        obstacle_x -= OBSTACLE_SPEED
        if obstacle_x < 0 - OBSTACLE_WIDTH:
            obstacle_x = SCREEN_WIDTH + 20
        obstacle.x = round(obstacle_x)
        pygame.draw.rect(screen, BLUE_COLOR, obstacle)

        # Draw ground and player
        pygame.draw.rect(screen, GREEN_COLOR, ground)  # Ground
        pygame.draw.rect(screen, RED_COLOR, player, border_radius=20)  # Player

        # Register key press
        key = pygame.key.get_pressed()

        # Move right and left using fractional speed
        if (key[pygame.K_a] or key[pygame.K_LEFT]) and player_x > 0:
            player_x -= MOVEMENT_SPEED  # Move left slower
        if (key[pygame.K_d] or key[pygame.K_RIGHT]) and player_x < (SCREEN_WIDTH - player.width):
            player_x += MOVEMENT_SPEED  # Move right slower

        # Jump logic
        if (
            key[pygame.K_SPACE] and not is_jumping
        ):  # If space is pressed and player is not already jumping
            velocity_y = -JUMP_HEIGHT  # Set upward velocity for jump
            is_jumping = True

        # Apply gravity continuously
        velocity_y += GRAVITY
        player_y += velocity_y

        # Prevent the player from falling through the ground
        if player_y >= STARTING_Y_POSITION:
            player_y = STARTING_Y_POSITION
            velocity_y = 0
            is_jumping = False  # Reset jump

        # Update player Rect position
        player.x = round(player_x)
        player.y = round(player_y)

        # Check for collision between player and obstacle (game over condition)
        if player.colliderect(obstacle):
            game_over = True  # Set game over flag

    else:
        # If the game is over, display the Game Over screen
        display_game_over()

        # Handle restart or quit
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart the game
                    # Reset player and obstacle positions to restart the game
                    player_x = STARTING_X_POSITION
                    player_y = STARTING_Y_POSITION
                    obstacle_x = SCREEN_WIDTH
                    velocity_y = 0
                    is_jumping = False
                    game_over = False  # Reset game over flag
                elif event.key == pygame.K_q:  # Quit the game
                    run = False

    # Quit game when X is pressed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Update screen
    pygame.display.update()

# Quit Pygame
pygame.quit()
