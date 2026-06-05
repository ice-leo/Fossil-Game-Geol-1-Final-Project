"""
support.py  –  Utility / helper functions
Pygbag-compatible: resource_path resolves relative to this file's directory.
"""

import pygame
import os
import sys


def import_folder(path: str) -> list:
    """Load every image in *path* and return as an ordered list of Surfaces."""
    surface_list = []

    resolved = resource_path(path)

    if not os.path.isdir(resolved):
        placeholder = pygame.Surface((64, 64))
        placeholder.fill((200, 100, 200))
        return [placeholder]

    img_files = sorted(
        f for f in os.listdir(resolved)
        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))
    )

    for image in img_files:
        full_path = os.path.join(resolved, image)
        surface_list.append(pygame.image.load(full_path).convert_alpha())

    if not surface_list:
        placeholder = pygame.Surface((64, 64))
        placeholder.fill((200, 100, 200))
        surface_list.append(placeholder)

    return surface_list


def import_folder_dict(path: str) -> dict:
    """Load images from *path* and return {stem: Surface}."""
    surface_dict = {}
    resolved = resource_path(path)

    if not os.path.isdir(resolved):
        return surface_dict

    for image in sorted(os.listdir(resolved)):
        if image.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            full_path = os.path.join(resolved, image)
            stem = os.path.splitext(image)[0]
            surface_dict[stem] = pygame.image.load(full_path).convert_alpha()

    return surface_dict


def draw_text(surface, text, font, color, pos, center=False):
    """Render *text* onto *surface*. Returns the rect used."""
    rendered = font.render(text, True, color)
    rect = rendered.get_rect()
    if center:
        rect.center = pos
    else:
        rect.topleft = pos
    surface.blit(rendered, rect)
    return rect


def wrap_text(text: str, font, max_width: int) -> list:
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


def resource_path(relative_path: str) -> str:
    """
    Resolve *relative_path* so it works in all three environments:
      1. Running directly as a script   (python main.py)
      2. Packed as a PyInstaller .exe   (sys._MEIPASS is set)
      3. Running inside pygbag / browser (files are beside main.py)

    All assets must sit in the same directory tree as main.py.
    """
    # PyInstaller unpacks to a temp folder stored in sys._MEIPASS
    if hasattr(sys, '_MEIPASS'):
        base = sys._MEIPASS
    else:
        # __file__ is support.py; assets live next to main.py one level up
        # when code/ subfolder layout is used, walk up once if needed.
        base = os.path.dirname(os.path.abspath(__file__))
        # If support.py lives in a 'code/' subdirectory, assets are one level up
        if os.path.basename(base).lower() == 'code':
            base = os.path.dirname(base)

    return os.path.join(base, relative_path)
