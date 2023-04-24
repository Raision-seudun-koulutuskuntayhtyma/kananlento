import pygame

DEFAULT_COLOR = (0, 0, 128)
DEFAULT_SELECT_COLOR = (60, 60, 255)
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
        self.color = color
        self.select_color = select_color
        self.font = pygame.font.Font(font_file, font_size)

    def render(self, screen):
        screen_w = screen.get_width()
        screen_h = screen.get_height()
        text_imgs = [
            self.font.render(text, True, self.color)
            for text in self.items
        ]
        padding = int(screen_h * 0.05)
        total_text_height = sum(img.get_height() for img in text_imgs)
        total_padding = (len(text_imgs) - 1) * padding

        menu_height = total_text_height + total_padding

        y = (screen_h - menu_height) / 2

        for text_img in text_imgs:
            x = (screen_w - text_img.get_width()) / 2
            screen.blit(text_img, (x, y))
            y += padding + text_img.get_height()
