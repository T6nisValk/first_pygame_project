import pygame
import sys
import random

# Initialize Pygame
pygame.init()


class PlatFormer:
    def __init__(self):
        # Window and Game Settings
        self.WINDOW_DIM = (800, 600)
        self.WINDOW = pygame.display.set_mode(self.WINDOW_DIM)
        pygame.display.set_caption("Basic Jumping")
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 255, 0)
        self.DARK_BROWN = (77, 43, 22)
        self.CLOCK = pygame.time.Clock()
        self.FPS = 60
        self.bg = pygame.image.load("assets/images/background.jpg")
        self.bg = pygame.transform.scale(self.bg, (800, 600))
        self.tiles = 3  # Number of tiles to draw
        self.scroll = 0

        # Platforms
        self.platform = pygame.image.load("assets/images/platform.jpg")
        self.platform_width = self.platform.get_width()
        self.platform_height = self.platform.get_height()

        self.ground_height = 52

        # Square (Player) Settings
        self.square_size = 30
        self.square = pygame.Rect(
            self.WINDOW_DIM[0] / 2 - self.square_size,
            self.WINDOW_DIM[1] - self.ground_height - self.square_size,
            self.square_size,
            self.square_size,
        )
        self.move_speed = 10

        # Jump/Gravity Settings
        self.gravity = 2  # Force pulling down
        self.jump_power = 30  # Force of the jump
        self.velocity_y = 0  # Vertical velocity
        self.is_jumping = False

        # Generate random positions for each tile's platform
        self.platform_positions = self.generate_platform_positions()

    def generate_platform_positions(self):
        """Generates random x and y positions for each tile's platform."""
        positions = []
        for _ in range(self.tiles):
            # Random x position within the tile (bg width)
            platform_x = random.randint(0, self.WINDOW_DIM[0] - self.platform_width)
            # Random y position but ensuring it's above the ground level
            platform_y = random.randint(
                200, self.WINDOW_DIM[1] - self.ground_height - self.platform_height
            )
            positions.append((platform_x, platform_y))
        return positions

    def main_loop(self):
        while True:
            self.handle_events()  # Handle input events
            self.move_player()  # Update player movement
            self.apply_gravity()  # Apply gravity effects
            self.draw_window()  # Redraw window and objects

            if self.scroll < -self.WINDOW_DIM[0]:
                self.scroll = 0
            if self.scroll > self.WINDOW_DIM[0]:
                self.scroll = 0

    def handle_events(self):
        # Event Handling (quit)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def move_player(self):
        keys = pygame.key.get_pressed()

        # Horizontal movement (A = left, D = right)
        if keys[pygame.K_a]:
            self.scroll += self.move_speed
        if keys[pygame.K_d]:
            self.scroll -= self.move_speed
        # Jumping logic (SPACE= jump)
        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.is_jumping = True
            self.velocity_y = -self.jump_power  # Jumping upwards

    def apply_gravity(self):
        # Gravity and ground collision detection
        if self.is_jumping:
            self.velocity_y += self.gravity  # Gravity pulling down
            self.square.y += self.velocity_y  # Apply vertical velocity

            # Ground collision
            if self.square.y >= self.WINDOW_DIM[1] - self.ground_height - self.square_size:
                self.square.y = (
                    self.WINDOW_DIM[1] - self.ground_height - self.square_size
                )  # Stay on the ground
                self.is_jumping = False  # Stop jumping
                self.velocity_y = 0  # Reset vertical velocity

    def draw_window(self):
        # Clear the screen and draw everything again
        for i in range(-1, self.tiles):
            # Blit the background
            self.WINDOW.blit(self.bg, (i * self.bg.get_width() + self.scroll, 0))

            # add platform spawn

        # Draw the square (player)
        pygame.draw.rect(self.WINDOW, self.GREEN, self.square)

        # Update display
        pygame.display.update()

        # Frame rate control
        self.CLOCK.tick(self.FPS)


if __name__ == "__main__":
    game = PlatFormer()
    game.main_loop()
