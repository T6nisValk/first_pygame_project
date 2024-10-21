import pygame
import sys
from random import randint
import time

# Init game
pygame.init()
pygame.display.set_caption("Like a Snake")


class LikeASnake:
    def __init__(self):
        # Window parameters
        self.window = pygame.display.set_mode((1000, 800))
        self.run = True
        self.fps = 60
        self.clock = pygame.time.Clock()

        # Snake
        self.snake_head = pygame.Rect(20, 20, 40, 40)
        self.snake_body_size = 30
        self.snake_speed = 4
        self.segments = []
        self.segment = pygame.Rect(
            self.snake_head.centerx,
            self.snake_head.centery,
            self.snake_body_size,
            self.snake_body_size,
        )
        self.segments.append(self.segment)
        self.snake_direction = 0
        self.score = 0
        self.last_turn_time = time.time()
        self.turn_delay = 0.1

        # Food
        self.food_size = 30
        self.is_spawned = False

        # Borders
        self.top = pygame.Rect(0, 0, 1000, 10)
        self.bottom = pygame.Rect(0, 790, 1000, 10)
        self.left = pygame.Rect(0, 0, 10, 800)
        self.right = pygame.Rect(990, 0, 10, 800)

        # State
        self.state = "menu"

        self.game_running = False
        self.hover_start = False
        self.hover_options = False
        self.hover_quit = False
        self.hover_back = False
        self.hover_new = False
        self.hover_main = False
        self.hover_continue = False

    def add_segment(self):
        last_segment_center = self.segments[-1].center

        self.segment = pygame.Rect(
            last_segment_center[0] - self.snake_body_size // 2,
            last_segment_center[1] - self.snake_body_size // 2,
            self.snake_body_size,
            self.snake_body_size,
        )

        self.segments.append(self.segment)

    def collision(self):
        # Check collision with food
        if self.snake_head.colliderect(self.food):
            self.score += 1
            self.snake_speed += 0.05
            self.is_spawned = False
            self.add_segment()

        for index, segment in enumerate(self.segments):
            if index >= 15:
                if self.snake_head.colliderect(segment):
                    self.state = "gameover"
                    print(f"Head: {self.snake_head.x}, {self.snake_head.y}")
                    print(f"Segment: {segment.x}, {segment.y}")

    def create_food(self):
        if not self.is_spawned:

            self.food = pygame.Rect(
                randint(100, 900 - self.food_size),
                randint(100, 700 - self.food_size),
                self.food_size,
                self.food_size,
            )
            self.is_spawned = True

    def move_snake(self):
        keys = pygame.key.get_pressed()
        x_limit = self.window.get_width() - self.snake_head.width
        y_limit = self.window.get_height() - self.snake_head.height

        previous_head_pos = (self.snake_head.x, self.snake_head.y)
        current_time = time.time()

        if self.snake_direction == 0:
            self.snake_head.x += self.snake_speed
            if self.snake_head.x > x_limit:
                self.state = "gameover"
        elif self.snake_direction == 90:
            self.snake_head.y += self.snake_speed
            if self.snake_head.y > y_limit:
                self.state = "gameover"
        elif self.snake_direction == 180:
            self.snake_head.x -= self.snake_speed
            if self.snake_head.x < 0:
                self.state = "gameover"
        elif self.snake_direction == 270:
            self.snake_head.y -= self.snake_speed
            if self.snake_head.y < 0:
                self.state = "gameover"

        if len(self.segments) > 0:
            for i in range(len(self.segments) - 1, 0, -1):
                self.segments[i].x = self.segments[i - 1].x
                self.segments[i].y = self.segments[i - 1].y

            self.segments[0].x = previous_head_pos[0] + 5
            self.segments[0].y = previous_head_pos[1] + 5

        if current_time - self.last_turn_time >= self.turn_delay:
            if keys[pygame.K_d] and self.snake_direction != 180:
                self.snake_direction = 0
                self.last_turn_time = current_time
            elif keys[pygame.K_a] and self.snake_direction != 0:
                self.snake_direction = 180
                self.last_turn_time = current_time
            elif keys[pygame.K_w] and self.snake_direction != 90:
                self.snake_direction = 270
                self.last_turn_time = current_time
            elif keys[pygame.K_s] and self.snake_direction != 270:
                self.snake_direction = 90
                self.last_turn_time = current_time

    def draw_window(self):
        # Draw background
        self.window.fill((0, 0, 0))

        # Draw food
        self.create_food()
        pygame.draw.rect(self.window, (200, 100, 0), self.food, border_radius=30)

        # Draw snake head
        pygame.draw.rect(self.window, (0, 200, 10), self.snake_head, border_radius=30)

        # Drae segments
        for segment in self.segments:
            pygame.draw.rect(self.window, (0, 200, 10), segment, border_radius=30)

        # Score text
        font = pygame.font.SysFont("Arial", 30)

        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.window.blit(score_text, (20, 750))

        # Speed text

        speed_text = font.render(f"Speed: {round(self.snake_speed, 2)}", True, (255, 255, 255))
        self.window.blit(speed_text, (150, 750))
        # Draw Borders
        pygame.draw.rect(self.window, (111, 111, 111), self.top)
        pygame.draw.rect(self.window, (111, 111, 111), self.bottom)
        pygame.draw.rect(self.window, (111, 111, 111), self.left)
        pygame.draw.rect(self.window, (111, 111, 111), self.right)

        # Update and fps
        self.clock.tick(self.fps)
        pygame.display.flip()

    def key_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = "continue"

    def start_game(self):
        # Draw objects
        self.draw_window()

        # Snake
        self.move_snake()

        # Check collision
        self.collision()

    def run_game(self):
        while self.run:

            # Key events
            self.key_event()

            # States
            if self.state == "menu":
                self.main_menu()
            elif self.state == "options":
                self.options_menu()
            elif self.state == "start":
                self.start_game()
            elif self.state == "gameover":
                self.gameover_menu()
            elif self.state == "continue":
                self.continue_menu()

    def gameover_menu(self):
        # Reset game
        self.reset_game()
        self.game_running = False
        # Draw game over menu
        self.window.fill((0, 0, 0))
        font = pygame.font.SysFont("Arial", 60)

        score_text = font.render(f"Your score: {self.score}", True, (255, 255, 255))
        gameover_text = font.render("Game Over", True, (255, 0, 0))
        if not self.hover_new:
            new_game_text = font.render("New Game", True, (255, 255, 255))
        else:
            new_game_text = font.render("New Game", True, (255, 255, 111))
        if not self.hover_main:
            main_menu_text = font.render("Main Menu", True, (255, 255, 255))
        else:
            main_menu_text = font.render("Main Menu", True, (255, 255, 111))
        if not self.hover_quit:
            quit_text = font.render("Quit", True, (255, 255, 255))
        else:
            quit_text = font.render("Quit", True, (255, 255, 111))

        score_rect = score_text.get_rect(center=(500, 750))
        gameover_rect = gameover_text.get_rect(center=(500, 150))
        main_menu_rect = main_menu_text.get_rect(center=(500, 300))
        new_game_rect = new_game_text.get_rect(center=(500, 400))
        quit_rect = quit_text.get_rect(center=(500, 500))

        self.window.blit(score_text, score_rect)
        self.window.blit(gameover_text, gameover_rect)
        self.window.blit(main_menu_text, main_menu_rect)
        self.window.blit(new_game_text, new_game_rect)
        self.window.blit(quit_text, quit_rect)

        pygame.display.flip()
        mouse_pos = pygame.mouse.get_pos()

        if new_game_rect.collidepoint(mouse_pos):
            self.hover_new = True
        else:
            self.hover_new = False
        if quit_rect.collidepoint(mouse_pos):
            self.hover_quit = True
        else:
            self.hover_quit = False
        if main_menu_rect.collidepoint(mouse_pos):
            self.hover_main = True
        else:
            self.hover_main = False

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:

                if new_game_rect.collidepoint(mouse_pos):
                    self.score = 0
                    self.snake_speed = 4
                    self.state = "start"
                elif main_menu_rect.collidepoint(mouse_pos):
                    self.score = 0
                    self.snake_speed = 4
                    self.state = "menu"
                elif quit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

            elif event.type == pygame.QUIT:
                self.run = False
                sys.exit()

    def continue_menu(self):
        self.window.fill((0, 0, 0))
        font = pygame.font.SysFont("Arial", 60)
        title_text = font.render("Main menu", True, (255, 0, 0))
        if not self.hover_continue:
            continue_text = font.render("Continue", True, (255, 255, 255))
        else:
            continue_text = font.render("Continue", True, (255, 255, 111))
        if not self.hover_new:
            new_game_text = font.render("New Game", True, (255, 255, 255))
        else:
            new_game_text = font.render("New Game", True, (255, 255, 111))
        if not self.hover_options:
            options_text = font.render("Options", True, (255, 255, 255))
        else:
            options_text = font.render("Options", True, (255, 255, 111))
        if not self.hover_quit:
            quit_text = font.render("Quit", True, (255, 255, 255))
        else:
            quit_text = font.render("Quit", True, (255, 255, 111))

        title_rect = title_text.get_rect(center=(500, 150))
        continute_rect = continue_text.get_rect(center=(500, 300))
        new_game_rect = new_game_text.get_rect(center=(500, 400))
        options_rect = options_text.get_rect(center=(500, 500))
        quit_rect = quit_text.get_rect(center=(500, 600))

        self.window.blit(title_text, title_rect)
        self.window.blit(continue_text, continute_rect)
        self.window.blit(new_game_text, new_game_rect)
        self.window.blit(options_text, options_rect)
        self.window.blit(quit_text, quit_rect)

        pygame.display.flip()
        mouse_pos = pygame.mouse.get_pos()

        if continute_rect.collidepoint(mouse_pos):
            self.hover_continue = True
        else:
            self.hover_continue = False
        if new_game_rect.collidepoint(mouse_pos):
            self.hover_new = True
        else:
            self.hover_new = False
        if options_rect.collidepoint(mouse_pos):
            self.hover_options = True
        else:
            self.hover_options = False

        if quit_rect.collidepoint(mouse_pos):
            self.hover_quit = True
        else:
            self.hover_quit = False

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if continute_rect.collidepoint(mouse_pos):
                    self.state = "start"
                elif options_rect.collidepoint(mouse_pos):
                    self.state = "options"
                elif new_game_rect.collidepoint(mouse_pos):
                    self.reset_game()
                    self.score = 0
                    self.snake_speed = 4
                    self.state = "start"
                elif quit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

            elif event.type == pygame.QUIT:
                self.run = False
                sys.exit()

    def main_menu(self):
        self.window.fill((0, 0, 0))

        font = pygame.font.SysFont("Arial", 60)

        title_text = font.render("Main Menu", True, (255, 0, 0))
        if not self.hover_start:
            start_text = font.render("Start Game", True, (255, 255, 255))
        else:
            start_text = font.render("Start Game", True, (255, 255, 111))

        if not self.hover_options:
            options_text = font.render("Options", True, (255, 255, 255))
        else:
            options_text = font.render("Options", True, (255, 255, 111))
        if not self.hover_quit:
            quit_text = font.render("Quit", True, (255, 255, 255))
        else:
            quit_text = font.render("Quit", True, (255, 255, 111))

        title_rect = title_text.get_rect(center=(500, 150))
        start_rect = start_text.get_rect(center=(500, 300))
        options_rect = options_text.get_rect(center=(500, 400))
        quit_rect = quit_text.get_rect(center=(500, 600))

        self.window.blit(title_text, title_rect)
        self.window.blit(start_text, start_rect)
        self.window.blit(options_text, options_rect)
        self.window.blit(quit_text, quit_rect)

        pygame.display.flip()
        mouse_pos = pygame.mouse.get_pos()

        if start_rect.collidepoint(mouse_pos):
            self.hover_start = True
        else:
            self.hover_start = False

        if options_rect.collidepoint(mouse_pos):
            self.hover_options = True
        else:
            self.hover_options = False

        if quit_rect.collidepoint(mouse_pos):
            self.hover_quit = True
        else:
            self.hover_quit = False

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(mouse_pos):
                    self.game_running = True
                    self.state = "start"
                elif options_rect.collidepoint(mouse_pos):
                    self.state = "options"
                elif quit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

            elif event.type == pygame.QUIT:
                self.run = False
                sys.exit()

    def options_menu(self):
        self.window.fill((0, 0, 0))

        font = pygame.font.SysFont("Arial", 60)
        placeholder = font.render("Nothing here yet", True, (255, 255, 255))
        options_text = font.render("Options Menu", True, (255, 0, 0))
        if not self.hover_back:
            back_text = font.render("Back", True, (255, 255, 255))
        else:
            back_text = font.render("Back", True, (255, 255, 111))

        placeholder_rect = placeholder.get_rect(center=(500, 300))
        options_rect = options_text.get_rect(center=(500, 150))
        back_rect = back_text.get_rect(center=(500, 600))

        self.window.blit(placeholder, placeholder_rect)
        self.window.blit(options_text, options_rect)
        self.window.blit(back_text, back_rect)

        pygame.display.flip()
        mouse_pos = pygame.mouse.get_pos()

        if back_rect.collidepoint(mouse_pos):
            self.hover_back = True
        else:
            self.hover_back = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(mouse_pos):
                    if self.game_running:
                        self.state = "continue"
                    else:
                        self.state = "menu"
            elif event.type == pygame.QUIT:
                self.run = False
                sys.exit()

    def reset_game(self):
        # Reset snake head position and direction
        self.snake_head = pygame.Rect(20, 20, 40, 40)
        self.snake_direction = 0

        # Reset food spawn state
        self.is_spawned = False

        # Reset score and segments
        self.segments = []

        # Add the initial segment (positioned just behind the snake's head initially)
        self.segment = pygame.Rect(
            self.snake_head.centerx - self.snake_body_size,  # Start it just behind the head
            self.snake_head.centery,
            self.snake_body_size,
            self.snake_body_size,
        )
        self.segments.append(self.segment)

        # Reset snake speed
        self.snake_speed = 4


if __name__ == "__main__":
    game = LikeASnake()
    game.run_game()
