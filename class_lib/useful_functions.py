from basics import Vector
from math import sqrt
from globals import MIN_DIST


def all_pos_roots(a, b, c):
    """Positive roots of a quadratic polynomial, already in order"""
    roots = []
    if a == 0:
        if b == 0:
            return None
        r = -c / b
        if r >= MIN_DIST:
            roots.append(r)
        return roots

    delta = b * b - 4 * a * c
    if delta < 0:
        return None

    delta = sqrt(delta)
    r1 = (-b + delta) / (2 * a)
    r2 = (-b - delta) / (2 * a)

    if r1 >= MIN_DIST:
        roots.append(r1)
    if r2 >= MIN_DIST:
        roots.append(r2)
    if len(roots) > 1:
        roots.sort()
    return roots


def min_pos_root(a, b, c):
    """Returns the minimum positive root for the function ax²+bx+c = 0. If no positive roots exist, returns None"""
    roots = all_pos_roots(a, b, c)
    if not roots or len(roots) == 0:
        return None
    return roots[0]


def reflected_vector(v, axis):
    """
    Returns vector rotated 180° around a given axis
    """
    unit_axis = axis.unit
    gama = unit_axis * (v * unit_axis)
    output = 2 * gama - v
    return output


def attenuate_by_distance_sq(distance_sq):
    if distance_sq > 0.1:
        return 1 / distance_sq
    else:
        return 10
