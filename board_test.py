from board import Board
from tile import Tile

board = Board(800, 800, 8)


def test_constructor():
    assert board.WIDTH == 800
    assert board.HEIGHT == 800
    assert board.GRID_NUMBER == 8
    assert board.SPACE == 100
    assert board.UP == 3
    assert board.LEFT == 3
    assert board.DOWN == 4
    assert board.RIGHT == 4
    assert len(board.tiles) == 64
    assert board.game_over is False


def test_grid():
    assert len(board.grid()) == 64
    assert board.grid()[0, 0] == board.tiles[0]
    assert board.grid()[7, 7] == board.tiles[-1]


def test_change_color():
    t1 = Tile(1, 2)
    t1.color = 0
    t2 = Tile(2, 2)
    t2.color = 225
    t3 = Tile(3, 2)
    t3.color = None
    board.change_color([t1, t2, t3])
    assert t1.color == 225
    assert t2.color == 0
    assert t3.color is None
