import random
import constants


def random_coordinates():
    p = int(constants.tick_num / 2 - 1)
    n, m = random.randint(0, p), random.randint(0, p)
    return constants.tick_len * (2 * n + 1), constants.tick_len * (2 * m + 1)

def same_axis(vector_a, vector_b):
    dot_product = vector_a[0] * vector_b[0] + vector_a[1] * vector_b[1]
    return dot_product != 0
