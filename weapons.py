class Weapon:
    def __init__(self, name, cooldown, shots, color):
        self.name = name
        # Frames between shots while fire is held
        self.cooldown = cooldown
        # One (x offset, horizontal velocity) pair per bullet fired
        self.shots = shots
        # Colour of the weapon's power-up
        self.color = color


BLASTER = Weapon("Blaster", 20, [(0, 0)], (255, 255, 255))
DOUBLE = Weapon("Double", 18, [(-10, 0), (10, 0)], (0, 160, 255))
SPREAD = Weapon("Spread", 22, [(0, -1.5), (0, 0), (0, 1.5)], (255, 160, 0))
RAPID = Weapon("Rapid", 7, [(0, 0)], (200, 0, 255))

# Weapons that enemies can drop as power-ups
POWER_UPS = [DOUBLE, SPREAD, RAPID]
