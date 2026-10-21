import json
import pygame


class Settings:
    FILE = 'settings.json'
    MAX_VOLUME = 10
    ACTIONS = [
        ('left', "Move Left"),
        ('right', "Move Right"),
        ('up', "Move Up"),
        ('down', "Move Down"),
        ('fire', "Fire"),
    ]
    DEFAULT_CONTROLS = {'left': 'left', 'right': 'right', 'up': 'up', 'down': 'down', 'fire': 'space'}

    def __init__(self):
        self.music_volume = 4
        self.sfx_volume = 10
        self.controls = {action: pygame.key.key_code(name) for action, name in self.DEFAULT_CONTROLS.items()}
        self.sounds = []
        self.load()

    def load(self):
        try:
            with open(self.FILE, 'r', encoding='utf-8') as file:
                data = json.load(file)
            self.music_volume = self.clamp(int(data.get('music_volume', self.music_volume)))
            self.sfx_volume = self.clamp(int(data.get('sfx_volume', self.sfx_volume)))
            for action, name in data.get('controls', {}).items():
                if action in self.controls:
                    self.controls[action] = pygame.key.key_code(name)
        except (OSError, ValueError, TypeError, AttributeError):
            pass

    def save(self):
        data = {
            'music_volume': self.music_volume,
            'sfx_volume': self.sfx_volume,
            'controls': {action: pygame.key.name(key) for action, key in self.controls.items()},
        }
        with open(self.FILE, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2)

    def clamp(self, volume):
        return max(0, min(self.MAX_VOLUME, volume))

    def register_sound(self, sound):
        self.sounds.append(sound)
        sound.set_volume(self.sfx_volume / self.MAX_VOLUME)

    def apply(self):
        # pygame resets the music volume whenever new music is loaded, so call this after loading
        pygame.mixer.music.set_volume(self.music_volume / self.MAX_VOLUME)
        for sound in self.sounds:
            sound.set_volume(self.sfx_volume / self.MAX_VOLUME)

    def adjust_volume(self, channel, delta):
        if channel == 'music':
            self.music_volume = self.clamp(self.music_volume + delta)
        else:
            self.sfx_volume = self.clamp(self.sfx_volume + delta)
        self.apply()
        self.save()

    def bind(self, action, key):
        # A key can only drive one action, so swap with whichever action already uses it
        for other, other_key in self.controls.items():
            if other_key == key:
                self.controls[other] = self.controls[action]
        self.controls[action] = key
        self.save()
