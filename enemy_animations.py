import math


def zig_zag(object):
    if object.direction >= 40:
        object.direction = 0
    if object.direction <= -40:
        object.direction = 1
    min_x = object.x - object.velocity
    max_x = object.x + object.velocity

    if object.direction >= 1 and max_x <= object.window.get_width():
        object.x += object.velocity
        object.direction += 1
    if object.direction <= 0 and min_x >= 0 :
        object.x -= object.velocity
        object.direction -= 1
    object.y += object.velocity


def line(object):
    object.y += object.velocity


def circle(object):
    movement = [
        (0,0), (1,1),(2,2), (3,3), (4,4), (5, 5),
        (5, 5), (4, 4), (3, 3), (2, 2), (1, 1), (0, 0)
    ]
    object.x = movement[object.move_index][0] + object.x
    object.y = movement[object.move_index][1] + object.y
    object.move_index += 1
    if object.move_index > len(movement) - 1:
        object.move_index = 0

