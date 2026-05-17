"""
excavation.py – The mining minigame.
"""

import pygame
import random
from settings import *

class ExcavationGame:
    def __init__(self, return_callback):
        self.display_surface = pygame.display.get_surface()
        self.return_callback = return_callback 

        self.cols = 15
        self.rows = 10
        self.offset_x = (WIDTH - (self.cols * TILESIZE)) // 2
        self.offset_y = (HEIGHT - (self.rows * TILESIZE)) // 2

        self.img_soil = pygame.image.load('graphics/excavation/interface/soil.png').convert_alpha()
        self.img_rock = pygame.image.load('graphics/excavation/interface/rock.png').convert_alpha()
        self.img_frame = pygame.image.load('graphics/excavation/interface/excavation_frame.png').convert_alpha()
        self.img_cursor = pygame.image.load('graphics/excavation/cursor/pickaxe.png').convert_alpha()
        
        self.fossil_images = []
        for i in range(1, 7):
            surf = pygame.image.load(f'graphics/excavation/fossils/fossil{i}.png').convert_alpha()
            self.fossil_images.append(surf)

        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 36)

        self.active = False
        self.grid = []
        self.fossils = []
        self.attempts = EXC_MAX_ATTEMPTS
        self.level = 1
        self.game_over = False
        self.result_text = ""
        self.points_earned = 0

    def start_level(self, level_num):
        self.active = True
        self.game_over = False
        self.level = level_num
        self.attempts = EXC_MAX_ATTEMPTS
        self.fossils = []
        pygame.mouse.set_visible(False) 

        self.grid = [[1 for _ in range(self.cols)] for _ in range(self.rows)]

        # IDs for Fossils: Level 1 -> (0, 1) | Level 2 -> (2, 3) | Level 3 -> (4, 5)
        fossil_idx_1 = (level_num - 1) * 2
        fossil_idx_2 = fossil_idx_1 + 1

        self.place_fossil(self.fossil_images[fossil_idx_1], fossil_idx_1)
        self.place_fossil(self.fossil_images[fossil_idx_2], fossil_idx_2)

    def place_fossil(self, image_surf, fossil_id):
        placed = False
        while not placed:
            c = random.randint(0, self.cols - 2)
            r = random.randint(0, self.rows - 2)
            new_rect = pygame.Rect(c, r, 2, 2)
            
            overlap = any(new_rect.colliderect(f['rect']) for f in self.fossils)
            
            if not overlap:
                self.fossils.append({
                    'rect': new_rect, 
                    'img': image_surf, 
                    'found': False,
                    'id': fossil_id  # Save the ID!
                })
                placed = True

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.game_over:
                self.end_minigame()
                return

            mx, my = pygame.mouse.get_pos()
            col = (mx - self.offset_x) // TILESIZE
            row = (my - self.offset_y) // TILESIZE

            if 0 <= col < self.cols and 0 <= row < self.rows:
                if self.grid[row][col] == 1:
                    self.grid[row][col] = 0
                    self.attempts -= 1
                    self.check_fossils()
                    self.check_game_end()

    def check_fossils(self):
        for fossil in self.fossils:
            if fossil['found']:
                continue
                
            c, r = fossil['rect'].topleft
            fully_uncovered = True
            for y in range(r, r + 2):
                for x in range(c, c + 2):
                    if self.grid[y][x] > 0:
                        fully_uncovered = False
                        break
            
            if fully_uncovered:
                fossil['found'] = True

    def check_game_end(self):
        found_count = sum(1 for f in self.fossils if f['found'])
        
        if found_count == 2:
            self.game_over = True
            self.points_earned = (2 * 2) + self.attempts
            self.result_text = f"Success! 2 Fossils Found. Earned {self.points_earned} pts."
        elif self.attempts <= 0:
            self.game_over = True
            self.points_earned = found_count * 2
            self.result_text = f"Out of attempts! {found_count} Fossils Found. Earned {self.points_earned} pts."

    def end_minigame(self):
        pygame.mouse.set_visible(True)
        self.active = False
        
        # Pull the IDs of only the fossils that were fully uncovered
        found_ids = [f['id'] for f in self.fossils if f['found']]
        
        # Return both the points AND the list of found IDs
        self.return_callback(self.points_earned, found_ids)

    def draw(self):
        self.display_surface.fill('#3d2b1f') 

        for row in range(self.rows):
            for col in range(self.cols):
                pixel_x = self.offset_x + (col * TILESIZE)
                pixel_y = self.offset_y + (row * TILESIZE)
                self.display_surface.blit(self.img_rock, (pixel_x, pixel_y))

        for fossil in self.fossils:
            c, r = fossil['rect'].topleft
            pixel_x = self.offset_x + (c * TILESIZE)
            pixel_y = self.offset_y + (r * TILESIZE)
            self.display_surface.blit(fossil['img'], (pixel_x, pixel_y))

        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] == 1:
                    pixel_x = self.offset_x + (col * TILESIZE)
                    pixel_y = self.offset_y + (row * TILESIZE)
                    self.display_surface.blit(self.img_soil, (pixel_x, pixel_y))

        self.display_surface.blit(self.img_frame, (0, 0))

        att_color = 'White' if self.attempts > 3 else 'Red'
        text_surf = self.font.render(f"Attempts: {self.attempts}", True, att_color)
        self.display_surface.blit(text_surf, (50, 50))

        if self.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(150)
            overlay.fill('Black')
            self.display_surface.blit(overlay, (0,0))
            
            res_surf = self.font.render(self.result_text, True, 'Yellow')
            res_rect = res_surf.get_rect(center=(WIDTH//2, HEIGHT//2))
            self.display_surface.blit(res_surf, res_rect)
            
            hint_surf = self.small_font.render("(Click anywhere to continue)", True, 'White')
            hint_rect = hint_surf.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
            self.display_surface.blit(hint_surf, hint_rect)
        
        if not self.game_over:
            mouse_pos = pygame.mouse.get_pos()
            self.display_surface.blit(self.img_cursor, (mouse_pos[0] - 10, mouse_pos[1] - 40))

    def run(self):
        self.draw()