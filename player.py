from move import Move
from tile import Tile

DIAMETER = 85


class Player(Move):
    """Class for player moves"""

    def first_two_tile(self):
        """Player place down the first two tiles"""
        self.add_disk(self.board.DOWN, self.board.LEFT)
        self.add_disk(self.board.UP, self.board.RIGHT)
        self.has_hint = False

    def give_hint(self):
        """Give player hint if clicked on the button"""
        for tile in self.board.tiles:
            if self.is_valid_move(tile):
                noFill()
                stroke(0)
                # these number are given in the instruction
                ellipse(tile.column * 100 + 50, tile.row * 100 + 50,
                        DIAMETER, DIAMETER)
                self.has_hint = True
                self.hint = tile
                return

    def remove_hint(self):
        """Remove hint"""
        if self.has_hint is True:
            tile = self.hint
            # this is dark green color ro match the background
            fill(color(40, 100, 40))
            stroke(color(40, 100, 40))
            # use an ellipse with slightly bigger diameter to cover the hint
            ellipse(tile.column * 100 + 50, tile.row * 100 + 50,
                    DIAMETER+5, DIAMETER+5)
            self.has_hint = False
