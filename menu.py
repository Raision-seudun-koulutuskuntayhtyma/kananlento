import pygame

from text_render import render_centered_text_lines

DEFAULT_COLOR = (0, 0, 128)
DEFAULT_SELECT_COLOR = (90, 90, 255)
DEFAULT_FONT_FILE = "fonts/SyneMono-Regular.ttf"
DEFAULT_FONT_SIZE = 48


class Menu:
    def __init__(
        self,
        items,
        color=DEFAULT_COLOR,
        select_color=DEFAULT_SELECT_COLOR,
        font_file=DEFAULT_FONT_FILE,
        font_size=DEFAULT_FONT_SIZE,
    ):
        self.items = items
        self.selected_idx = 0
        self.color = color
        self.select_color = select_color
        self.font_file = font_file
        self.set_font_size(font_size)

    def set_font_size(self, size):
        self.font = pygame.font.Font(self.font_file, size)

    def select_next_item(self):
        self.selected_idx += 1
        if self.selected_idx >= len(self.items):
            self.selected_idx = 0

    def select_previous_item(self):
        self.selected_idx -= 1
        if self.selected_idx < 0:
            self.selected_idx = len(self.items) - 1

    def get_selected_item(self):
        return self.items[self.selected_idx]

    def render(self, screen):
        texts_and_colors = [
            (text, self.select_color if i == self.selected_idx else self.color)
            for (i, text) in enumerate(self.items)
        ]
        render_centered_text_lines(screen, self.font, texts_and_colors)
