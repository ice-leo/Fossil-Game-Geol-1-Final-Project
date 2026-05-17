"""
quiz.py – The final test minigame.
"""

import pygame
from settings import (WIDTH, HEIGHT, QUIZ_QUESTIONS, 
                      GOLD_THRESHOLD, SILVER_THRESHOLD, BRONZE_THRESHOLD, TROPHY_DATA)

class QuizGame:
    def __init__(self, level_ref, return_callback):
        self.display_surface = pygame.display.get_surface()
        self.level_ref = level_ref
        self.return_callback = return_callback 

        # ── Load Graphics ────────────────────────────────────────────────────
        self.img_cursor = pygame.image.load('graphics/quiz/cursor/cursor.png').convert_alpha()
        self.img_qscore = pygame.image.load('graphics/quiz/end/qscore.png').convert_alpha()
        self.img_trophy = pygame.image.load('graphics/quiz/end/trophy.png').convert_alpha()

        # Load all question background images dynamically based on the settings list
        self.q_images = []
        for i in range(len(QUIZ_QUESTIONS)):
            # Note: Assuming files are named q1.png, q2.png, etc.
            surf = pygame.image.load(f'graphics/quiz/questions/q{i+1}.png').convert_alpha()
            self.q_images.append(surf)

        # ── Fonts ────────────────────────────────────────────────────────────
        self.font = pygame.font.Font(None, 50)
        self.medium_font = pygame.font.Font(None, 70)
        self.large_font = pygame.font.Font(None, 90)

        # ── State Variables ──────────────────────────────────────────────────
        self.active = False
        self.phase = 'quiz' # Phases: 'quiz', 'score', 'trophy'
        self.current_q_index = 0
        self.cursor_index = 0
        self.quiz_points_earned = 0

    def start_quiz(self):
        """Initializes the quiz variables when the player talks to the professor."""
        self.active = True
        self.phase = 'quiz'
        self.current_q_index = 0
        self.cursor_index = 0
        self.quiz_points_earned = 0

    def handle_event(self, event):
        """Handles keyboard input passed from main.py"""
        if event.type == pygame.KEYDOWN:
            
            # PHASE 1: Answering Questions
            if self.phase == 'quiz':
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.cursor_index = (self.cursor_index - 1) % 4
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.cursor_index = (self.cursor_index + 1) % 4
                
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    # Check if answer is correct (using the 'answer' index from settings)
                    correct_idx = QUIZ_QUESTIONS[self.current_q_index]['answer']
                    if self.cursor_index == correct_idx:
                        # Award 2 points per correct answer (adjust as you see fit!)
                        self.quiz_points_earned += 2 

                    self.current_q_index += 1
                    self.cursor_index = 0 # Reset cursor to 'A' for the next question

                    # Check if we finished the last question
                    if self.current_q_index >= len(QUIZ_QUESTIONS):
                        # Add quiz points to the player's total right away
                        self.level_ref.player.points += self.quiz_points_earned
                        self.phase = 'score'
            
            # PHASE 2: Viewing the Total Score
            elif self.phase == 'score':
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self.phase = 'trophy'
            
            # PHASE 3: Viewing the Trophy
            elif self.phase == 'trophy':
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self.end_quiz()

    def end_quiz(self):
        self.active = False
        self.return_callback()

    def draw(self):
        if self.phase == 'quiz':
            # 1. Draw the background question image
            self.display_surface.blit(self.q_images[self.current_q_index], (0, 0))

            # 2. Draw the 4 options in the lower right
            start_x = 700
            start_y = 350
            spacing = 60
            letters = ['A', 'B', 'C', 'D']
            
            options = QUIZ_QUESTIONS[self.current_q_index]['options']

            for i in range(4):
                y_pos = start_y + (i * spacing)
                
                # Format: "A. Soft body"
                text = f"{letters[i]}. {options[i]}"
                text_surf = self.font.render(text, True, 'White')
                
                # Draw a subtle dark shadow behind the text for readability
                shadow_surf = self.font.render(text, True, 'Black')
                self.display_surface.blit(shadow_surf, (start_x + 2, y_pos + 2))
                self.display_surface.blit(text_surf, (start_x, y_pos))

                # 3. Draw the cursor pointing at the current selection
                if i == self.cursor_index:
                    self.display_surface.blit(self.img_cursor, (start_x - 70, y_pos - 15))

        elif self.phase == 'score':
            # Draw score background
            self.display_surface.blit(self.img_qscore, (0, 0))
            
            # Draw total points in the center
            total_pts = self.level_ref.player.points
            score_text = self.large_font.render(f"Final Score: {total_pts}", True, 'White')
            score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2))
            
            # Shadow and Text
            shadow = self.large_font.render(f"Final Score: {total_pts}", True, 'Black')
            self.display_surface.blit(shadow, score_rect.move(3, 3))
            self.display_surface.blit(score_text, score_rect)
            
            hint = self.font.render("(Press Enter to continue)", True, 'Yellow')
            self.display_surface.blit(hint, hint.get_rect(center=(WIDTH//2, HEIGHT//2 + 80)))

        elif self.phase == 'trophy':
            # Draw trophy background
            self.display_surface.blit(self.img_trophy, (0, 0))
            
            # Calculate trophy tier
            total_pts = self.level_ref.player.points
            if total_pts >= GOLD_THRESHOLD:
                t_type = 'gold'
            elif total_pts >= SILVER_THRESHOLD:
                t_type = 'silver'
            elif total_pts >= BRONZE_THRESHOLD:
                t_type = 'bronze'
            else:
                t_type = 'none'

            # Fetch styling from settings.py
            t_data = TROPHY_DATA[t_type]
            label = t_data['label']
            color = t_data['color']

            rank_text = self.large_font.render(f"Rank: {label}", True, color)
            rank_rect = rank_text.get_rect(center=(WIDTH//2, HEIGHT//2))
            
            shadow = self.large_font.render(f"Rank: {label}", True, 'Black')
            self.display_surface.blit(shadow, rank_rect.move(3, 3))
            self.display_surface.blit(rank_text, rank_rect)

            hint = self.medium_font.render("(Press Enter to conclude your expedition)", True, 'Gray')
            self.display_surface.blit(hint, hint.get_rect(center=(WIDTH//2, HEIGHT//2 + 80)))