from tkinter import*
from random import randint

# constants that go in the making of the grid used for the snake's movment
GRADUATION = 40
PIXEL = 10
STEP = 2 * PIXEL
WD = PIXEL * GRADUATION
HT = PIXEL * GRADUATION
# constants that go into specifying the shapes' sizes
OB_SIZE_FACTOR = 1
SN_SIZE_FACTOR = 0.9
OB_SIZE = PIXEL * OB_SIZE_FACTOR
SN_SIZE = PIXEL * SN_SIZE_FACTOR
# color constants
BG_COLOR = 'black'
OB_COLOR = 'red'
SN_COLOR = 'white'
# a dictionary to ease access to a shape's type in the Shape class
SN = 'snake'
OB = 'obstacle'
SIZE = {SN: SN_SIZE, OB: OB_SIZE}
# constants for keyboard input
UP = 'Up'
DOWN = 'Down'
RIGHT = 'Right'
LEFT = 'Left'
# a dictionary to ease access to 'directions'
DIRECTIONS = {UP: [0, -1], DOWN: [0, 1], RIGHT: [1, 0], LEFT: [-1, 0]}
AXES = {UP: 'Vertical', DOWN: 'Vertical', RIGHT: 'Horizontal', LEFT: 'Horizontal'}
# refresh time for the perpetual motion
REFRESH_TIME = 100


class Master(Canvas):
    """create the game canvas, the snake, the obstacle, keep track of the score"""
    def __init__(self, boss=None):
        super().__init__(boss)
        self.configure(width=WD, height=HT, bg=BG_COLOR)
        self.running = 0
        self.snake = None
        self.obstacle = None
        self.direction = None
        self.current = None
        self.score = Scores(boss)

    def start(self):
        """start snake game"""
        if self.running == 0:
            self.snake = Snake(self)
            self.obstacle = Obstacle(self)
            self.direction = RIGHT
            self.current = Movement(self, RIGHT)
            self.current.begin()
            self.running = 1

    def clean(self):
        """restarting the game"""
        if self.running == 1:
            self.score.reset()
            self.current.stop()
            self.running = 0
            self.obstacle.delete()
            for block in self.snake.blocks:
                block.delete()

    def redirect(self, event):
        """taking keyboard inputs and moving the snake accordingly"""
        if 1 == self.running and \
                event.keysym in AXES.keys() and\
                AXES[event.keysym] != AXES[self.direction]:
            self.current.flag = 0
            self.direction = event.keysym
            self.current = Movement(self, event.keysym)  # a new instance at each turn to avoid confusion/tricking
            self.current.begin()  # program gets tricked if the user presses two arrow keys really quickly


class Scores:
    """Objects that keep track of the score and high score"""
    def __init__(self, boss=None):
        self.counter = StringVar(boss, '0')
        self.maximum = StringVar(boss, '0')

    def increment(self):
        score = int(self.counter.get()) + 1
        maximum = max(score, int(self.maximum.get()))
        self.counter.set(str(score))
        self.maximum.set(str(maximum))

    def reset(self):
        self.counter.set('0')


class Shape:
    """This is a template to make obstacles and snake body parts"""
    def __init__(self, can, a, b, kind):
        self.can = can
        self.x, self.y = a, b
        self.kind = kind
        if kind == SN:
            self.ref = Canvas.create_rectangle(self.can,
                                               a - SN_SIZE, b - SN_SIZE,
                                               a + SN_SIZE, b + SN_SIZE,
                                               fill=SN_COLOR,
                                               width=2)
        elif kind == OB:
            self.ref = Canvas.create_oval(self.can,
                                          a - OB_SIZE, b - OB_SIZE,
                                          a + SN_SIZE, b + SN_SIZE,
                                          fill=OB_COLOR,
                                          width=2)

    def modify(self, a, b):
        self.x, self.y = a, b
        self.can.coords(self.ref,
                        a - SIZE[self.kind], b - SIZE[self.kind],
                        a + SIZE[self.kind], b + SIZE[self.kind])

    def delete(self):
        self.can.delete(self.ref)


class Obstacle(Shape):
    """snake food"""
    def __init__(self, can):
        """only create the obstacles where there is no snake body part"""
        self.can = can
        p = int(GRADUATION/2 - 1)
        n, m = randint(0, p), randint(0, p)
        a, b = PIXEL * (2 * n + 1), PIXEL * (2 * m + 1)
        while [a, b] in [[block.x, block.y] for block in self.can.snake.blocks]:
            n, m = randint(0, p), randint(0, p)
            a, b = PIXEL * (2 * n + 1), PIXEL * (2 * m + 1)
        super().__init__(can, a, b, OB)


class Block(Shape):
    """snake body part"""
    def __init__(self, can, a, y):
        super().__init__(can, a, y, SN)


class Snake:
    """a snake keeps track of its body parts"""
    def __init__(self, can):
        """initial position chosen by me"""
        self.can = can
        a = PIXEL + 2 * int(GRADUATION/4) * PIXEL
        self.blocks = [Block(can, a, a), Block(can, a, a + STEP)]

    def move(self, path):
        """an elementary step consisting of putting the tail of the snake in the first position"""
        a = (self.blocks[-1].x + STEP * path[0]) % WD
        b = (self.blocks[-1].y + STEP * path[1]) % HT
        if a == self.can.obstacle.x and b == self.can.obstacle.y:  # check if we find food
            self.can.score.increment()
            self.can.obstacle.delete()
            self.blocks.append(Block(self.can, a, b))
            self.can.obstacle = Obstacle(self.can)
        elif [a, b] in [[block.x, block.y] for block in self.blocks]:  # check if we hit a body part
            self.can.clean()
        else:
            self.blocks[0].modify(a, b)
            self.blocks = self.blocks[1:] + [self.blocks[0]]


class Movement:
    """object that enters the snake into a perpetual state of motion in a predefined direction"""
    def __init__(self, can, direction):
        self.flag = 1
        self.can = can
        self.direction = direction

    def begin(self):
        """start the perpetual motion"""
        if self.flag > 0:
            self.can.snake.move(DIRECTIONS[self.direction])
            self.can.after(REFRESH_TIME, self.begin)

    def stop(self):
        """stop the perpetual movement"""
        self.flag = 0


root = Tk()
root.title("Snake Game")
game = Master(root)
game.grid(column=1, row=0, rowspan=3)
root.bind("<Key>", game.redirect)
buttons = Frame(root, width=35, height=3*HT/5)
Button(buttons, text='Start', command=game.start).grid()
Button(buttons, text='Stop', command=game.clean).grid()
Button(buttons, text='Quit', command=root.destroy).grid()
buttons.grid(column=0, row=0)
scoreboard = Frame(root, width=35, height=2*HT/5)
Label(scoreboard, text='Game Score').grid()
Label(scoreboard, textvariable=game.score.counter).grid()
Label(scoreboard, text='High Score').grid()
Label(scoreboard, textvariable=game.score.maximum).grid()
scoreboard.grid(column=0, row=2)
root.mainloop()
