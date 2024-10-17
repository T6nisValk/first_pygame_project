import pygame

# Initialize Pygame
pygame.init()

# Set up the display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Scrolling Background Example")

# Load the background image
background_image = pygame.image.load("assets/images/background.jpg")
bg_width, bg_height = background_image.get_size()

# Optionally scale the image if you want to tile or scale it
# background_image = pygame.transform.scale(background_image, (bg_width * 2, bg_height * 2))

# Player properties
player_width, player_height = 50, 50
player_color = (0, 255, 0)  # Green
player_pos = [screen_width // 2, screen_height // 2]  # Player stays centered on screen
player_speed = 5

# Player's position in the world (game world coordinates)
player_world_x = bg_width // 2
player_world_y = bg_height // 2

# Main loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle player movement in the world
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_world_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_world_x += player_speed
    if keys[pygame.K_UP]:
        player_world_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_world_y += player_speed

    # Calculate the offset for the background based on the player's world position
    # We want the player to stay centered, so the background moves inversely to the player's world position
    offset_x = player_world_x - screen_width // 2
    offset_y = player_world_y - screen_height // 2

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the background at the calculated offset (scrolling effect)
    screen.blit(background_image, (-offset_x, -offset_y))

    # Draw the player at the center of the screen (player does not move on the screen)
    player_rect = pygame.Rect(
        player_pos[0] - player_width // 2,
        player_pos[1] - player_height // 2,
        player_width,
        player_height,
    )
    pygame.draw.rect(screen, player_color, player_rect)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
