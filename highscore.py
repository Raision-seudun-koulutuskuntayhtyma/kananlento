import datetime
import enum
import json
import pathlib

import pygame

from text_render import render_centered_text_lines

DEFAULT_COLOR = (160, 160, 0)
DEFAULT_FONT_FILE = "fonts/SyneMono-Regular.ttf"
DEFAULT_FONT_SIZE = 48

HIGHSCORE_FILE_PATH = pathlib.Path(__file__).parent / "highscores.json"


class HighscoreAction(enum.Enum):
    CLOSE = enum.auto()


class HighscoreRecorder:
    def __init__(
        self,
        color=DEFAULT_COLOR,
        font_file=DEFAULT_FONT_FILE,
        font_size=DEFAULT_FONT_SIZE,
    ):
        self.color = color
        self.font_file = font_file
        self.set_font_size(font_size)
        self.text = ""
        self.score = None
        self.file = HighscoreFile()

    def set_font_size(self, size):
        self.font = pygame.font.Font(self.font_file, size)

    def record_highscore(self, score):
        self.score = score

    def handle_event(self, event) -> "HighscoreAction | None":
        if event.type == pygame.TEXTINPUT:
            self.text += event.text
            return None

        if event.type != pygame.KEYUP:
            return None

        if event.key == pygame.K_ESCAPE:
            return HighscoreAction.CLOSE
        elif event.key == pygame.K_RETURN:
            self.file.add_entry(name=self.text, score=self.score)
            self.file.save()
            return HighscoreAction.CLOSE
        elif event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]

        return None

    def render(self, screen):
        texts_and_colors = [
            ("New highscore!", self.color),
            (str(self.score), self.color),
            ("Enter your name: ", self.color),
            (self.text, self.color),
        ]
        render_centered_text_lines(screen, self.font, texts_and_colors)


class HighscoreFile:
    def __init__(self):
        if HIGHSCORE_FILE_PATH.exists():
            with open(HIGHSCORE_FILE_PATH, "r") as fp:
                self.entries = json.load(fp)
        else:
            self.entries = []

    def add_entry(self, name, score):
        date = datetime.datetime.now().isoformat()
        self.entries.append((score, name, date))
        self.entries.sort(reverse=True)

    def save(self):
        with open(HIGHSCORE_FILE_PATH, "w") as fp:
            json.dump(self.entries, fp)
