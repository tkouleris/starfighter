import json
import logging
import pygame


class HighScores:
    FILE = 'highscores.json'
    MAX_ENTRIES = 10

    def __init__(self):
        self.entries = self.load()
        self.title_font = pygame.font.SysFont('comicsans', 30, True, True)
        self.font = pygame.font.SysFont('comicsans', 20, True, True)

    def load(self):
        try:
            with open(self.FILE, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (OSError, ValueError):
            return []

    def save(self):
        # A failed save (e.g. read-only folder) must not crash the game; the table still shows this session's scores
        try:
            with open(self.FILE, 'w', encoding='utf-8') as file:
                json.dump(self.entries, file, indent=2)
        except OSError as error:
            logging.warning("Could not save %s: %s", self.FILE, error)

    def qualifies(self, score):
        if score <= 0:
            return False
        return len(self.entries) < self.MAX_ENTRIES or score > self.entries[-1]['score']

    def add(self, name, score):
        self.entries.append({'name': name, 'score': score})
        self.entries.sort(key=lambda entry: entry['score'], reverse=True)
        self.entries = self.entries[:self.MAX_ENTRIES]
        self.save()

    def draw(self, screen, y):
        text = self.title_font.render("HIGH SCORES", 1, (255, 255, 0))
        screen.blit(text, (320 - (text.get_width() / 2), y))
        y += 45

        if not self.entries:
            text = self.font.render("No scores yet", 1, (255, 255, 255))
            screen.blit(text, (320 - (text.get_width() / 2), y))
            return

        for rank, entry in enumerate(self.entries, start=1):
            text = self.font.render(f"{rank:>2}. {entry['name']:<3}  {entry['score']:>6}", 1, (255, 255, 255))
            screen.blit(text, (320 - (text.get_width() / 2), y))
            y += 26
