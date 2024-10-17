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

        # Ground Settings
        self.ground_height = 50
        self.ground = pygame.Rect(
            0, self.WINDOW_DIM[1] - self.ground_height, self.WINDOW_DIM[0], self.ground_height
        )

        # Platforms
        self.platform_height = 20
        self.platform_width = 40
        self.platform = pygame.Rect(
            random.randint(20, 780),
            random.randint(20, 500),
            self.platform_width,
            self.platform_height,
        )

        # Square (Player) Settings
        self.square_size = 30
        self.square = pygame.Rect(
            100,
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

    def main_loop(self):
        while True:
            self.handle_events()  # Handle input events
            self.move_player()  # Update player movement
            self.apply_gravity()  # Apply gravity effects
            self.draw_window()  # Redraw window and objects

    def handle_events(self):
        # Event Handling (quit)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def move_player(self):
        keys = pygame.key.get_pressed()

        # Horizontal movement (A = left, D = right)
        if keys[pygame.K_a] and self.square.x > 0 and self.square.colliderect(self.platform):
            self.square.x -= self.move_speed
        if keys[pygame.K_d] and self.square.x < self.WINDOW_DIM[0] - self.square_size:
            self.square.x += self.move_speed

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
        self.WINDOW.fill(self.BLACK)
        pygame.draw.rect(self.WINDOW, self.DARK_BROWN, self.ground)  # Draw the ground
        pygame.draw.rect(self.WINDOW, self.DARK_BROWN, self.platform)
        pygame.draw.rect(self.WINDOW, self.GREEN, self.square)  # Draw the square (player)

        # Update display
        pygame.display.update()

        # Frame rate control
        self.CLOCK.tick(self.FPS)


if __name__ == "__main__":
    game = PlatFormer()
    game.main_loop()
