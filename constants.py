# layout
tick_num = 40
tick_len = 10
step_len = 2 * tick_len

layout = {
    "size": tick_num * tick_len,
    "background_color": "grey",
}

# shapes
snake_factor = 1
obstacle_factor = 0.9

obstacle = {
    "size": tick_len * obstacle_factor,
    "color": "red",
}

snake = {
    "size": tick_len * snake_factor,
    "color": "white",
}

# constants for keyboard input
direction_vectors = {
    "Up": (0, -1),
    "Down": (0, 1),
    "Left": (-1, 0),
    "Right": (1, 0),
}

# refresh time for the perpetual motion
refresh_ms = 100
