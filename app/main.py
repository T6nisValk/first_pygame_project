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
        self.platform_x = 0
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
            self.platform_x += self.move_speed
            self.scroll += self.move_speed
        if keys[pygame.K_d]:
            self.platform_x -= self.move_speed
            self.scroll -= self.move_speed

        # Platform collision check for movement
        platform_rect = pygame.Rect(
            240 + self.platform_x, 400, self.platform_width, self.platform_height
        )

        # Check if player is within platform bounds when moving
        if platform_rect.left <= self.square.centerx <= platform_rect.right:
            # If player is on platform and within bounds, adjust ground height
            if self.square.bottom >= platform_rect.top:
                self.ground_height = (
                    self.WINDOW_DIM[1] - platform_rect.top
                )  # Set ground height to platform
        else:
            # Reset ground height if not on the platform
            self.ground_height = 52

        # Jumping logic (SPACE= jump)
        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.is_jumping = True
            self.velocity_y = -self.jump_power  # Jumping upwards

    def apply_gravity(self):
        # Gravity and ground collision detection
        if self.is_jumping:
            self.velocity_y += self.gravity  # Gravity pulling down
            self.square.y += self.velocity_y  # Apply vertical velocity

            # Check for platform collision
            platform_rect = pygame.Rect(
                240 + self.platform_x, 400, self.platform_width, self.platform_height
            )

            # If player is above the platform and moving down
            if (
                platform_rect.colliderect(self.square)
                and self.square.bottom <= platform_rect.top + self.velocity_y
                and platform_rect.left <= self.square.centerx <= platform_rect.right
            ):
                self.square.y = platform_rect.top - self.square_size  # Land on platform
                self.is_jumping = False
                self.velocity_y = 0
                self.ground_height = self.WINDOW_DIM[1] - platform_rect.top  # Set new ground height
            else:
                # If not on the platform, reset to ground height
                if self.square.y >= self.WINDOW_DIM[1] - self.ground_height - self.square_size:
                    self.square.y = (
                        self.WINDOW_DIM[1] - self.ground_height - self.square_size
                    )  # Stay on the ground
                    self.is_jumping = False  # Stop jumping
                    self.velocity_y = 0  # Reset vertical velocity
                else:
                    self.ground_height = 52  # Reset ground height when off the platform

    def draw_window(self):
        # Clear the screen and draw everything again
        for i in range(-1, self.tiles):
            # Blit the background
            self.WINDOW.blit(self.bg, (i * self.bg.get_width() + self.scroll, 0))

            # add platform spawn
        self.WINDOW.blit(self.platform, (240 + self.platform_x, 400))

        # Draw the square (player)
        pygame.draw.rect(self.WINDOW, self.GREEN, self.square)

        # Update display
        pygame.display.update()

        # Frame rate control
        self.CLOCK.tick(self.FPS)


if __name__ == "__main__":
    game = PlatFormer()
    game.main_loop()
