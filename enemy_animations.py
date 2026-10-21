import math
import random

# Enemies are 32x32
ENEMY_SIZE = 32


def zig_zag(object):
    # Swing sideways in legs of random length, bouncing off the window edges
    object.move_index -= 1
    if object.move_index <= 0:
        object.direction = -object.direction
        object.move_index = random.randint(30, 60)

    object.x += object.direction * object.velocity
    max_x = object.window.get_width() - ENEMY_SIZE
    if object.x <= 0 or object.x >= max_x:
        object.x = max(0, min(max_x, object.x))
        object.direction = -object.direction
        object.move_index = random.randint(30, 60)
    object.y += object.velocity * 0.75


def line(object):
    object.y += object.velocity


def circle(object):
    # Orbit a centre point that slowly sinks down the screen
    radius = 50
    if object.move_index == 0:
        # Keep the whole orbit inside the window
        object.anchor_x = max(radius, min(object.window.get_width() - ENEMY_SIZE - radius, object.x))
        object.anchor_y = object.y
    object.move_index += 1

    # Angular speed chosen so the ship's speed along the orbit matches its velocity
    angle = object.direction * object.move_index * object.velocity / radius
    object.anchor_y += object.velocity * 0.4
    object.x = object.anchor_x + radius * math.sin(angle)
    object.y = object.anchor_y - radius * math.cos(angle) + radius
