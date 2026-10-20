import math
import random
import pygame


class Explosion:
    # Color stages from fresh blast to dying embers
    colors = [(255, 255, 220), (255, 220, 80), (255, 140, 0), (200, 50, 0), (90, 20, 10)]

    def __init__(self, window, center, size=1.0, duration=30):
        self.window = window
        self.x, self.y = center
        self.size = size
        self.duration = duration
        self.frame = 0
        self.particles = []
        for _ in range(int(24 * size)):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(0.5, 3) * size
            # [x, y, velocity x, velocity y, radius]
            self.particles.append([self.x, self.y, math.cos(angle) * speed, math.sin(angle) * speed,
                                   random.uniform(2, 5) * size])

    @property
    def finished(self):
        return self.frame >= self.duration

    def draw(self):
        if self.finished:
            return
        progress = self.frame / self.duration
        color = self.colors[min(int(progress * len(self.colors)), len(self.colors) - 1)]

        # Bright core and shockwave ring during the first part of the blast
        if progress < 0.3:
            flash = progress / 0.3
            pygame.draw.circle(self.window, (255, 255, 255), (self.x, self.y), int(12 * self.size * (1 - flash)) + 1)
            pygame.draw.circle(self.window, (255, 200, 120), (self.x, self.y), int(24 * self.size * flash) + 2, 2)

        for particle in self.particles:
            particle[0] += particle[2]
            particle[1] += particle[3]
            particle[2] *= 0.95
            particle[3] *= 0.95
            radius = particle[4] * (1 - progress)
            if radius >= 1:
                pygame.draw.circle(self.window, color, (int(particle[0]), int(particle[1])), int(radius))

        self.frame += 1
