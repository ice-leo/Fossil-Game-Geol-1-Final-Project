"""
support.py  –  Utility / helper functions
"""

import pygame
import os


def import_folder(path: str) -> list[pygame.Surface]:
    """Load every image in *path* and return as an ordered list of Surfaces."""
    surface_list = []
    if not os.path.isdir(path):
        # Return a 1-frame placeholder so the game doesn't crash on missing art
        placeholder = pygame.Surface((64, 64))
        placeholder.fill((200, 100, 200))
        return [placeholder]

    for _, __, img_files in os.walk(path):
        for image in sorted(img_files):
            full_path = os.path.join(path, image)
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    if not surface_list:
        placeholder = pygame.Surface((64, 64))
        placeholder.fill((200, 100, 200))
        surface_list.append(placeholder)

    return surface_list


def import_folder_dict(path: str) -> dict[str, pygame.Surface]:
    """Load images from *path* and return {stem: Surface}."""
    surface_dict = {}
    if not os.path.isdir(path):
        return surface_dict

    for _, __, img_files in os.walk(path):
        for image in sorted(img_files):
            full_path = os.path.join(path, image)
            stem = os.path.splitext(image)[0]
            surface_dict[stem] = pygame.image.load(full_path).convert_alpha()

    return surface_dict


def draw_text(surface: pygame.Surface,
              text: str,
              font: pygame.font.Font,
              color,
              pos,
              center: bool = False) -> pygame.Rect:
    """Render *text* onto *surface*. Returns the rect used."""
    rendered = font.render(text, True, color)
    rect = rendered.get_rect()
    if center:
        rect.center = pos
    else:
        rect.topleft = pos
    surface.blit(rendered, rect)
    return rect


def wrap_text(text: str, font: pygame.font.Font, max_width: int) -> list[str]:
    """Split *text* into lines that fit within *max_width* pixels."""
    words = text.split()
    lines, current = [], []
    for word in words:
        test = ' '.join(current + [word])
        if font.size(test)[0] <= max_width:
            current.append(word)
        else:
            if current:
                lines.append(' '.join(current))
            current = [word]
    if current:
        lines.append(' '.join(current))
    return lines
