from basics import Vector


def coordinate_system(i_prime):
    """Returns a coordinate system (i', j' and k') given i'"""
    new_i = i_prime.unit
    if new_i == Vector(0, 0, 1) or new_i == Vector(0, 0, -1):
        new_j = Vector(1, 0, 0)
    else:
        new_j = Vector(-new_i.y, new_i.x, 0).unit
    new_k = new_i ** new_j  # Vector product
    return new_i, new_j, new_k
