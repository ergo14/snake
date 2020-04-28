import constants
import utils

class Shape:
    """Abstract class"""
    def __init__(self, master, x, y):
        """x, y represent the centers of the shape"""
        self.master = master
        self.x = x
        self.y = y
        self.ref = getattr(master, self.draw_callback)(
            x - self.dr, y - self.dr,
            x + self.dr, y + self.dr,
            fill=self.color,
            width=2,
        )

    def modify(self, x, y):
        self.x, self.y = x, y
        self.master.coords(
            self.ref,
            x - self.dr, y - self.dr,
            x + self.dr, y + self.dr,
        )

    def delete(self):
        self.master.delete(self.ref)


class Obstacle(Shape):
    dr = constants.obstacle["size"]
    color = constants.obstacle["color"]
    draw_callback = "create_oval"
    def __init__(self, master):
        """Randomely generate a block on a free cell"""
        x, y = utils.random_coordinates()
        while (x, y) in master.snake.block_coords:
            x, y = utils.random_coordinates()

        super().__init__(master, x, y)


class Block(Shape):
    dr = constants.snake["size"]
    color = constants.snake["color"]
    draw_callback = "create_rectangle"
