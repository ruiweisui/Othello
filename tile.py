BLACK = 0
WHITE = 225


class Tile:
    """Class for black and white tile"""

    def __init__(self, row, column):
        """Tile constructor"""
        self.row = row
        self.column = column
        self.WHITE = WHITE
        self.BLACK = BLACK
        self.DIAMETER = 85
        self.color = None

    def display_tile(self):
        """Draw tile"""
        fill(self.color)
        stroke(0)
        # these number are given in the instruction
        ellipse(self.column * 100 + 50, self.row * 100 + 50,
                self.DIAMETER, self.DIAMETER)

    def change_color(self):
        """Swap color of the tile"""
        if self.color == self.WHITE:
            self.color = self.BLACK
        elif self.color == self.BLACK:
            self.color = self.WHITE
