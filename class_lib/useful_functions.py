from basics import Vector
from math import sqrt
from globals import MIN_DIST


def coordinate_system(i_prime):
    """Returns a coordinate system (i', j' and k') given i'"""
    new_i = i_prime.unit
    if new_i == Vector(0, 0, 1) or new_i == Vector(0, 0, -1):
        new_j = Vector(1, 0, 0)
    else:
        new_j = Vector(-new_i.y, new_i.x, 0).unit
    new_k = new_i ** new_j  # Vector product
    return new_i, new_j, new_k


def min_pos_root(a, b, c):
    """Returns the minimum positive root for the function ax²+bx+c = 0. If no positive roots exist, returns None"""
    delta = b * b - 4 * a * c
    if delta < 0:
        return None

    delta = sqrt(delta)
    r1 = (-b + delta) / (2 * a)
    r2 = (-b - delta) / (2 * a)

    if r1 >= MIN_DIST:
        if r2 >= MIN_DIST:
            return min(r1, r2)
        return r1
    else:
        if r2 >= MIN_DIST:
            return r2
        return None
