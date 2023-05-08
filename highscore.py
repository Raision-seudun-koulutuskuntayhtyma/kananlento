import datetime
import enum
import json
import pathlib

import pygame

from text_render import render_centered_text_lines

DEFAULT_COLOR = (160, 160, 0)
DEFAULT_FONT_FILE = "fonts/SyneMono-Regular.ttf"
DEFAULT_RECORD_FONT_SIZE = 48
DEFAULT_DISPLAY_FONT_SIZE = 32

HIGHSCORE_FILE_PATH = pathlib.Path(__file__).parent / "highscores.json"


class HighscoreAction(enum.Enum):
    CLOSE = enum.auto()


class HighscoreRecorder:
    def __init__(
        self,
        color=DEFAULT_COLOR,
        font_file=DEFAULT_FONT_FILE,
        font_size=DEFAULT_RECORD_FONT_SIZE,
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


class HighscoresDisplay:
    def __init__(
        self,
        color=DEFAULT_COLOR,
        font_file=DEFAULT_FONT_FILE,
        font_size=DEFAULT_DISPLAY_FONT_SIZE,
    ):
        self.color = color
        self.font_file = font_file
        self.set_font_size(font_size)
        self.file = HighscoreFile()

    def set_font_size(self, size):
        self.font = pygame.font.Font(self.font_file, size)

    def reload_file(self):
        self.file.load()

    def handle_event(self, event) -> "HighscoreAction | None":
        if event.type == pygame.KEYUP:
            return HighscoreAction.CLOSE
        return None

    def render(self, screen):
        entries = self.file.get_top_10()

        def format_date(date):
            return f"{date:%d.%m. %H:%M}" if date else ""

        lines = [
            f"{n:2}. {name:20} {score:4}   {format_date(date):12}"
            for (n, (score, name, date)) in enumerate(entries, 1)
        ]
        texts_and_colors = [
            (line, self.color)
            for line in lines
        ]
        render_centered_text_lines(screen, self.font, texts_and_colors,
                                   padding_perc=0.01)


class HighscoreFile:
    def __init__(self):
        self.load()

    def load(self):
        if HIGHSCORE_FILE_PATH.exists():
            with open(HIGHSCORE_FILE_PATH, "r") as fp:
                data = json.load(fp)
                self.entries = [
                    (score, name, datetime.datetime.fromisoformat(date_str))
                    for (score, name, date_str) in data
                ]
        else:
            self.entries = []

    def save(self):
        with open(HIGHSCORE_FILE_PATH, "w") as fp:
            data = [
                (score, name, date.isoformat())
                for (score, name, date) in self.entries
            ]
            json.dump(data, fp)

    def get_top_10(self):
        count = len(self.entries)
        if count >= 10:
            return self.entries[:10]
        empty_entries = (10 - count) * [("", "", None)]
        return self.entries + empty_entries

    def add_entry(self, name, score):
        date = datetime.datetime.now()
        self.entries.append((score, name, date))
        self.sort_scores()

    def sort_scores(self):
        """
        Järjestä nousevaan järjestykseen siten, että pisteet käännetään
        negatiiviseksi, jolloin suurimmat pisteet tulevat ensin.

        Järjestettävät asiat ovat siis seuraavanlaisia:

            -99  2023-05-08T13:35:00  Nimi1
            -88  2023-05-06T10:00:00  Nimi2
            -77  2023-05-07T20:00:00  Nimi3
            -77  2023-05-08T10:00:00  Nimi4

        Huomaa, että pisteet ovat ensisijainen järjestystekijä ja
        aikaileima on toinen järjestystekijä, jolloin samalla
        pistemäärällä olevat rivit järjestyvät aikaleiman mukaan
        """
        def sort_key(item):
            (score, name, date) = item
            return (-score, date, name)

        self.entries.sort(key=sort_key)
