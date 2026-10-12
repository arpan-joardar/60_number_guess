import random
import pygame
from game.text_box import TextBox

MIN_NUMBER = 1
MAX_NUMBER = 100

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.input_box = TextBox(width // 2 - 110, 190, 120, 48)
        self.submit_btn = pygame.Rect(width // 2 + 25, 190, 100, 48)

        self.font_title = pygame.font.SysFont(None, 42)
        self.font_medium = pygame.font.SysFont(None, 28)
        self.font_btn = pygame.font.SysFont(None, 26)
        self.font_small = pygame.font.SysFont(None, 22)

        self.reset()

    def show_warning(self, message):
        self.feedback_msg = message
        self.feedback_color = (250, 200, 70)

    def submit_guess(self):
        if self.game_won:
            return

        text = self.input_box.text.strip()
        if not text:
            self.show_warning("Please enter a number first!")
            return

        try:
            guess = int(text)
        except ValueError:
            self.input_box.clear()
            self.show_warning("Invalid input! Digits only.")
            return

        if not MIN_NUMBER <= guess <= MAX_NUMBER:
            self.input_box.clear()
            self.show_warning(f"{guess} is out of range! Pick {MIN_NUMBER} - {MAX_NUMBER}.")
            return

        self.attempts += 1
        self.input_box.clear()

        if guess < self.secret_number:
            self.low = max(self.low, guess + 1)
            self.feedback_msg = f"TOO LOW! (Guess was {guess})"
            self.feedback_color = (80, 160, 240)
        elif guess > self.secret_number:
            self.high = min(self.high, guess - 1)
            self.feedback_msg = f"TOO HIGH! (Guess was {guess})"
            self.feedback_color = (240, 100, 80)
        else:
            self.low = self.high = guess
            self.feedback_msg = f"CORRECT! Found in {self.attempts} attempts."
            self.feedback_color = (80, 220, 90)
            self.game_won = True

    def reset(self):
        self.secret_number = random.randint(MIN_NUMBER, MAX_NUMBER)
        self.attempts = 0
        self.low = MIN_NUMBER
        self.high = MAX_NUMBER
        self.feedback_msg = f"Enter a number between {MIN_NUMBER} and {MAX_NUMBER}"
        self.feedback_color = (220, 220, 220)
        self.game_won = False
        self.input_box.clear()

    def handle_event(self, event):
        self.input_box.handle_event(event)

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self.submit_guess()
            elif event.key == pygame.K_r and self.game_won:
                self.reset()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.submit_btn.collidepoint(event.pos):
                self.input_box.active = True
                self.submit_guess()

    def update(self):
        pass

    def render_range(self, screen):
        if self.low < self.high:
            label = f"Range: {self.low} - {self.high}"
        else:
            label = f"Range: {self.low}"
        range_surf = self.font_medium.render(label, True, (235, 235, 240))
        screen.blit(range_surf, (self.width // 2 - range_surf.get_width() // 2, 122))

        track = pygame.Rect(self.width // 2 - 200, 156, 400, 10)
        span = MAX_NUMBER - MIN_NUMBER + 1
        start = track.x + (self.low - MIN_NUMBER) * track.width // span
        end = track.x + (self.high - MIN_NUMBER + 1) * track.width // span
        pygame.draw.rect(screen, (55, 61, 74), track, border_radius=5)
        pygame.draw.rect(screen, (90, 200, 150), (start, track.y, end - start, track.height), border_radius=5)

        min_surf = self.font_small.render(str(MIN_NUMBER), True, (150, 155, 165))
        max_surf = self.font_small.render(str(MAX_NUMBER), True, (150, 155, 165))
        label_y = track.centery - min_surf.get_height() // 2
        screen.blit(min_surf, (track.x - min_surf.get_width() - 10, label_y))
        screen.blit(max_surf, (track.right + 10, label_y))

    def render(self, screen):
        screen.fill((30, 34, 42))

        title_surf = self.font_title.render("Number Guessing Arena", True, (245, 245, 245))
        screen.blit(title_surf, (self.width // 2 - title_surf.get_width() // 2, 35))

        attempts_surf = self.font_medium.render(f"Attempts: {self.attempts}", True, (180, 185, 195))
        screen.blit(attempts_surf, (self.width // 2 - attempts_surf.get_width() // 2, 88))
        self.render_range(screen)
        self.input_box.render(screen)

        pygame.draw.rect(screen, (50, 150, 80), self.submit_btn, border_radius=6)
        pygame.draw.rect(screen, (220, 220, 220), self.submit_btn, width=2, border_radius=6)
        btn_text = self.font_btn.render("SUBMIT", True, (255, 255, 255))
        screen.blit(
            btn_text,
            (self.submit_btn.centerx - btn_text.get_width() // 2, self.submit_btn.centery - btn_text.get_height() // 2),
        )

        feedback_surf = self.font_medium.render(self.feedback_msg, True, self.feedback_color)
        screen.blit(feedback_surf, (self.width // 2 - feedback_surf.get_width() // 2, 268))

        if self.game_won:
            restart_surf = self.font_medium.render("Press [R] to Start a New Game", True, (255, 220, 80))
            screen.blit(restart_surf, (self.width // 2 - restart_surf.get_width() // 2, 318))
