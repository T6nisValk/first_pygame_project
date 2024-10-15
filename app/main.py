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

# Load images
HEAD_WIDTH, HEAD_HEIGHT = 40, 40
BODY_WIDTH, BODY_HEIGHT = 40, 20
HEAD = pygame.image.load("assets/images/snake_head.png")
HEAD = pygame.transform.rotate(HEAD, 90)  # Starting direction
HEAD = pygame.transform.scale(HEAD, (HEAD_WIDTH, HEAD_HEIGHT))
BODY = pygame.image.load("assets/images/snake_body.png")
BODY = pygame.transform.rotate(BODY, 0)  # Starting direction
BODY = pygame.transform.scale(BODY, (BODY_WIDTH, BODY_HEIGHT))

# Load corner images
TOP_LEFT = pygame.image.load("assets/images/top_left_corner.png")
TOP_LEFT = pygame.transform.scale(TOP_LEFT, (BODY_WIDTH, BODY_HEIGHT))

TOP_RIGHT = pygame.image.load("assets/images/top_right_corner.png")
TOP_RIGHT = pygame.transform.scale(TOP_RIGHT, (BODY_WIDTH, BODY_HEIGHT))

BOTTOM_LEFT = pygame.image.load("assets/images/bottom_left_corner.png")
BOTTOM_LEFT = pygame.transform.scale(BOTTOM_LEFT, (BODY_WIDTH, BODY_HEIGHT))

BOTTOM_RIGHT = pygame.image.load("assets/images/bottom_right_corner.png")
BOTTOM_RIGHT = pygame.transform.scale(BOTTOM_RIGHT, (BODY_WIDTH, BODY_HEIGHT))


class SnakeGame:
    def __init__(self):
        # Initialize Pygame
        pygame.display.set_caption("Snake")
        self.window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 36)

        # Snake and game settings
        self.direction = "right"
        self.original_body = BODY
        self.body = self.original_body
        self.original_head = HEAD
        self.head = self.original_head
        self.snake_segments = [pygame.Rect(10, 10, PLAYER_WIDTH, PLAYER_WIDTH)]
        self.segment_directions = ["right"]  # List to store direction of each segment
        self.player_speed = 5
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
        for i, segment in enumerate(self.snake_segments):
            if i == 0:
                self.window.blit(self.head, (segment.x, segment.y))
            else:
                pygame.draw.rect(self.window, RED, self.new, border_radius=10)

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
        if key == pygame.K_a and self.dir_x == 0:  # Move left
            self.head = pygame.transform.rotate(self.original_head, 180)
            self.dir_x, self.dir_y = -self.player_speed, 0
            self.direction = "left"  # Update direction

        elif key == pygame.K_d and self.dir_x == 0:  # Move right
            self.head = pygame.transform.rotate(self.original_head, 0)
            self.dir_x, self.dir_y = self.player_speed, 0
            self.direction = "right"  # Update direction

        elif key == pygame.K_w and self.dir_y == 0:  # Move up
            self.head = pygame.transform.rotate(self.original_head, 90)
            self.dir_x, self.dir_y = 0, -self.player_speed
            self.direction = "up"  # Update direction

        elif key == pygame.K_s and self.dir_y == 0:  # Move down
            self.head = pygame.transform.rotate(self.original_head, 270)
            self.dir_x, self.dir_y = 0, self.player_speed
            self.direction = "down"  # Update direction

    def add_segment(self):
        """Add a new segment to the snake."""
        last_segment = self.snake_segments[-1]
        new_segment = pygame.Rect(last_segment.x, last_segment.y, PLAYER_WIDTH, PLAYER_WIDTH)
        self.snake_segments.append(new_segment)
        self.segment_directions.append(self.direction)  # Append new segment's direction

    def move_snake(self):
        """Move the snake segments."""
        # Move body segments
        for i in range(len(self.snake_segments) - 1, 0, -1):
            self.snake_segments[i].x = self.snake_segments[i - 1].x
            self.snake_segments[i].y = self.snake_segments[i - 1].y
            self.segment_directions[i] = self.segment_directions[i - 1]

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
