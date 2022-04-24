DIRECTIONS = [(-1, 1), (0, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (0, -1),
              (1, -1)]


class Move:
    """Class for all the possible move each turn"""

    def __init__(self, color, board):
        """Constructor for move"""
        self.board = board
        self.grid = self.board.grid()
        self.color = color

    def add_disk(self, row, column):
        """Add a disk to the board"""
        self.grid[(row, column)].color = self.color

    def swap_color(self, tiles_to_swap):
        """Call board method swap on tiles to be swapped"""
        self.board.change_color(tiles_to_swap)

    def one_full_move(self, tile_placed):
        """One full move including adding tile and swapping tiles"""
        tiles_swap = self.tiles_to_swap(tile_placed)
        self.swap_color(tiles_swap)
        self.add_disk(tile_placed.row, tile_placed.column)

    def is_inside_board(self, row, column):
        """Condition for being inside board"""
        if row < 0 or column < 0 or\
           row >= self.board.GRID_NUMBER or\
           column >= self.board.GRID_NUMBER:
            return False
        else:
            return True

    def tiles_to_swap(self, tile):
        """return tiles to swap"""

        # make empty dictionary and list
        tiles = []
        legal_moves = {}

        # for each direction, set the first tile to itself
        for direction in DIRECTIONS:
            row = tile.row
            column = tile.column
            legal_moves[direction] = []

            # keep moving forward until one of the following condition is met
            while True:
                row += direction[0]
                column += direction[1]

                # check if still on the board, break if not
                if self.is_inside_board(row, column) is False:
                    break

                # check the color
                # 1) break when met an empty tile
                if self.grid[(row, column)].color is None:
                    break
                # 2) for opponent's tile, appende to the list of fliipable tile
                elif self.grid[(row, column)].color != self.color:
                    legal_moves[direction].append(self.grid[(row, column)])
                # 3) for own tile, if the list length is zero (0), meaning no
                # opponent's tile is in between, break. Otherwise return
                else:
                    if len(legal_moves[direction]) != 0:
                        tiles += legal_moves[direction]
                    break

        return tiles

    def is_valid_move(self, tile):
        """Check if a tile is valid move"""
        if tile.color is not None:
            return False
        if self.tiles_to_swap(tile) == []:
            return False
        else:
            return True

    def is_out_of_move(self):
        """Check if computer or player is out of move"""
        for tile in self.board.tiles:
            if self.is_valid_move(tile) is True:
                return False
        return True
