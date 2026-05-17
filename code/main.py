"""
main.py – The core engine and State Manager for the Fossil Game.
"""

import pygame
import sys
from settings import WIDTH, HEIGHT, FPS, TITLE
from level import Level
from excavation import ExcavationGame
from fossildex import FossilDex
from quiz import QuizGame
from support import resource_path

class Game:
    def __init__(self):
        # ── Pygame Initialization ────────────────────────────────────────────
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

        # ── Pre-Game Graphics ────────────────────────────────────────────────
        # Load the title and mechanics screens
        self.img_title = pygame.image.load(resource_path('graphics/pregame/title.png')).convert()
        self.img_mechanics = pygame.image.load(resource_path('graphics/pregame/mechanics.png')).convert()

        # ── State Machine ────────────────────────────────────────────────────
        # Valid states: 'title', 'mechanics', 'overworld', 'excavation', 'quiz', 'fossildex'
        self.state = 'title'  # Start the game on the title screen!

        # ── Module Initialization ────────────────────────────────────────────
        self.level = Level(self.change_state)
        self.excavation_game = ExcavationGame(self.end_excavation) 
        self.quiz_game = QuizGame(self.level, self.end_quiz)
        self.fossildex_ui = FossilDex(self.level)

    def change_state(self, new_state: str):
        """
        Callback method passed to other objects. 
        Call this to switch the active screen.
        """
        self.state = new_state

    def end_excavation(self, points_earned, found_ids):
        """Called by excavation.py when the minigame is finished."""
        # Add points to player
        self.level.player.points += points_earned
        
        # Save the specifically found fossils to the level's tracker
        self.level.excavated_fossils.extend(found_ids)
        
        # Add the current level to the list of completed levels
        current_level = len(self.level.exc_levels_done) + 1
        self.level.exc_levels_done.append(current_level)
        
        self.change_state('overworld')
    
    def end_quiz(self):
        """Called by quiz.py when the minigame is finished."""
        self.level.quiz_done = True
        self.change_state('overworld')

    def run(self):
        """The main game loop."""
        while True:
            # ── 1. Event Handling ────────────────────────────────────────────
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    # NEW: Pressing Enter to transition between pre-game screens
                    if event.key == pygame.K_RETURN:
                        if self.state == 'title':
                            self.change_state('mechanics')
                        elif self.state == 'mechanics':
                            self.change_state('overworld')

                    # Global toggle for the FossilDex (Press 'F' to open/close)
                    if event.key == pygame.K_f:
                        if self.state == 'overworld':
                            self.change_state('fossildex')
                        elif self.state == 'fossildex':
                            self.change_state('overworld')

                # Route events directly to the active minigame!
                if self.state == 'excavation' and self.excavation_game.active:
                    self.excavation_game.handle_event(event)

                if self.state == 'fossildex':
                    self.fossildex_ui.handle_event(event)
                
                if self.state == 'quiz' and self.quiz_game.active:
                    self.quiz_game.handle_event(event)

            # ── 2. Update and Draw ───────────────────────────────────────────
            self.screen.fill('black') 

            # Route the logic to the correct module based on the current state
            
            # NEW: Draw the Pre-Game Screens
            if self.state == 'title':
                self.screen.blit(self.img_title, (0, 0))
                
            elif self.state == 'mechanics':
                self.screen.blit(self.img_mechanics, (0, 0))
                
            elif self.state == 'overworld':
                self.level.run()
            
            elif self.state == 'excavation':
                if not self.excavation_game.active:
                    next_level = len(self.level.exc_levels_done) + 1
                    self.excavation_game.start_level(next_level)
                self.excavation_game.run()
            
            elif self.state == 'quiz':
                # Automatically start the quiz logic when entering this state
                if not self.quiz_game.active:
                    self.quiz_game.start_quiz()
                self.quiz_game.draw()
            
            elif self.state == 'fossildex':
                self.fossildex_ui.draw()

            # ── 3. Display Update ────────────────────────────────────────────
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()