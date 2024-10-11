import pygame
import random

# Initialize Pygame
pygame.init()

# Set screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Create the screen object
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Set initial player speed and starting position
player_speed = 5  # The speed should be reasonable for smooth movement
player_pos = [300, 300]  # Starting position of the player (head of the snake)

# Set the initial snake body (just one segment at start)
snake_body = [pygame.Rect(player_pos[0], player_pos[1], 25, 25)]

# Define initial length of the snake
snake_length = 1

# Create the first point (food) at a random position
food = pygame.Rect(
    random.randint(0, SCREEN_WIDTH - 25), random.randint(0, SCREEN_HEIGHT - 25), 25, 25
)

# Set initial direction (moving right by default)
direction = pygame.Vector2(1, 0)  # This is a 2D vector for movement direction

# Run the game loop
run = True
clock = pygame.time.Clock()

while run:
    # Fill the screen with black (clear screen)
    screen.fill((0, 0, 0))

    # Get the state of all keyboard buttons
    key = pygame.key.get_pressed()
    key_toggle = pygame.key.to
    # Check for movement keys and change direction
    if key[pygame.K_a] and direction.x == 0:  # Move left
        direction = pygame.Vector2(-1, 0)
    if key[pygame.K_d] and direction.x == 0:  # Move right
        direction = pygame.Vector2(1, 0)
    if key[pygame.K_w] and direction.y == 0:  # Move up
        direction = pygame.Vector2(0, -1)
    if key[pygame.K_s] and direction.y == 0:  # Move down
        direction = pygame.Vector2(0, 1)

    # Move the snake automatically in the current direction
    player_pos[0] += direction.x * player_speed
    player_pos[1] += direction.y * player_speed

    # Insert the new head position at the beginning of the snake body
    new_head = pygame.Rect(player_pos[0], player_pos[1], 25, 25)
    snake_body.insert(0, new_head)

    # Ensure the snake doesn't grow indefinitely; trim to the correct length
    if len(snake_body) > snake_length:
        snake_body.pop()

    # Check for collision with the food
    if new_head.colliderect(food):
        snake_length += 1  # Increase the length of the snake
        food = pygame.Rect(
            random.randint(0, SCREEN_WIDTH - 25), random.randint(0, SCREEN_HEIGHT - 25), 25, 25
        )  # Respawn food

    # Draw the snake body
    for segment in snake_body:
        pygame.draw.rect(screen, (255, 0, 0), segment, border_radius=11)

    # Draw the food (point)
    pygame.draw.rect(screen, (0, 255, 0), food)

    # Handle events (like closing the window)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Update the screen display
    if not key[pygame.K_ESCAPE]:
        pygame.display.update()

    # Control the game frame rate
    clock.tick(30)  # Controls the game speed (30 FPS for smoother movement)

# Quit Pygame when the loop ends
pygame.quit()
