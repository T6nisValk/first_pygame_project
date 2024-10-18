import pygame
import sys
from random import randint

# Init game
pygame.init()


class Platformer:
    def __init__(self):
        # Window parameters
        self.window = pygame.display.set_mode((1000, 800))
        self.run = True
        self.fps = 60
        self.clock = pygame.time.Clock()

        # Snake
        self.snake_head = pygame.Rect(20, 20, 40, 40)
        self.snake_body_size = 30
        self.snake_speed = 11
        self.segments = []

        # Food
        self.food_size = 30
        self.is_spawned = False

        # State
        self.state = "menu"

        self.hover_start = False
        self.hover_options = False
        self.hover_quit = False
        self.hover_back = False

    def collision(self):
        if self.snake_head.colliderect(self.food):
            self.is_spawned = False

    def create_food(self):
        if not self.is_spawned:
            window_height = self.window.get_height() - self.food_size
            window_width = self.window.get_width() - self.food_size

            self.food = pygame.Rect(
                randint(30, window_width),
                randint(30, window_height),
                self.food_size,
                self.food_size,
            )
            self.is_spawned = True

    def move_snake(self):
        keys = pygame.key.get_pressed()
        x_limit = self.window.get_width() - self.snake_head.width - 10
        y_limit = self.window.get_height() - self.snake_head.height - 10
        if keys[pygame.K_d] and self.snake_head.x < x_limit:
            self.snake_head.x += self.snake_speed
        elif keys[pygame.K_a] and self.snake_head.x > 10:
            self.snake_head.x -= self.snake_speed
        elif keys[pygame.K_w] and self.snake_head.y > 10:
            self.snake_head.y -= self.snake_speed
        elif keys[pygame.K_s] and self.snake_head.y < y_limit:
            self.snake_head.y += self.snake_speed

    def draw_window(self):
        # Draw background
        self.window.fill((0, 0, 0))

        # Draw snake head
        pygame.draw.rect(self.window, (111, 111, 111), self.snake_head, border_radius=30)

        # Draw food
        self.create_food()
        pygame.draw.rect(self.window, (111, 111, 111), self.food, border_radius=30)

        # Update and fps
        self.clock.tick(self.fps)
        pygame.display.update()

    def key_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.state = "menu"

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
                # Draw objects
                self.draw_window()

                # Snake
                self.move_snake()

                # Check collision
                self.collision()

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
        quit_rect = quit_text.get_rect(center=(500, 500))

        self.window.blit(title_text, title_rect)
        self.window.blit(start_text, start_rect)
        self.window.blit(options_text, options_rect)
        self.window.blit(quit_text, quit_rect)

        pygame.display.update()
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
        options_text = font.render("Options Menu", True, (255, 0, 0))
        if not self.hover_back:
            back_text = font.render("Back", True, (255, 255, 255))
        else:
            back_text = font.render("Back", True, (255, 255, 111))

        options_rect = options_text.get_rect(center=(500, 150))
        back_rect = back_text.get_rect(center=(500, 500))

        self.window.blit(options_text, options_rect)
        self.window.blit(back_text, back_rect)

        pygame.display.update()
        mouse_pos = pygame.mouse.get_pos()

        if back_rect.collidepoint(mouse_pos):
            self.hover_back = True
        else:
            self.hover_back = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(mouse_pos):
                    self.state = "menu"
            elif event.type == pygame.QUIT:
                self.run = False
                sys.exit()


if __name__ == "__main__":
    game = Platformer()
    game.run_game()
