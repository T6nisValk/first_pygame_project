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

# Player settings
PLAYER_WIDTH = 20

# Info bar settings
INFO_WIDTH = 50

# Initialize Pygame font
pygame.font.init()


class SnakeGame:
    def __init__(self):
        # Initialize Pygame
        pygame.display.set_caption("Snake")
        self.window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)

        # Snake and game settings
        self.snake_segments = [pygame.Rect(10, 10, PLAYER_WIDTH, PLAYER_WIDTH)]
        self.player_speed = 2
        self.dir_x, self.dir_y = self.player_speed, 0
        self.new = pygame.Rect(
            random.randint(0, WIN_WIDTH - PLAYER_WIDTH),
            random.randint(0, WIN_HEIGHT - PLAYER_WIDTH - INFO_WIDTH),
            PLAYER_WIDTH,
            PLAYER_WIDTH,
        )
        self.score = 0
        self.info_rect = pygame.Rect(0, WIN_HEIGHT - INFO_WIDTH, WIN_WIDTH, INFO_WIDTH)
        self.run = True

    def draw_window(self):
        """Draw the snake, the new rectangle, and the score info."""
        self.window.fill(BLACK)

        # Draw snake segments
        for segment in self.snake_segments:
            pygame.draw.rect(self.window, RED, segment, border_radius=10)

        # Draw target rectangle
        pygame.draw.rect(self.window, RED, self.new, border_radius=10)

        # Draw the bottom info bar
        pygame.draw.rect(self.window, BROWN, self.info_rect)

        # Render and draw score
        score_info = self.font.render(f"Score: {self.score}", True, WHITE)
        self.window.blit(score_info, (20, WIN_HEIGHT - 35))

        pygame.display.update()

    def respawn_new(self):
        """Respawn the target rectangle at a random position."""
        self.new.x = random.randint(0, WIN_WIDTH - PLAYER_WIDTH)
        self.new.y = random.randint(0, WIN_HEIGHT - PLAYER_WIDTH - INFO_WIDTH)

    def boundary(self):
        """Check if the snake hits the boundary."""
        head = self.snake_segments[0]
        if head.x < -PLAYER_WIDTH:
            head.x = WIN_WIDTH
        elif head.x > WIN_WIDTH:
            head.x = -PLAYER_WIDTH
        elif head.y < -PLAYER_WIDTH:
            head.y = WIN_HEIGHT - INFO_WIDTH
        elif head.y > WIN_HEIGHT - INFO_WIDTH:
            head.y = -PLAYER_WIDTH

    def move_player(self, key):
        """Handle player direction based on key press."""
        if key == pygame.K_a and self.dir_x == 0:
            self.dir_x, self.dir_y = -self.player_speed, 0
        elif key == pygame.K_d and self.dir_x == 0:
            self.dir_x, self.dir_y = self.player_speed, 0
        elif key == pygame.K_w and self.dir_y == 0:
            self.dir_x, self.dir_y = 0, -self.player_speed
        elif key == pygame.K_s and self.dir_y == 0:
            self.dir_x, self.dir_y = 0, self.player_speed

    def add_segment(self):
        """Add a new segment to the snake."""
        last_segment = self.snake_segments[-1]
        new_segment = pygame.Rect(last_segment.x, last_segment.y, PLAYER_WIDTH, PLAYER_WIDTH)
        self.snake_segments.append(new_segment)

    def move_snake(self):
        """Move the snake segments."""
        for i in range(len(self.snake_segments) - 1, 0, -1):
            self.snake_segments[i].x = self.snake_segments[i - 1].x
            self.snake_segments[i].y = self.snake_segments[i - 1].y

        # Move the head in the current direction
        self.snake_segments[0].x += self.dir_x
        self.snake_segments[0].y += self.dir_y

    def handle_collision(self):
        """Check for collision with the target."""
        if self.snake_segments[0].colliderect(self.new):
            self.respawn_new()
            self.add_segment()
            self.player_speed += 0.1
            self.score += 1

    def handle_events(self):
        """Handle user input and events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
            if event.type == pygame.KEYDOWN:
                self.move_player(event.key)

    def run_game(self):
        """Main game loop."""
        while self.run:
            self.clock.tick(FPS)
            self.handle_events()
            self.move_snake()
            self.boundary()
            self.handle_collision()
            self.draw_window()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = SnakeGame()
    game.run_game()
