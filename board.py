from tile import Tile

STROKE_WEIGHT = 3
GRID_COLOR = 0
GREY = 150
BLACK = 0
TEXT_SIZE = 42
SPACE = 25
HINT_SIZE = (350, 85)
HALF = 0.5
LETTER_COORD = (950, 745)


class Board:
    """Class for board"""

    def __init__(self, WIDTH, HEIGHT, GRID_NUMBER):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.GRID_NUMBER = GRID_NUMBER
        self.SPACE = WIDTH/GRID_NUMBER
        self.UP = self.LEFT = self.GRID_NUMBER*HALF - 1
        self.DOWN = self.RIGHT = self.GRID_NUMBER*HALF
        # self.MESSAGE_COORD = 50
        self.tiles = [Tile(r, c)
                      for r in range(GRID_NUMBER)
                      for c in range(GRID_NUMBER)]
        self.game_over = False

    def grid(self):
        """return a dictionary of board with the value of each tile object"""
        grid = {}
        for row in range(self.GRID_NUMBER):
            for column in range(self.GRID_NUMBER):
                # this equation calculates the position of tile in a 2d list
                grid[(row, column)] = self.tiles[row*self.GRID_NUMBER + column]
        return grid

    def display_board(self):
        """Draw board"""
        # draw background
        background(40, 100, 40)

        # draw grid
        noFill()
        stroke(GRID_COLOR)
        strokeWeight(STROKE_WEIGHT)
        for i in range(1, self.GRID_NUMBER + 1):
            line(i*self.SPACE, 0, i*self.SPACE, self.WIDTH)
        for i in range(1, self.GRID_NUMBER):
            line(0, i*self.SPACE, self.HEIGHT, i*self.SPACE)

        # draw rectangle for displaying info
        fill(GREY)
        self.HINT_COORD = (self.WIDTH + SPACE,
                           self.HEIGHT - HINT_SIZE[1] - SPACE)
        rect(self.HINT_COORD[0], self.HINT_COORD[1],
             HINT_SIZE[0], HINT_SIZE[1])
        fill(BLACK)
        textSize(TEXT_SIZE)
        text("HINT", LETTER_COORD[0], LETTER_COORD[1])

    def change_color(self, tiles_to_swap):
        """Change color for tiles"""
        for tile in tiles_to_swap:
            tile.change_color()

    def reset_board(self):
        """Rest the board for test"""
        for i in range(self.GRID_NUMBER*self.GRID_NUMBER):
            self.tiles[i].color = None
