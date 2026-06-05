"""
quiz.py – The final test minigame.
Choices are baked into the question images — this code only draws
the cursor on top of whichever answer the player has selected.
"""

import pygame
from settings import (WIDTH, HEIGHT, QUIZ_QUESTIONS,
                      GOLD_THRESHOLD, SILVER_THRESHOLD, BRONZE_THRESHOLD, TROPHY_DATA)
from support import resource_path


# ── Cursor anchor points (left edge of each answer button, 1280×720) ─────────
# Order matches cursor_index: 0=A, 1=B, 2=C, 3=D
# A = top-left,  B = bottom-left,  C = top-right,  D = bottom-right
CURSOR_POSITIONS = [
    (40, 425),   # A  (top-left button)
    (40, 535),   # B  (bottom-left button)
    (625, 425),   # C  (top-right button)
    (625, 535),   # D  (bottom-right button)
]

# Navigation map: which index to jump to for each arrow key
# Layout:   A(0)  C(2)
#           B(1)  D(3)
_NAV = {
    0: {'up': 1, 'down': 1, 'left': 2, 'right': 2},   # A → B vertically, C horizontally
    1: {'up': 0, 'down': 0, 'left': 3, 'right': 3},   # B → A vertically, D horizontally
    2: {'up': 3, 'down': 3, 'left': 0, 'right': 0},   # C → D vertically, A horizontally
    3: {'up': 2, 'down': 2, 'left': 1, 'right': 1},   # D → C vertically, B horizontally
}


class QuizGame:
    def __init__(self, level_ref, return_callback):
        self.display_surface = pygame.display.get_surface()
        self.level_ref        = level_ref
        self.return_callback  = return_callback

        # ── Load Graphics ────────────────────────────────────────────────────
        self.img_cursor = pygame.image.load(
            resource_path('graphics/quiz/cursor/cursor.png')).convert_alpha()
        self.img_qscore = pygame.image.load(
            resource_path('graphics/quiz/end/qscore.png')).convert_alpha()
        self.img_trophy = pygame.image.load(
            resource_path('graphics/quiz/end/trophy.png')).convert_alpha()

        self.q_images = []
        for i in range(len(QUIZ_QUESTIONS)):
            surf = pygame.image.load(
                resource_path(f'graphics/quiz/questions/q{i+1}.png')).convert_alpha()
            self.q_images.append(surf)

        # ── Fonts (score / trophy screens only) ─────────────────────────────
        JOYSTIX = resource_path('graphics/font/joystix.ttf')
        self.font        = pygame.font.Font(JOYSTIX, 20)
        self.medium_font = pygame.font.Font(JOYSTIX, 40)
        self.large_font  = pygame.font.Font(JOYSTIX, 90)

        # ── State ────────────────────────────────────────────────────────────
        self.active            = False
        self.phase             = 'quiz'   # 'quiz' | 'score' | 'trophy'
        self.current_q_index   = 0
        self.cursor_index      = 0        # 0=A 1=B 2=C 3=D
        self.quiz_points_earned = 0

    # ── Public API ───────────────────────────────────────────────────────────

    def start_quiz(self):
        self.active             = True
        self.phase              = 'quiz'
        self.current_q_index    = 0
        self.cursor_index       = 0
        self.quiz_points_earned = 0

    def handle_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        # PHASE 1 — answering questions
        if self.phase == 'quiz':
            nav = _NAV[self.cursor_index]

            if event.key in (pygame.K_UP, pygame.K_w):
                self.cursor_index = nav['up']
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.cursor_index = nav['down']
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                self.cursor_index = nav['left']
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.cursor_index = nav['right']

            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                correct_idx = QUIZ_QUESTIONS[self.current_q_index]['answer']
                if self.cursor_index == correct_idx:
                    self.quiz_points_earned += 2

                self.current_q_index += 1
                self.cursor_index = 0   # reset to A for next question

                if self.current_q_index >= len(QUIZ_QUESTIONS):
                    self.level_ref.player.points += self.quiz_points_earned
                    self.phase = 'score'

        # PHASE 2 — score screen
        elif self.phase == 'score':
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.phase = 'trophy'

        # PHASE 3 — trophy screen
        elif self.phase == 'trophy':
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.end_quiz()

    def end_quiz(self):
        self.active = False
        self.return_callback()

    # ── Drawing ──────────────────────────────────────────────────────────────

    def draw(self):
        if self.phase == 'quiz':
            # 1. Background question image (choices are already drawn on it)
            self.display_surface.blit(self.q_images[self.current_q_index], (0, 0))

            # 2. Cursor on top of the selected answer button
            cx, cy = CURSOR_POSITIONS[self.cursor_index]
            self.display_surface.blit(self.img_cursor, (cx, cy))

        elif self.phase == 'score':
            self.display_surface.blit(self.img_qscore, (0, 0))

            total_pts  = self.level_ref.player.points
            score_text = self.large_font.render(f"{total_pts}", True, 'White')
            score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
            self.display_surface.blit(score_text, score_rect)

            hint = self.font.render("(Press Enter to continue)", True, 'White')
            self.display_surface.blit(hint, hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 200)))

        elif self.phase == 'trophy':
            self.display_surface.blit(self.img_trophy, (0, 0))

            total_pts = self.level_ref.player.points
            if total_pts >= GOLD_THRESHOLD:
                t_type = 'gold'
            elif total_pts >= SILVER_THRESHOLD:
                t_type = 'silver'
            elif total_pts >= BRONZE_THRESHOLD:
                t_type = 'bronze'
            else:
                t_type = 'none'

            t_data    = TROPHY_DATA[t_type]
            rank_text = self.medium_font.render(f"Rank: {t_data['label']}", True, t_data['color'])
            rank_rect = rank_text.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 50))

            shadow = self.medium_font.render(f"Rank: {t_data['label']}", True, 'Black')
            self.display_surface.blit(shadow, rank_rect.move(3, 3))
            self.display_surface.blit(rank_text, rank_rect)

            hint = self.font.render("(Press Enter to conclude your expedition)", True, 'White')
            hint_rect = hint.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))
            hint_shadow = self.font.render("(Press Enter to conclude your expedition)", True, 'Black')
            self.display_surface.blit(hint_shadow, hint_rect.move(3, 3))
            self.display_surface.blit(hint, hint_rect)