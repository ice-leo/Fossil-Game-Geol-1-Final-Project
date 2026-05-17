"""
ui.py  –  Heads-Up Display.
           Shows: current score, FossilDex button, interaction hint.
"""

import pygame
from settings import TEXT_COLOR, UI_BG_COLOR


class UI:

    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        # Fonts
        self.font_large  = pygame.font.Font(None, 42)
        self.font_medium = pygame.font.Font(None, 30)
        self.font_small  = pygame.font.Font(None, 24)

        # FossilDex button rect (top-right corner)
        self.dex_btn_rect = pygame.Rect(
            self.display_surface.get_width() - 170, 10, 160, 44
        )

    # ── Score ────────────────────────────────────────────────────────────────

    def _draw_score(self, points: int):
        label = self.font_large.render(f'Points: {points}', True, TEXT_COLOR)
        bg    = label.get_rect(topleft=(10, 10)).inflate(16, 8)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg, border_radius=6)
        self.display_surface.blit(label, (18, 14))

    # ── FossilDex button ─────────────────────────────────────────────────────

    def _draw_fossildex_button(self):
        pygame.draw.rect(self.display_surface, '#2a4a2a',
                         self.dex_btn_rect, border_radius=8)
        pygame.draw.rect(self.display_surface, '#55aa55',
                         self.dex_btn_rect, 2, border_radius=8)
        label = self.font_small.render('FossilDex (Press F)', True, TEXT_COLOR)
        lrect = label.get_rect(center=self.dex_btn_rect.center)
        self.display_surface.blit(label, lrect)

    # ── Interaction hint ─────────────────────────────────────────────────────

    def _draw_hint(self, text: str):
        if not text:
            return
        label = self.font_small.render(text, True, TEXT_COLOR)
        bg    = label.get_rect(
            midbottom=(self.display_surface.get_width() // 2,
                       self.display_surface.get_height() - 12)
        ).inflate(20, 10)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg, border_radius=6)
        self.display_surface.blit(label, bg.inflate(-20, -10))

    # ── Game-state indicators ────────────────────────────────────────────────

    def _draw_game_progress(self, exc_levels_done: list, quiz_done: bool):
        """Small indicator in top-left below score showing which games are done."""
        y = 64
        for lvl in range(1, 4):
            done  = lvl in exc_levels_done
            color = "#001eff" if done else '#555555'
            label = self.font_small.render(
                f'Dig {lvl}: {"Done" if done else "Not yet completed"}', True, color
            )
            self.display_surface.blit(label, (18, y))
            y += 22

        color = '#55aa55' if quiz_done else '#555555'
        label = self.font_small.render(
            f'Quiz: {"Done" if quiz_done else "Not yet completed"}', True, color
        )
        self.display_surface.blit(label, (18, y))

    # ── Main draw ────────────────────────────────────────────────────────────

    def display(self, points: int, hint: str,
                exc_levels_done: list, quiz_done: bool):
        self._draw_score(points)
        self._draw_fossildex_button()
        self._draw_hint(hint)
        self._draw_game_progress(exc_levels_done, quiz_done)

    def fossildex_btn_clicked(self, mouse_pos) -> bool:
        return self.dex_btn_rect.collidepoint(mouse_pos)
