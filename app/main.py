import pygame

# Colors
BROWN = (139, 69, 19)
BLACK = (0, 0, 0)
# Main window
pygame.display.set_caption("Tank")
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

# Tank properties
TANK_WIDTH, TANK_HEIGHT = 40, 40

# Player
PLAYER_TANK = pygame.image.load("assets/images/player_tank.png")
PLAYER = pygame.transform.scale(PLAYER_TANK, (TANK_WIDTH, TANK_HEIGHT))
# PLAYER = pygame.transform.rotate(PLAYER, 90)
PLAYER_SPEED = 11

# Enemy
ENEMY_TANK = pygame.image.load("assets/images/enemy_tank.png")
ENEMY = pygame.transform.scale(ENEMY_TANK, (TANK_WIDTH, TANK_HEIGHT))

# World Borders
LEFT = pygame.Rect(0, 0, 10, 600)
TOP = pygame.Rect(0, 0, 800, 10)
RIGHT = pygame.Rect(WIDTH - 10, 0, 10, 600)
BOTTOM = pygame.Rect(0, HEIGHT - 10, 800, 10)

# FPS
clock = pygame.time.Clock()
FPS = 60


# Rotation
def tank_rotate(tank, rot):
    tank = pygame.transform.rotate(tank, rot)


def draw_borders():
    pygame.draw.rect(WINDOW, BLACK, LEFT)
    pygame.draw.rect(WINDOW, BLACK, TOP)
    pygame.draw.rect(WINDOW, BLACK, RIGHT)
    pygame.draw.rect(WINDOW, BLACK, BOTTOM)


# Draw window
def draw_window(player, enemy):
    WINDOW.fill(BROWN)
    draw_borders()

    WINDOW.blit(ENEMY, (enemy.x, enemy.y))
    WINDOW.blit(PLAYER, (player.x, player.y))
    pygame.display.update()


def move_player(keys, player, enemy):
    # Move left
    if keys[pygame.K_a] and not player.colliderect(LEFT):
        player.x -= PLAYER_SPEED
        if player.colliderect(enemy):
            player.x += PLAYER_SPEED

    # Move right
    if keys[pygame.K_d] and not player.colliderect(RIGHT):
        player.x += PLAYER_SPEED
        if player.colliderect(enemy):
            player.x -= PLAYER_SPEED

    # Move up
    if keys[pygame.K_w] and not player.colliderect(TOP):
        player.y -= PLAYER_SPEED
        if player.colliderect(enemy):
            player.y += PLAYER_SPEED

    # Move down
    if keys[pygame.K_s] and not player.colliderect(BOTTOM):
        player.y += PLAYER_SPEED
        if player.colliderect(enemy):
            player.y -= PLAYER_SPEED


# Main event loop
def main():
    run = True
    enemy = pygame.Rect(100, 100, TANK_WIDTH, TANK_HEIGHT)
    player = pygame.Rect(400 - TANK_WIDTH, 600 - TANK_HEIGHT, TANK_WIDTH, TANK_HEIGHT)
    while run:

        keys = pygame.key.get_pressed()
        move_player(keys, player, enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_window(player, enemy)
        clock.tick(FPS)
    pygame.quit()


if __name__ == "__main__":
    main()
